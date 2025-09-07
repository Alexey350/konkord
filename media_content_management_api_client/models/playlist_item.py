import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media_file import MediaFile


T = TypeVar("T", bound="PlaylistItem")


@_attrs_define
class PlaylistItem:
    """
    Attributes:
        id (Union[Unset, int]):
        playlist_id (Union[Unset, int]):
        media_file_id (Union[Unset, int]):
        order_index (Union[Unset, int]):
        display_duration (Union[Unset, int]):
        start_time (Union[Unset, str]):
        end_time (Union[Unset, str]):
        days_of_week (Union[Unset, list[int]]):
        created_at (Union[Unset, datetime.datetime]):
        media_file (Union[Unset, MediaFile]):
    """

    id: Union[Unset, int] = UNSET
    playlist_id: Union[Unset, int] = UNSET
    media_file_id: Union[Unset, int] = UNSET
    order_index: Union[Unset, int] = UNSET
    display_duration: Union[Unset, int] = UNSET
    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    days_of_week: Union[Unset, list[int]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    media_file: Union[Unset, "MediaFile"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        playlist_id = self.playlist_id

        media_file_id = self.media_file_id

        order_index = self.order_index

        display_duration = self.display_duration

        start_time = self.start_time

        end_time = self.end_time

        days_of_week: Union[Unset, list[int]] = UNSET
        if not isinstance(self.days_of_week, Unset):
            days_of_week = self.days_of_week

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        media_file: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.media_file, Unset):
            media_file = self.media_file.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if playlist_id is not UNSET:
            field_dict["playlist_id"] = playlist_id
        if media_file_id is not UNSET:
            field_dict["media_file_id"] = media_file_id
        if order_index is not UNSET:
            field_dict["order_index"] = order_index
        if display_duration is not UNSET:
            field_dict["display_duration"] = display_duration
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if days_of_week is not UNSET:
            field_dict["days_of_week"] = days_of_week
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if media_file is not UNSET:
            field_dict["media_file"] = media_file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media_file import MediaFile

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        playlist_id = d.pop("playlist_id", UNSET)

        media_file_id = d.pop("media_file_id", UNSET)

        order_index = d.pop("order_index", UNSET)

        display_duration = d.pop("display_duration", UNSET)

        start_time = d.pop("start_time", UNSET)

        end_time = d.pop("end_time", UNSET)

        days_of_week = cast(list[int], d.pop("days_of_week", UNSET))

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _media_file = d.pop("media_file", UNSET)
        media_file: Union[Unset, MediaFile]
        if isinstance(_media_file, Unset):
            media_file = UNSET
        else:
            media_file = MediaFile.from_dict(_media_file)

        playlist_item = cls(
            id=id,
            playlist_id=playlist_id,
            media_file_id=media_file_id,
            order_index=order_index,
            display_duration=display_duration,
            start_time=start_time,
            end_time=end_time,
            days_of_week=days_of_week,
            created_at=created_at,
            media_file=media_file,
        )

        playlist_item.additional_properties = d
        return playlist_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
