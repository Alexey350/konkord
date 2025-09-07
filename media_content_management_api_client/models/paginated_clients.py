from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.client import Client


T = TypeVar("T", bound="PaginatedClients")


@_attrs_define
class PaginatedClients:
    """
    Attributes:
        data (Union[Unset, list['Client']]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        total (Union[Unset, int]):
        total_pages (Union[Unset, int]):
    """

    data: Union[Unset, list["Client"]] = UNSET
    page: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        page = self.page

        limit = self.limit

        total = self.total

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.client import Client

        d = dict(src_dict)
        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = Client.from_dict(data_item_data)

            data.append(data_item)

        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        total = d.pop("total", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        paginated_clients = cls(
            data=data,
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        )

        paginated_clients.additional_properties = d
        return paginated_clients

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
