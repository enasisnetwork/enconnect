"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from requests import Response
from requests import request

if TYPE_CHECKING:
    from .params import BridgeParams



class Bridge:
    """
    Interact with the cloud service API with various methods.

    :param params: Parameters for instantiating the instance.
    """

    __params: 'BridgeParams'


    def __init__(
        self,
        params: 'BridgeParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params


    @property
    def params(
        self,
    ) -> 'BridgeParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


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

        server = self.params.server
        token = self.params.token
        verify = self.params.ssl_verify
        capem = self.params.ssl_capem

        token_key = 'hue-application-key'

        location = (
            f'https://{server}'
            f'/clip/v2/{path}')

        return request(
            method=method,
            url=location,
            timeout=self.params.timeout,
            params=params,
            json=json,
            headers={token_key: token},
            verify=capem or verify)
