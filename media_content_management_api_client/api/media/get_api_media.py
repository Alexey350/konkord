from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_media import PaginatedMedia
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    type_: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["type"] = type_

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/media",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PaginatedMedia]:
    if response.status_code == 200:
        response_200 = PaginatedMedia.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PaginatedMedia]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    type_: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Response[PaginatedMedia]:
    """List media files

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        type_ (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedMedia]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        type_=type_,
        search=search,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    type_: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Optional[PaginatedMedia]:
    """List media files

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        type_ (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedMedia
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        type_=type_,
        search=search,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    type_: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Response[PaginatedMedia]:
    """List media files

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        type_ (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedMedia]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        type_=type_,
        search=search,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    type_: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Optional[PaginatedMedia]:
    """List media files

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        type_ (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedMedia
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            type_=type_,
            search=search,
        )
    ).parsed
