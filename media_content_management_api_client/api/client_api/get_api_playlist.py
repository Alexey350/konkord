from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.playlist import Playlist
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client_id: str,
    name: str,
    version: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["client_id"] = client_id

    params["name"] = name

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/playlist",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Playlist]:
    if response.status_code == 200:
        response_200 = Playlist.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Playlist]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    name: str,
    version: Union[Unset, int] = UNSET,
) -> Response[Playlist]:
    """Get assigned playlist for client by name/version

    Args:
        client_id (str):
        name (str):
        version (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Playlist]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        name=name,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    name: str,
    version: Union[Unset, int] = UNSET,
) -> Optional[Playlist]:
    """Get assigned playlist for client by name/version

    Args:
        client_id (str):
        name (str):
        version (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Playlist
    """

    return sync_detailed(
        client=client,
        client_id=client_id,
        name=name,
        version=version,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    name: str,
    version: Union[Unset, int] = UNSET,
) -> Response[Playlist]:
    """Get assigned playlist for client by name/version

    Args:
        client_id (str):
        name (str):
        version (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Playlist]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        name=name,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    name: str,
    version: Union[Unset, int] = UNSET,
) -> Optional[Playlist]:
    """Get assigned playlist for client by name/version

    Args:
        client_id (str):
        name (str):
        version (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Playlist
    """

    return (
        await asyncio_detailed(
            client=client,
            client_id=client_id,
            name=name,
            version=version,
        )
    ).parsed
