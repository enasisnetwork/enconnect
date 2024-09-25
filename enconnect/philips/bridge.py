"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from json import loads
from typing import AsyncIterator
from typing import Iterator
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import DictStrAny

from httpx import Response

from ..utils import HTTPClient
from ..utils.http import _METHODS
from ..utils.http import _PAYLOAD

if TYPE_CHECKING:
    from .params import BridgeParams



class Bridge:
    """
    Interact with the local service API with various methods.

    :param params: Parameters used to instantiate the class.
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
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        timeout: Optional[int] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param timeout: Timeout waiting for the server response.
            This will override the default client instantiated.
        :returns: Response from upstream request to the server.
        """

        params = dict(params or {})
        json = dict(json or {})

        _params = self.__params
        server = _params.server
        token = _params.token

        client = self.__client

        tokey = 'hue-application-key'

        headers = {tokey: token}

        location = (
            f'https://{server}'
            f'/clip/v2/{path}')

        request = client.request_block

        return request(
            method=method,
            location=location,
            params=params,
            headers=headers,
            json=json)


    def events_block(
        self,
        timeout: Optional[int] = None,
    ) -> Iterator[DictStrAny]:
        """
        Return the response for upstream request to the server.

        :param timeout: Timeout waiting for the server response.
            This will override the default client instantiated.
        """

        _params = self.__params
        server = _params.server
        token = _params.token

        client = self.__client

        accept = 'text/event-stream'
        tokey = 'hue-application-key'

        headers = {
            'Accept': accept,
            tokey: token}

        location = (
            f'https://{server}'
            f'/eventstream/clip/v2')

        request = client.stream_block


        stream = request(
            method='get',
            location=location,
            headers=headers,
            timeout=timeout)


        for event in stream:

            if event is None:
                continue  # NOCVR

            event = event.strip()

            if event[0:5] != 'data:':
                continue

            loaded = loads(event[6:])

            for _event in loaded:

                events = _event['data']

                yield from events


    async def events_async(
        self,
        timeout: Optional[int] = None,
    ) -> AsyncIterator[DictStrAny]:
        """
        Return the response for upstream request to the server.

        :param timeout: Timeout waiting for the server response.
            This will override the default client instantiated.
        """

        _params = self.__params
        server = _params.server
        token = _params.token

        client = self.__client

        accept = 'text/event-stream'
        tokey = 'hue-application-key'

        headers = {
            'Accept': accept,
            tokey: token}

        location = (
            f'https://{server}'
            f'/eventstream/clip/v2')

        request = client.stream_async


        stream = request(
            method='get',
            location=location,
            headers=headers,
            timeout=timeout)


        async for event in stream:

            if event is None:
                continue  # NOCVR

            event = event.strip()

            if event[0:5] != 'data:':
                continue

            loaded = loads(event[6:])

            for _event in loaded:

                events = _event['data']

                for event in events:

                    assert isinstance(event, dict)

                    yield event

                    await asyncio.sleep(0)


        await asyncio.sleep(0)
