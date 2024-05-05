"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from requests import Response
from requests import Session

if TYPE_CHECKING:
    from .params import RouterParams



class Router:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'RouterParams'
    __session: Session


    def __init__(
        self,
        params: 'RouterParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params
        self.__session = Session()


    @property
    def params(
        self,
    ) -> 'RouterParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def session(
        self,
    ) -> Session:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__session


    def request_cookie(
        self,
    ) -> Response:
        """
        Establish new session obtaining cookie for authorization.

        :returns: Response for upstream request to the server.
        """

        params = self.params
        username = params.username
        password = params.password

        payload = {
            'username': username,
            'password': password}

        response = self.request(
            method='post',
            path='api/auth/login',
            json=payload)

        response.raise_for_status()

        return response


    def request(
        self,
        method: str,
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

        request = self.session.request

        server = self.params.server
        verify = self.params.ssl_verify
        capem = self.params.ssl_capem

        location = (
            f'https://{server}/{path}')

        return request(
            method=method,
            url=location,
            timeout=self.params.timeout,
            params=params,
            json=json,
            verify=capem or verify)


    def request_proxy(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        .. note::
           Most endpoints on Ubiquiti routers are prefixed with
           not only the site but also `/proxy/network/api`. The
           method will handle concatenating the values for you.
           It will also handle authenticating if not already.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :returns: Response for upstream request to the server.
        """

        site = self.params.site

        path = (
            'proxy/network/api'
            f'/s/{site}/{path}')


        def _request() -> Response:

            return self.request(
                method, path,
                params, json)


        response = _request()

        if response.status_code == 401:

            self.request_cookie()

            response = _request()

        response.raise_for_status()


        return response
