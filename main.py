# === Минимально адаптированная версия под Android ===
# Сохранено ~95% исходного кода. Изменения только там, где это критично для Android:
# 1) Добавлен флаг IS_ANDROID (через kivy.utils.platform).
# 2) ffprobe не вызывается на Android (возвращает None).
# 3) Проигрывание на Android через Kivy Video/Image, на десктопе — как у тебя (mpv).
# 4) Windows-пайп и автозапуск не трогаем (они и так отключены вне Windows).

# Инициализация системных библиотек, работа с ядрами, датами и временем
import os
import json
import datetime
import hashlib
import threading
import subprocess
import time
from pathlib import Path
import requests
import subprocess, shutil, sys, os

# NEW: определяем платформу (Android/десктоп)
try:
    from kivy.utils import platform as _kv_platform
    IS_ANDROID = (_kv_platform == 'android')
except Exception:
    IS_ANDROID = False

if getattr(sys, 'frozen', False):  # запущено из .exe
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).resolve().parent
mpv_dir = base_dir / 'mpv'
if mpv_dir.exists():
    os.environ['PATH'] = str(mpv_dir) + os.pathsep + os.environ.get('PATH', '')


# Интеграция конфигов и окна, принимающие опциональные параметры (скрыть курсор, сделать фулскрин, убрать рамки) 
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('modules', 'touchring', '')
Config.set('graphics', 'borderless', '1')
Config.set('input', 'wm_pen', '')
Config.set('input', 'wm_touch', '')
Config.set('kivy', 'video', 'ffpyplayer')  # для Android это важно
Config.set('kivy', 'keyboard_mode', 'system')


from kivy.core.window import Window
Window.clearcolor = (0, 0, 0, 1)
Window.softinput_mode = 'pan'


# Инициализация библиотек, предназначенных для работы с Kivy, а также серверные обращения клиента
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.image import Image as KivyImage
from media_content_management_api_client.client import Client
from media_content_management_api_client.api.client_api.get_api_playlist import sync_detailed as get_playlist
from media_content_management_api_client.models.playlist import Playlist

def ffprobe_cmd():
    # NEW: на Android не пытаемся искать/запускать ffprobe
    if IS_ANDROID:
        return None

    # База: если onefile — PyInstaller распакует файлы во временную _MEIPASS,
    # иначе берём папку рядом с exe (фrozen) или со скриптом (dev).
    base = Path(getattr(sys, "_MEIPASS", Path(sys.executable if getattr(sys, "frozen", False) else __file__).parent))
    local = base / 'bin' / ('ffprobe.exe' if os.name == 'nt' else 'ffprobe')

    if local.exists():
        os.environ['PATH'] = str(local.parent) + os.pathsep + os.environ.get('PATH', '')
        return str(local)

    found = shutil.which('ffprobe')
    return found or 'ffprobe'

def ensure_local_bin_on_path():
    base = Path(getattr(sys, "_MEIPASS",
                        Path(sys.executable if getattr(sys, "frozen", False) else __file__).parent))
    bin_dir = base / 'bin'
    if bin_dir.exists():
        os.environ['PATH'] = str(bin_dir) + os.pathsep + os.environ.get('PATH', '')

from kivy.uix.video import Video as _Video

class SafeVideo(_Video):
    def reload(self, *args, **kw):
        # Блокируем попытку Image загрузить mp4 как изображение
        src = getattr(self, 'source', '') or ''
        if Path(src).suffix.lower() in _VIDEO_EXTS:
            return
        return super().reload(*args, **kw)
    
from kivy.logger import Logger
import logging

class _SilenceMp4ImageErrors(logging.Filter):
    def filter(self, record):
        s = str(record.msg)
        # отбрасываем только "Image: Error loading <...mp4>"
        return not ('Error loading <' in s and s.lower().endswith('.mp4>'))

Logger.addFilter(_SilenceMp4ImageErrors())

# Инициализация констант, которые содержат в себе информацию о допустимых форматах изображений и видео
_IMAGE_EXTS = frozenset(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'))
_VIDEO_EXTS = frozenset(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.mpg', '.mpeg'))


# Функция, позволяющая ставить приложение в автозапуск (Windows)
def ensure_autostart(app_name="MyKivyPlayer"):
    if os.name != "nt":
        return False
    import sys, winreg
    from pathlib import Path
    if getattr(sys, "frozen", False):           
        cmd = f'"{sys.executable}"'
    else:                                       
        py = Path(sys.executable)
        pyw = py.with_name("pythonw.exe")
        interp = pyw if pyw.exists() else py
        cmd = f'"{interp}" "{Path(__file__).resolve()}"'
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
        try:
            cur, _ = winreg.QueryValueEx(key, app_name)
        except FileNotFoundError:
            cur = None
        if cur != cmd:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
    return True


# Утилита, возвращающая хэш для проверки целостности скачиваемых файлов
def sha256_of_file(path, buf_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(buf_size), b''):
            h.update(chunk)
    return h.hexdigest()


# Определение типа файла (image/video/unknown)
def guess_media_type(path):
    ext = Path(path).suffix.lower()
    if ext in _IMAGE_EXTS:
        return 'image'
    if ext in _VIDEO_EXTS:
        return 'video'
    return 'unknown'


# Функция определения длины видео в секундах (требуется ffprobe)
def get_video_duration_seconds(path):
    # NEW: на Android возвращаем None (не ограничиваем длительность фактом)
    if IS_ANDROID:
        return None
    cmd = ffprobe_cmd()
    if not cmd:
        return None
    out = subprocess.run(
        [cmd, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nk=1:nw=1', path],
        capture_output=True, text=True, timeout=5
    )
    return round(float(out.stdout.strip())) if out.returncode == 0 and out.stdout.strip() else None


# Преобразование времени из общего числа секунд в формат "HH:MM:SS" и наоборот
def to_sec(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s
def to_str(sec):
    h = sec // 3600; m = (sec % 3600) // 60; s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# Построение расписания игры в формате словаря: время => событие и данные о событии (подробнее ниже)
def build_schedule(ids, orders, starts, ends, days_list, durations, number_of_day):
    # Фильтрация по дню недели и обработка исключений; заполнение данных по ключам
    FULL = set(range(1, 8))
    raw = []
    for i_id, ord_, st, en, dw, dur in zip(ids, orders, starts, ends, days_list, durations):
        if None in (i_id, ord_, st, en, dur):
            continue
        days = set(dw) if dw else FULL
        if number_of_day not in days and number_of_day in [1,2,3,4,5,6,7]:
            continue
        ts = to_sec(st); te = to_sec(en)
        if ts >= te:
            continue
        raw.append({'id': i_id, 'order': ord_, 'start': ts, 'end': te, 'duration': dur})

    # Группировка начала и конца элементов для создания карусели
    seg_map = {}
    for e in raw:
        seg_map.setdefault((e['start'], e['end']), []).append(e)
    segments = []
    for (st, en), lst in seg_map.items():
        lst_sorted = sorted(lst, key=lambda x: x['order'])
        segments.append({
            'start': st, 'end': en, 'entries': lst_sorted,
            'first_order': lst_sorted[0]['order'], 'started': False,
            'idx': 0
        })

    # Цикл, направленный на заполнение расписания: одна итерация = одно событие
    events = {}
    active = None
    cur_ord = None
    end_time = None
    while True:
        # Определние ключевых точек времени, когда что-то начинается, переключается или заканчивается
        pending = [s for s in segments if not s['started']]
        next_arr = min((s['start'] for s in pending), default=None)
        fin = end_time
        if fin is None:
            if next_arr is None:
                break
            now = next_arr
        else:
            if next_arr is None:
                now = fin
            else:
                now = min(fin, next_arr)
        t_str = to_str(now)
        arr = [s for s in segments if not s['started'] and s['start'] == now]

        # Обработка первичных данных для нового сегмента при нахождении временной точки изменения 
        if arr:
            s_new = max(arr, key=lambda s: s['first_order'])
            for s in arr:
                s['started'] = True
            if active is None or s_new['first_order'] > cur_ord:
                active = s_new
                active['idx'] = 0
                ent = active['entries'][0]
                cur_ord = ent['order']
                events[t_str] = {'action': 'включить элемент', 'номер': ent['id'], 'duration': ent['duration']}
                # Schedule finish
                if len(active['entries']) == 1:
                    end_time = active['end']
                else:
                    end_time = now + ent['duration']
            continue

        # Обработка карусели: переход к следующему её элементу или завершение её игры
        if fin is not None and fin == now:
            if active is None:
                end_time = None
                continue
            if len(active['entries']) == 1:
                events[t_str] = {'action': 'стоп элемент'}
                active = None
                cur_ord = None
                end_time = None
            else:
                if now >= active['end']:
                    events[t_str] = {'action': 'стоп элемент'}
                    active = None
                    cur_ord = None
                    end_time = None
                else:
                    active['idx'] = (active['idx'] + 1) % len(active['entries'])
                    ent = active['entries'][active['idx']]
                    cur_ord = ent['order']
                    events[t_str] = {'action': 'включить элемент', 'номер': ent['id'], 'duration': ent['duration']}
                    next_finish = now + ent['duration']
                    end_time = min(next_finish, active['end'])
            continue

        # Запуск отложенных сегментов, когда элемент может проигрываться, но не проигрывается из-за наложения элементов
        if active is None:
            delayed = [s for s in segments if not s['started'] and s['start'] < now < s['end']]
            if delayed:
                s_new = min(delayed, key=lambda s: s['start'])
                s_new['started'] = True
                active = s_new
                active['idx'] = 0
                ent = active['entries'][0]
                cur_ord = ent['order']
                events[t_str] = {'action': 'включить элемент', 'номер': ent['id'], 'duration': ent['duration']}
                if len(active['entries']) == 1:
                    end_time = active['end']
                else:
                    end_time = now + ent['duration']
                continue
        break
    return events


# Функция, которая отправляет список имён всех пользовательских id, используя актуальный IP-адрес
def fetch_client_ids_from_server(ip):
    try:
        url = f"http://{ip}/api/clients"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json().get("data")
        return [item["client_id"] for item in data]
    except:
        return []


# Класс Kivy, котоырй открывает окно при первом запуске, чтобы получить от пользователя актуальный IP-адрес
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import threading

class IPInputDialog(Popup):
    def __init__(self, on_submit=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Введите IP адрес Konkord DS"
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        box.add_widget(Label(text="Введите IP адрес Konkord DS"))
        self.text_input = TextInput(hint_text="", multiline=False)
        # --- важные настройки для стабильной клавиатуры ---
        self.text_input.unfocus_on_touch = False      # тап по полю не снимает фокус
        self.text_input.write_tab = False
        self.text_input.focus = True                  # сразу фокус на поле
        self.text_input.bind(focus=self._on_focus)    # при получении фокуса – открыть клавиатуру
        # ---------------------------------------------------
        box.add_widget(self.text_input)

        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=20)
        box.add_widget(self.error_label)

        self.submit_btn = Button(text="Отправить", size_hint=(1, 0.3))
        self.submit_btn.bind(on_release=self._on_submit)
        box.add_widget(self.submit_btn)

        self.content = box
        self._on_submit_callback = on_submit

        # --- поддержка пульта Android TV (DPAD + OK/Enter) ---
        self.focusables = [self.text_input, self.submit_btn]
        self.focus_index = 0
        self.focusables[self.focus_index].focus = True
        self._tv_keys_bound = True
        Window.bind(on_key_down=self._on_tv_key_down)
        # ------------------------------------------------------

        # гарантированный показ клавиатуры после построения попапа
        Clock.schedule_once(lambda dt: self._ensure_keyboard_open(), 0.05)

    def on_open(self):
        # удерживаем фокус на поле и ещё раз открываем клавиатуру
        self.focus_index = 0
        self.focusables[self.focus_index].focus = True
        Clock.schedule_once(lambda dt: self._ensure_keyboard_open(), 0.05)

    def on_dismiss(self):
        # чтобы обработчик пульта не висел дальше
        if getattr(self, "_tv_keys_bound", False):
            try:
                Window.unbind(on_key_down=self._on_tv_key_down)
            except Exception:
                pass
            self._tv_keys_bound = False

    # === стабильный показ клавиатуры ===
    def _on_focus(self, instance, value):
        if value:
            # небольшая задержка помогает на Android TV, чтобы UI успел стабилизироваться
            Clock.schedule_once(lambda dt: self._ensure_keyboard_open(), 0.02)

    def _ensure_keyboard_open(self):
        # стандартный путь Kivy: запросить клавиатуру у Window
        try:
            Window.request_keyboard(lambda: None, self)
        except Exception:
            pass

    # === навигация пультом ===
    def _on_tv_key_down(self, window, key, scancode, codepoint, modifiers):
        # DPAD: UP=19, DOWN=20, LEFT=21, RIGHT=22, CENTER(OK)=23, ENTER=66
        if key in (19, 20):  # вверх/вниз
            self.focusables[self.focus_index].focus = False
            self.focus_index = (self.focus_index - 1) % len(self.focusables) if key == 19 \
                               else (self.focus_index + 1) % len(self.focusables)
            self.focusables[self.focus_index].focus = True
            return True
        if key in (23, 66):  # OK / Enter
            current = self.focusables[self.focus_index]
            if isinstance(current, Button):
                current.trigger_action(duration=0.1)
            else:  # TextInput
                current.focus = True
                self._ensure_keyboard_open()  # критично: принудительно открыть клавиатуру
            return True
        if key in (21, 22):  # влево/вправо
            if self.focusables[self.focus_index] is self.submit_btn:
                # для кнопки трактуем как переключение вверх/вниз
                return self._on_tv_key_down(window, 19 if key == 21 else 20, scancode, codepoint, modifiers)
            # на TextInput пропускаем — пусть двигается курсор
            return False
        return False

    # === отправка остаётся как у вас ===
    def _on_submit(self, instance):
        ip = self.text_input.text.strip()
        self.error_label.text = "Проверка..."
        instance.disabled = True

        def worker():
            ids = fetch_client_ids_from_server(ip)
            def finish(dt):
                if len(ids) != 0:
                    self.dismiss()
                    if self._on_submit_callback:
                        self._on_submit_callback(ip)
                else:
                    self.error_label.text = "Введён неверный IP-адрес или он не существует в базе"
                    instance.disabled = False
            Clock.schedule_once(finish, 0)
        threading.Thread(target=worker, daemon=True).start()





# Основной класс Kivy: в нём происходят все события вычислений, обработки и воспроизведения
class MyApp(App):


    # Контейнер, в котором создаётся корневой виджет и отключаются лишние функции Kivy (рамка окна, реакция на тачпад)
    def build(self):
        root = BoxLayout()
        self.media_box = BoxLayout()
        root.add_widget(self.media_box)
        def _drag_start(w, touch):
            if touch.y >= Window.height - 40:
                w._drag = touch.pos; return True
        def _drag_move(w, touch):
            p = getattr(w, '_drag', None)
            if not p: return False
            dx, dy = touch.x - p[0], touch.y - p[1]
            Window.left += dx; Window.top -= dy
            w._drag = touch.pos; return True
        def _drag_end(w, touch):
            w._drag = None; return False
        root.bind(on_touch_down=_drag_start, on_touch_move=_drag_move, on_touch_up=_drag_end)
        return root


    # Действия, происходящие на старте: инициализация переменных и чтение IP-адреса из файла .txt
    def on_start(self):
        ensure_local_bin_on_path()

        # NEW: на Android mpv/pipe не используем
        self._mpv_proc = None
        self._mpv_io = None
        if os.name == "nt":
            self._mpv_pipe = r'\\.\pipe\mpv-kivy'
            try:
                ensure_autostart("MyKivyPlayer")
            except Exception:
                pass
        else:
            self._mpv_pipe = None  # на Android/Unix здесь ничего не создаём

        self._playlist_seq = 0
        Window.bind(on_key_down=self._on_key_down)
        self._updates_inflight = False
        self.schedule = {}
        self.ready_play = False

        os.makedirs(self.user_data_dir, exist_ok=True)
        ip_path = os.path.join(self.user_data_dir, "client_ip.txt")
        client_ip = ""
        if os.path.exists(ip_path):
            with open(ip_path, "r", encoding="utf-8") as f:
                client_ip = f.read().strip()

        if client_ip: # Если IP найден, значит, его уже записали при первом запуске и можно продолжать
            try:
                self._after_ip_available(client_ip)
            except RuntimeError as e:
                Popup(title="Ошибка авторизации", content=Label(text=str(e)), size_hint=(0.8, 0.4)).open()
        else:
            self._show_ip_dialog() # Если нет, значит файл утерян или это и есть первый запуск


    # Открытие окна ввода IP-адреса при первом запуске или потере файла .txt с IP
    def _show_ip_dialog(self):
        dlg = IPInputDialog(on_submit=self._on_ip_entered)
        dlg.open()


    # Инициализация и запись в .txt файл полученного IP при его вводе в первый запуск
    def _on_ip_entered(self, ip):
        ip_path = os.path.join(self.user_data_dir, "client_ip.txt")
        with open(ip_path, "w", encoding="utf-8") as f:
            f.write(ip)
        self._after_ip_available(ip)


    # Авторизация: чтение клиентского ID (или его запись при отсутсвии) и запуск цикла проверки обновлений на сервере
    def _after_ip_available(self, client_ip):
        cid_path = os.path.join(self.user_data_dir, "client_id.txt")
        client_id = ""
        if os.path.exists(cid_path):
            with open(cid_path, "r", encoding="utf-8") as f:
                client_id = f.read().strip()
        if not client_id:
            ids = fetch_client_ids_from_server(client_ip)
            if not ids:
                raise RuntimeError(f"Не удалось получить client_id с сервера по адресу {client_ip}. Проверьте подключение к сети Интернет или обратитесь к системному администратору.")
            client_id = ids[-1]
            with open(cid_path, "w", encoding="utf-8") as f:
                f.write(client_id)

        print(f"Используем client_id: {client_id}")
        print(f"Используем client_ip: {client_ip}")
        self.client_id = client_id
        self.client_ip = client_ip

        pl_path = os.path.join(self.user_data_dir, "playlist.txt")
        if not os.path.exists(pl_path):
            with open(pl_path, "w", encoding="utf-8") as f:
                f.write("")  # пустой файл
        else:
            try:
                with open(pl_path, "r", encoding="utf-8") as f:
                    val = f.read().strip()
                if val.isdigit():
                    Clock.schedule_once(lambda _dt, pid=int(val): self._playlist(pid), 0)
            except Exception:
                pass

        Clock.schedule_once(self._check_updates, 0)


    # Ежесекундная проверка обновлений по константе self._utc_time и обработка событий
    def _check_updates(self, dt):
        try:
            # Вычисление времени
            now = datetime.datetime.now().astimezone()
            now_str = now.strftime('%H:%M:%S')
            self.number_of_day = now.isoweekday()


            # Обработка событий (с учётом защиты от двойного срабатывания) для операций с медиа
            prev_str = (now - datetime.timedelta(seconds=1)).strftime('%H:%M:%S')
            for key in (now_str, prev_str):
                if self.ready_play and key in self.schedule and key != getattr(self, '_last_fired_ts', None):
                    self._last_fired_ts = key
                    ev = self.schedule[key]
                    if ev['action'] == 'включить элемент':
                        num = ev['номер']
                        file_path = os.path.join(self.media_dir, self.deshifr[num])
                        self._play_media_from_desktop(os.path.abspath(file_path), self.type_file[self.ids.index(num)])
                    else:
                        self._stop_current_media()
                    break

            # Сбор информации с сервера и выявление обновлений
            if not getattr(self, '_updates_inflight', False):
                self._updates_inflight = True
                def worker():
                    data = None
                    try:
                        resp = requests.get(
                            f"http://{self.client_ip}/api/updates",
                            params={'client_id': self.client_id, 'last_check': '2025-07-02T10:00:00Z'},
                            timeout=(1, 3)
                        )
                        resp.raise_for_status()
                        data = resp.json().get("data", {}).get("updates", []) or []
                    except Exception:
                        pass
                    def finish(_dt):
                        try:
                            if data is not None:
                                prev = getattr(self, '_prev_updates_len', None)
                                if prev is None:
                                    self._prev_updates_len = len(data)
                                else:
                                    if len(data) > self._prev_updates_len:
                                        client = Client(base_url=f"http://{self.client_ip}")
                                        response = get_playlist(client=client, client_id=self.client_id, name=f"{data[-1]['playlist_id']}")
                                        if response.status_code != 200:
                                            print(f"Ошибка запроса: HTTP {response.status_code}")
                                            print("Тело ответа:", response.content.decode("utf-8"))
                                        else:
                                            playlist_id = data[-1]['playlist_id']
                                            print(f"Получено обновление: плейлист #{playlist_id}")
                                            try:
                                                with open(os.path.join(self.user_data_dir, "playlist.txt"), "w", encoding="utf-8") as f:
                                                    f.write(str(playlist_id))
                                            except Exception:
                                                pass
                                            self.ready_play = False
                                            Clock.schedule_once(lambda __dt: self._playlist(playlist_id), 0)
                                    self._prev_updates_len = len(data)
                        finally:
                            self._updates_inflight = False
                    Clock.schedule_once(finish, 0)
                threading.Thread(target=worker, daemon=True).start()
        finally:
            Clock.schedule_once(self._check_updates, 1.0)


    # События, происходящие при получении плейлиста: скачивание и обработка медиа-файлов
    def _playlist(self, playlist):
        # Извлечение данных о медиа-файлах внутри плейлиста
        client = Client(base_url=f"http://{self.client_ip}")
        response = get_playlist(client=client, client_id=self.client_id, name=f"{playlist}")
        raw = response.content.decode("utf-8")
        wrapper = json.loads(raw)
        data = wrapper.get("data")
        if data is None:
            print("В ответе нет поля data")
        playlist = Playlist.from_dict(data)

        # Обработка данных о каждом медиа-файле внутри плейлиста
        videos_data = []
        for item in playlist.items or []:
            videos_data.append(item.to_dict())
        start_time = []
        end_time = []
        days_of_the_week = []
        order = []
        duration = []
        check_sum = []
        self.ids = []
        self.name_file = []
        self.type_file = []
        self.deshifr = {}
        for elem in videos_data:
            self.deshifr[str(elem['media_file']['id'])] = elem['media_file']['filename']
            self.ids.append(str(elem['media_file']['id']))
            self.name_file.append(elem['media_file']['filename'])
            check_sum.append(elem['media_file']['checksum'])
            start_time.append(elem['start_time'])
            end_time.append(elem['end_time'])
            days_of_the_week.append(elem['days_of_week'])
            order.append(elem['order_index'])
            duration.append(elem['display_duration'])
        
        # Выявление ненужных медиа-файлов и регистрация недостающих в рамках актуального плейлиста
        to_download = []
        downloads_dir = os.path.join(self.user_data_dir, "downloads")
        os.makedirs(downloads_dir, exist_ok=True)
        for fi in os.listdir(downloads_dir): 
            path = os.path.join(downloads_dir, fi)
            if os.path.isfile(path):
                if fi not in self.name_file:
                    os.remove(path)
        for fi in set(self.name_file):
            if fi not in os.listdir(downloads_dir):
                to_download.append(fi)  
        self.media_dir = downloads_dir  
        self._playlist_seq += 1
        seq = self._playlist_seq

        def worker():
            # Цикл скачивания файлов, занесения их в текстовый файл и определения длины файла
            for i in range(len(order)):
                file_path = os.path.join(downloads_dir, self.name_file[i])
                self.media_dir = os.path.join(self.user_data_dir, "downloads")
                expected = (check_sum[i] or "").lower()

                # Проверка хэша для верификации целостности файла для уже скачанных элементов
                need_download = self.name_file[i] in to_download
                if not need_download and expected and os.path.exists(file_path):
                    try:
                        actual = sha256_of_file(file_path).lower()
                    except Exception:
                        actual = None
                    if actual != expected:
                        print(f"Хэш не совпал (локальный) для {self.name_file[i]} — перекачиваем")
                        need_download = True
                        try: 
                            os.remove(file_path)
                        except: 
                            pass

                # Генерация хэша для верификации целостности файла для элементов, которые необходимо скачать
                if need_download:
                    download_url = f"http://{self.client_ip}/api/media/{self.ids[i]}/download"
                    try:
                        os.makedirs(self.media_dir, exist_ok=True)
                        resp = requests.get(download_url, stream=True, timeout=10)
                        resp.raise_for_status()
                        if resp.status_code == 200:
                            tmp = file_path + ".part"
                            with open(tmp, "wb") as f:
                                for chunk in resp.iter_content(1024 * 256):
                                    if chunk: f.write(chunk)
                            os.replace(tmp, file_path)
                        else:
                            print(f"Ошибка при скачивании media/{self.ids[i]}/download: HTTP {resp.status_code}")
                    except Exception as e:
                        print(f"Ошибка скачивания {download_url}: {e}")

                    if expected and os.path.exists(file_path):
                        try:
                            actual = sha256_of_file(file_path).lower()
                        except Exception:
                            actual = None
                            print(f"Контрольная сумма НЕ совпала для {self.name_file[i]}.\n"
                                f"ожидалось: {expected}\nполучено:  {actual}\nФайл удалён.")
                        if actual != expected:
                            print(f"Контрольная сумма НЕ совпала для {self.name_file[i]}.\n"
                                f"ожидалось: {expected}\nполучено:  {actual}\nФайл удалён.")
                            try: 
                                os.remove(file_path)
                            except: 
                                pass
                            self.type_file.append('unknown')
                            duration[i] = 5
                            continue 
                
                # Определение типа файла и нормализация duration
                self.type_file.append(guess_media_type(os.path.abspath(file_path)))
                if self.type_file[i] == 'image':
                    # для картинок дефолт, если не задано
                    duration[i] = 5 if not duration[i] else int(duration[i])
                elif self.type_file[i] == 'video':
                    volume = get_video_duration_seconds(os.path.abspath(file_path))
                    if volume is None:
                        # ffprobe недоступен или не смог прочитать — не сравниваем с None
                        duration[i] = 5 if not duration[i] else int(duration[i])
                    else:
                        # есть длина — подрезаем длительность до длины видео
                        if not duration[i] or duration[i] > volume:
                            duration[i] = int(volume)
                        else:
                            duration[i] = int(duration[i])
                else:
                    # unknown — просто дефолт
                    duration[i] = 5

            def finish(dt):
                if seq != self._playlist_seq:
                    return
                self.ready_play = True
                self.schedule = build_schedule(self.ids, order, start_time, end_time, days_of_the_week, duration, self.number_of_day)
                # self.schedule = {'00:30:10': {'action': 'включить элемент', 'номер': '31', 'duration': 10}}
                print(self.schedule)
            Clock.schedule_once(finish, 0)
        threading.Thread(target=worker, daemon=True).start()


    # Включение медиа-файла: остановка предыдущего, если как таковой включён и включение актуального
    def _ensure_mpv(self):
        # NEW: на Android mpv не используется
        if IS_ANDROID:
            return
        if getattr(self, '_mpv_proc', None) and self._mpv_proc.poll() is None:
            return
        mpv_exe = shutil.which("mpv") or "mpv"
        args = [
            mpv_exe,
            "--idle=yes",             # держать процесс/окно между роликами
            "--force-window=yes",     # окно существует всегда
            "--fs=yes",               # фуллскрин
            "--no-osc",               # без плавающей панели
            "--osd-level=0",          # без OSD
            "--input-media-keys=no",
            "--no-config",            # игнорировать пользовательские конфиги
            f"--input-ipc-server={self._mpv_pipe}",
        ]
        self._mpv_proc = subprocess.Popen(args, close_fds=True)

        # ждём появления IPC-пайпа и подключаемся
        t0 = time.time()
        while time.time() - t0 < 3:
            try:
                self._mpv_io = open(self._mpv_pipe, "w+b", buffering=0)
                break
            except Exception:
                time.sleep(0.05)

    def _mpv_cmd(self, *words):
        """Отправка JSON-команды в mpv (loadfile, set_property, stop, …)."""
        if IS_ANDROID:
            return
        if not getattr(self, "_mpv_io", None) or self._mpv_io.closed:
            try:
                self._mpv_io = open(self._mpv_pipe, "w+b", buffering=0)
            except Exception:
                return
        try:
            payload = (json.dumps({"command": list(words)}) + "\n").encode("utf-8")
            self._mpv_io.write(payload)
            self._mpv_io.flush()
        except Exception:
            try:
                self._mpv_io.close()
            except Exception:
                pass
            self._mpv_io = None

    @mainthread
    def _play_media_from_desktop(self, way, media_type):
        # ВСЕГДА работаем как «андроид»: Video/Image из Kivy
        path = os.path.expanduser(way)
        print(f"[MEDIA] play request: {path}")

        if not os.path.exists(path):
            print(f"[MEDIA] file not found: {path}")
            return

        # Сносим прежний виджет, чистим контейнер
        self._stop_current_media()
        self.media_box.clear_widgets()

        mtype = media_type or guess_media_type(path)

        if mtype == 'video':
            v = Video(source=path)
            # важные настройки, чтобы картинка не была пустой и занимала весь контейнер
            v.size_hint = (1, 1)
            v.allow_stretch = True
            v.keep_ratio = True
            v.eos = 'loop'  # корректный способ зациклить в Kivy

            # Небольшая телеметрия, чтобы видеть жизненный цикл
            def _on_state(inst, value):
                print(f"[MEDIA] video state -> {value}")
            def _on_eos(*_):
                print("[MEDIA] video EOS")

            v.bind(on_state=_on_state, on_eos=_on_eos)

            self.current_media = v
            self.media_box.add_widget(v)

            # Ключевой момент: стартуем ПOСЛЕ того, как виджет появился в дереве.
            # Иначе часто получаем «белый экран» (пустую текстуру).
            Clock.schedule_once(lambda dt: setattr(v, 'state', 'play'), 0)

            # Диагностика: если через секунду текстуры нет, подсказка в лог
            def _check_ready(dt):
                if v.texture is None:
                    print("[MEDIA] video has no texture yet — проверь кодек/путь/доступ. "
                        "Файл существует, но кадров нет.")
            Clock.schedule_once(_check_ready, 1.0)
            return

        if mtype == 'image':
            img = KivyImage(source=path, allow_stretch=True, keep_ratio=True, size_hint=(1, 1))
            self.current_media = img
            self.media_box.add_widget(img)
            print("[MEDIA] image shown")
            return

        print(f"[MEDIA] unknown media type for {path}")

    @mainthread
    def _stop_current_media(self, *args):
        cm = getattr(self, 'current_media', None)
        if not cm:
            return
        try:
            if isinstance(cm, Video):
                cm.state = 'stop'
                print("[MEDIA] video stopped")
        except Exception as e:
            print(f"[MEDIA] error while stopping video: {e}")
        try:
            if cm.parent is not None:
                cm.parent.remove_widget(cm)
        except Exception as e:
            print(f"[MEDIA] error while removing widget: {e}")
        self.current_media = None

    # Функции для корректного закрытия приложения
    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 27:  # Esc / Back
            try: 
                self._stop_current_media()
            except: 
                pass
            self.stop()
            return True
        return False

    def on_stop(self):
        # попросим mpv завершиться (на Android это no-op)
        try:
            self._mpv_cmd("quit")
        except Exception:
            pass
        p = getattr(self, "_mpv_proc", None)
        if p and p.poll() is None:
            try: p.terminate()
            except: pass

# Спец-переменная для того, чтобы программа срабатывала только при исполнении
if __name__ == "__main__":
    MyApp().run()