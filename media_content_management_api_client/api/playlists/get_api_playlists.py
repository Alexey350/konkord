from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_playlists import PaginatedPlaylists
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    active: Union[Unset, bool] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_items: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["active"] = active

    params["search"] = search

    params["include_items"] = include_items

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/playlists",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PaginatedPlaylists]:
    if response.status_code == 200:
        response_200 = PaginatedPlaylists.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PaginatedPlaylists]:
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
    active: Union[Unset, bool] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_items: Union[Unset, bool] = UNSET,
) -> Response[PaginatedPlaylists]:
    """Get playlists (pagination/filtering)

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        active (Union[Unset, bool]):
        search (Union[Unset, str]):
        include_items (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedPlaylists]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        active=active,
        search=search,
        include_items=include_items,
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
    active: Union[Unset, bool] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_items: Union[Unset, bool] = UNSET,
) -> Optional[PaginatedPlaylists]:
    """Get playlists (pagination/filtering)

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        active (Union[Unset, bool]):
        search (Union[Unset, str]):
        include_items (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedPlaylists
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        active=active,
        search=search,
        include_items=include_items,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    active: Union[Unset, bool] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_items: Union[Unset, bool] = UNSET,
) -> Response[PaginatedPlaylists]:
    """Get playlists (pagination/filtering)

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        active (Union[Unset, bool]):
        search (Union[Unset, str]):
        include_items (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedPlaylists]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        active=active,
        search=search,
        include_items=include_items,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    active: Union[Unset, bool] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_items: Union[Unset, bool] = UNSET,
) -> Optional[PaginatedPlaylists]:
    """Get playlists (pagination/filtering)

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        active (Union[Unset, bool]):
        search (Union[Unset, str]):
        include_items (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedPlaylists
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            active=active,
            search=search,
            include_items=include_items,
        )
    ).parsed
