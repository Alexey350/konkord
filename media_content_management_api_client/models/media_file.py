import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="MediaFile")


@_attrs_define
class MediaFile:
    """
    Attributes:
        id (Union[Unset, int]):
        filename (Union[Unset, str]):
        original_name (Union[Unset, str]):
        file_path (Union[Unset, str]):
        mime_type (Union[Unset, str]):
        file_size (Union[Unset, int]):
        duration (Union[Unset, int]):
        width (Union[Unset, int]):
        height (Union[Unset, int]):
        checksum (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, int] = UNSET
    filename: Union[Unset, str] = UNSET
    original_name: Union[Unset, str] = UNSET
    file_path: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    file_size: Union[Unset, int] = UNSET
    duration: Union[Unset, int] = UNSET
    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    checksum: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        filename = self.filename

        original_name = self.original_name

        file_path = self.file_path

        mime_type = self.mime_type

        file_size = self.file_size

        duration = self.duration

        width = self.width

        height = self.height

        checksum = self.checksum

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if filename is not UNSET:
            field_dict["filename"] = filename
        if original_name is not UNSET:
            field_dict["original_name"] = original_name
        if file_path is not UNSET:
            field_dict["file_path"] = file_path
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type
        if file_size is not UNSET:
            field_dict["file_size"] = file_size
        if duration is not UNSET:
            field_dict["duration"] = duration
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height
        if checksum is not UNSET:
            field_dict["checksum"] = checksum
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        filename = d.pop("filename", UNSET)

        original_name = d.pop("original_name", UNSET)

        file_path = d.pop("file_path", UNSET)

        mime_type = d.pop("mime_type", UNSET)

        file_size = d.pop("file_size", UNSET)

        duration = d.pop("duration", UNSET)

        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        checksum = d.pop("checksum", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        media_file = cls(
            id=id,
            filename=filename,
            original_name=original_name,
            file_path=file_path,
            mime_type=mime_type,
            file_size=file_size,
            duration=duration,
            width=width,
            height=height,
            checksum=checksum,
            created_at=created_at,
        )

        media_file.additional_properties = d
        return media_file

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
