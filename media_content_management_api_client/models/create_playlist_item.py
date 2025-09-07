from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePlaylistItem")


@_attrs_define
class CreatePlaylistItem:
    """
    Attributes:
        media_file_id (int):
        order_index (int):
        display_duration (int):
        start_time (Union[Unset, str]):
        end_time (Union[Unset, str]):
        days_of_week (Union[Unset, list[int]]):
    """

    media_file_id: int
    order_index: int
    display_duration: int
    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    days_of_week: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        media_file_id = self.media_file_id

        order_index = self.order_index

        display_duration = self.display_duration

        start_time = self.start_time

        end_time = self.end_time

        days_of_week: Union[Unset, list[int]] = UNSET
        if not isinstance(self.days_of_week, Unset):
            days_of_week = self.days_of_week

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "media_file_id": media_file_id,
                "order_index": order_index,
                "display_duration": display_duration,
            }
        )
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if days_of_week is not UNSET:
            field_dict["days_of_week"] = days_of_week

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        media_file_id = d.pop("media_file_id")

        order_index = d.pop("order_index")

        display_duration = d.pop("display_duration")

        start_time = d.pop("start_time", UNSET)

        end_time = d.pop("end_time", UNSET)

        days_of_week = cast(list[int], d.pop("days_of_week", UNSET))

        create_playlist_item = cls(
            media_file_id=media_file_id,
            order_index=order_index,
            display_duration=display_duration,
            start_time=start_time,
            end_time=end_time,
            days_of_week=days_of_week,
        )

        create_playlist_item.additional_properties = d
        return create_playlist_item

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
