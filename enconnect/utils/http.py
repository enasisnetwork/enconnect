"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from copy import deepcopy
from ssl import SSLContext
from time import sleep
from typing import AsyncIterator
from typing import Iterator
from typing import Literal
from typing import Optional

from encommon.types import DictStrAny

from httpx import AsyncClient
from httpx import Client as BlockClient
from httpx import Response
from httpx._client import UseClientDefault



_METHODS = Literal[
    'delete',
    'get',
    'post',
    'patch',
    'put']

_HTTPAUTH = tuple[str, str]

_HEADERS = dict[str, str]

_PAYLOAD = DictStrAny

_VERIFY = SSLContext | str | bool



class HTTPClient:
    """
    Interact with the upstream server in blocking or async.

    :param timeout: Timeout waiting for the server response.
    :param headers: Optional headers to include in requests.
    :param verify: Require valid certificate from the server.
    :param capem: Optional path to the certificate authority.
    :param httpauth: Optional information for authentication.
    :param retry: How many attempts are made with the server.
    :param backoff: Backoff backoff if encountered retries.
    :param states: Which states will be retried with backoff.
    """

    __timeout: int
    __headers: Optional[_HEADERS]
    __verify: _VERIFY
    __capem: Optional[str]
    __httpauth: Optional[_HTTPAUTH]
    __retry: int
    __backoff: float
    __states: set[int]

    __client_block: BlockClient
    __client_async: AsyncClient


    def __init__(  # noqa: CFQ002
        self,
        timeout: int = 30,
        headers: Optional[_HEADERS] = None,
        verify: _VERIFY = True,
        capem: Optional[str] = None,
        httpauth: Optional[_HTTPAUTH] = None,
        retry: int = 3,
        backoff: float = 3.0,
        states: set[int] = {429},
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        timeout = int(timeout)
        headers = deepcopy(headers)
        httpauth = deepcopy(httpauth)
        retry = int(retry)
        backoff = float(backoff)
        states = set(states)

        client_block = BlockClient(
            timeout=timeout,
            headers=headers or None,
            auth=httpauth or None,
            verify=capem or verify,
            follow_redirects=True)

        client_async = AsyncClient(
            timeout=timeout,
            headers=headers or None,
            auth=httpauth or None,
            verify=capem or verify,
            follow_redirects=True)

        self.__timeout = timeout
        self.__headers = headers
        self.__verify = verify
        self.__capem = capem
        self.__httpauth = httpauth
        self.__retry = retry
        self.__backoff = backoff
        self.__states = states

        self.__client_block = client_block
        self.__client_async = client_async


    @property
    def timeout(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__timeout


    @property
    def httpauth(
        self,
    ) -> Optional[_HTTPAUTH]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return deepcopy(self.__httpauth)


    @property
    def headers(
        self,
    ) -> Optional[_HEADERS]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return deepcopy(self.__headers)


    @property
    def verify(
        self,
    ) -> _VERIFY:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__verify


    @property
    def capem(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__capem


    @property
    def retry(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__retry


    @property
    def backoff(
        self,
    ) -> float:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__backoff


    @property
    def states(
        self,
    ) -> set[int]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__states


    @property
    def client_block(
        self,
    ) -> BlockClient:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client_block


    @property
    def client_async(
        self,
    ) -> AsyncClient:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__client_async


    def request_block(  # noqa: CFQ002
        self,
        method: _METHODS,
        location: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        data: Optional[_PAYLOAD] = None,
        files: Optional[_PAYLOAD] = None,
        timeout: Optional[int] = None,
        headers: Optional[_HEADERS] = None,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param data: Optional dict payload included in request.
        :param files: Optional file payload included in request.
        :param timeout: Timeout waiting for the server response.
        :param headers: Optional headers to include in requests.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        retry = self.__retry
        backoff = self.__backoff
        states = self.__states

        default = UseClientDefault()

        client = self.__client_block
        request = client.request


        for count in range(retry):

            response = request(
                method=method,
                url=location,
                headers=headers or None,
                auth=httpauth or default,
                timeout=timeout or default,
                params=params or None,
                data=data or None,
                files=files or None,
                json=json or None)

            status = response.status_code

            if status not in states:
                break

            sleep(backoff)


        return response


    async def request_async(  # noqa: CFQ002
        self,
        method: _METHODS,
        location: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        data: Optional[_PAYLOAD] = None,
        files: Optional[_PAYLOAD] = None,
        timeout: Optional[int] = None,
        headers: Optional[_HEADERS] = None,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param data: Optional dict payload included in request.
        :param files: Optional file payload included in request.
        :param timeout: Timeout waiting for the server response.
        :param headers: Optional headers to include in requests.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        retry = self.__retry
        backoff = self.__backoff
        states = self.__states

        default = UseClientDefault()

        client = self.__client_async
        request = client.request


        for count in range(retry):

            response = await request(
                method=method,
                url=location,
                headers=headers or None,
                auth=httpauth or default,
                timeout=timeout or default,
                params=params or None,
                data=data or None,
                files=files or None,
                json=json or None)

            status = response.status_code

            if status not in states:
                break

            await asyncio.sleep(backoff)


        await asyncio.sleep(0)

        return response


    def stream_block(  # noqa: CFQ002
        self,
        method: _METHODS,
        location: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        data: Optional[_PAYLOAD] = None,
        timeout: Optional[int] = None,
        headers: Optional[_HEADERS] = None,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> Iterator[str]:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param data: Optional dict payload included in request.
        :param timeout: Timeout waiting for the server response.
        :param headers: Optional headers to include in requests.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        default = UseClientDefault()

        client = self.__client_block
        request = client.stream


        stream = request(
            method=method,
            url=location,
            headers=headers or None,
            auth=httpauth or default,
            timeout=timeout or default,
            params=params or None,
            data=data or None,
            json=json or None)


        with stream as _stream:

            lines = (
                _stream.iter_lines())

            yield from lines


    async def stream_async(  # noqa: CFQ002
        self,
        method: _METHODS,
        location: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        data: Optional[_PAYLOAD] = None,
        timeout: Optional[int] = None,
        headers: Optional[_HEADERS] = None,
        httpauth: Optional[_HTTPAUTH] = None,
    ) -> AsyncIterator[str]:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param data: Optional dict payload included in request.
        :param timeout: Timeout waiting for the server response.
        :param headers: Optional headers to include in requests.
        :param httpauth: Optional information for authentication.
        :returns: Response from upstream request to the server.
        """

        default = UseClientDefault()

        client = self.__client_async
        request = client.stream


        stream = request(
            method=method,
            url=location,
            headers=headers or None,
            auth=httpauth or default,
            timeout=timeout or default,
            params=params or None,
            data=data or None,
            json=json or None)


        async with stream as _stream:

            lines = (
                _stream.aiter_lines())

            async for line in lines:
                yield line
