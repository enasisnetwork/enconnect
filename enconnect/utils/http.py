"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from time import sleep
from typing import Any
from typing import Literal
from typing import Optional

from httpx import AsyncClient
from httpx import Client as BlockClient
from httpx import Response
from httpx._types import VerifyTypes



_METHODS = Literal[
    'delete',
    'get',
    'patch',
    'put']



class HTTPClient:
    """
    Interact with the upstream server in blocking or async.

    :param timeout: Timeout when waiting for server response.
    :param verify: Require valid certificate from the server.
    :param capem: Optional path to the certificate authority.
    :param retry: How many attempts are made with the server.
    :param backoff: Backoff backoff if encountered retries.
    :param states: Which states will be retried with backoff.
    """

    __timeout: int
    __verify: VerifyTypes
    __capem: Optional[str]
    __retry: int
    __backoff: float
    __states: set[int]

    __client_block: BlockClient
    __client_async: AsyncClient


    def __init__(  # noqa: CFQ002
        self,
        timeout: int = 30,
        verify: VerifyTypes = True,
        capem: Optional[str] = None,
        retry: int = 3,
        backoff: float = 3.0,
        states: set[int] = {429},
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        timeout = int(timeout)
        retry = int(retry)
        backoff = float(backoff)
        states = set(states)

        client_block = BlockClient(
            timeout=timeout,
            verify=capem or verify,
            follow_redirects=True)

        client_async = AsyncClient(
            timeout=timeout,
            verify=capem or verify,
            follow_redirects=True)

        self.__timeout = timeout
        self.__verify = verify
        self.__capem = capem
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
    def verify(
        self,
    ) -> VerifyTypes:
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


    def request_block(
        self,
        method: _METHODS,
        location: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :returns: Response for upstream request to the server.
        """

        retry = self.retry
        backoff = self.backoff
        states = self.states

        client = self.client_block
        request = client.request

        for count in range(retry):

            response = request(
                method=method,
                url=location,
                params=params,
                json=json)

            status = response.status_code

            if status not in states:
                break

            sleep(backoff)

        return response


    async def request_async(
        self,
        method: _METHODS,
        location: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param location: Location with path for server request.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :returns: Response for upstream request to the server.
        """

        retry = self.retry
        backoff = self.backoff
        states = self.states

        client = self.client_async
        request = client.request

        for count in range(retry):

            response = await request(
                method=method,
                url=location,
                params=params,
                json=json)

            status = response.status_code

            if status not in states:
                break

            await asyncio.sleep(backoff)

        await asyncio.sleep(0)

        return response
