import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaylistUpdate")


@_attrs_define
class PlaylistUpdate:
    """
    Attributes:
        id (Union[Unset, int]):
        playlist_id (Union[Unset, int]):
        client_id (Union[Unset, int]):
        update_type (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    playlist_id: Union[Unset, int] = UNSET
    client_id: Union[Unset, int] = UNSET
    update_type: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        playlist_id = self.playlist_id

        client_id = self.client_id

        update_type = self.update_type

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if playlist_id is not UNSET:
            field_dict["playlist_id"] = playlist_id
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if update_type is not UNSET:
            field_dict["update_type"] = update_type
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        playlist_id = d.pop("playlist_id", UNSET)

        client_id = d.pop("client_id", UNSET)

        update_type = d.pop("update_type", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        playlist_update = cls(
            id=id,
            playlist_id=playlist_id,
            client_id=client_id,
            update_type=update_type,
            created_at=created_at,
        )

        playlist_update.additional_properties = d
        return playlist_update

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
