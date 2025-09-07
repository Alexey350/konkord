import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_updates_response_200 import GetApiUpdatesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client_id: str,
    last_check: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["client_id"] = client_id

    json_last_check: Union[Unset, str] = UNSET
    if not isinstance(last_check, Unset):
        json_last_check = last_check.isoformat()
    params["last_check"] = json_last_check

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/updates",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetApiUpdatesResponse200]:
    if response.status_code == 200:
        response_200 = GetApiUpdatesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetApiUpdatesResponse200]:
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
    last_check: Union[Unset, datetime.datetime] = UNSET,
) -> Response[GetApiUpdatesResponse200]:
    """Get update log for client (playlist changes)

    Args:
        client_id (str):
        last_check (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiUpdatesResponse200]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        last_check=last_check,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    last_check: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[GetApiUpdatesResponse200]:
    """Get update log for client (playlist changes)

    Args:
        client_id (str):
        last_check (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiUpdatesResponse200
    """

    return sync_detailed(
        client=client,
        client_id=client_id,
        last_check=last_check,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    last_check: Union[Unset, datetime.datetime] = UNSET,
) -> Response[GetApiUpdatesResponse200]:
    """Get update log for client (playlist changes)

    Args:
        client_id (str):
        last_check (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetApiUpdatesResponse200]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        last_check=last_check,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    last_check: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[GetApiUpdatesResponse200]:
    """Get update log for client (playlist changes)

    Args:
        client_id (str):
        last_check (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetApiUpdatesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            client_id=client_id,
            last_check=last_check,
        )
    ).parsed
