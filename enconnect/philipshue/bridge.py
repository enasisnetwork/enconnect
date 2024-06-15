"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from json import loads
from threading import Event as BlockEvent
from typing import Any
from typing import AsyncIterator
from typing import Iterator
from typing import Optional
from typing import TYPE_CHECKING

from httpx import Response

from ..utils import HTTPClient
from ..utils.http import _METHODS

if TYPE_CHECKING:
    from .params import BridgeParams

AsyncEvent = asyncio.Event



class Bridge:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'BridgeParams'
    __client: HTTPClient


    def __init__(
        self,
        params: 'BridgeParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params

        client = HTTPClient(
            timeout=params.timeout,
            verify=params.ssl_verify,
            capem=params.ssl_capem)

        self.__client = client


    @property
    def params(
        self,
    ) -> 'BridgeParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def client(
        self,
    ) -> HTTPClient:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client


    def request(
        self,
        method: _METHODS,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :returns: Response for upstream request to the server.
        """

        params = dict(params or {})
        json = dict(json or {})

        server = self.params.server
        token = self.params.token
        client = self.client

        token_key = 'hue-application-key'

        location = (
            f'https://{server}'
            f'/clip/v2/{path}')

        request = client.request_block

        return request(
            method=method,
            location=location,
            params=params,
            headers={token_key: token},
            json=json)


    def events_block(
        self,
        timeout: int = 60,
        cancel: Optional[BlockEvent] = None,
    ) -> Iterator[list[dict[str, Any]]]:
        """
        Return the response for upstream request to the server.

        :param timeout: Timeout when waiting for server response.
        :param cancel: Event used to indicate we should cacnel.
        """

        if cancel is None:
            cancel = BlockEvent()

        server = self.params.server
        token = self.params.token
        client = self.client

        accept = 'text/event-stream'
        token_key = 'hue-application-key'

        location = (
            f'https://{server}'
            f'/eventstream/clip/v2')

        request = client.stream_block


        stream = request(
            method='get',
            location=location,
            headers={
                'Accept': accept,
                token_key: token},
            timeout=timeout)


        for event in stream:

            if event is None:
                continue  # NOCVR

            event = event.strip()

            if event[0:5] != 'data:':
                continue

            yield loads(event[6:])

            if cancel.is_set():
                break  # NOCVR


    async def events_async(  # noqa: ASYNC900
        self,
        timeout: int = 60,  # noqa: ASYNC109
        cancel: Optional[AsyncEvent] = None,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """
        Return the response for upstream request to the server.

        :param timeout: Timeout when waiting for server response.
        :param cancel: Event used to indicate we should cacnel.
        """

        if cancel is None:
            cancel = AsyncEvent()

        server = self.params.server
        token = self.params.token
        client = self.client

        accept = 'text/event-stream'
        token_key = 'hue-application-key'

        location = (
            f'https://{server}'
            f'/eventstream/clip/v2')

        request = client.stream_async


        stream = request(
            method='get',
            location=location,
            headers={
                'Accept': accept,
                token_key: token},
            timeout=timeout)


        async for event in stream:

            if event is None:
                continue  # NOCVR

            event = event.strip()

            if event[0:5] != 'data:':
                continue

            yield loads(event[6:])

            if cancel.is_set():
                break  # NOCVR


        await asyncio.sleep(0)
