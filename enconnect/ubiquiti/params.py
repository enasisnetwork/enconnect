"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from pydantic import BaseModel



class RouterParams(BaseModel, extra='forbid'):
    """
    Process and validate the class configuration parameters.

    :param server: Host or IP address for server connection.
    :param timeout: Timeout when waiting for server response.
    :param username: Username for authenticating with server.
    :param password: Password for authenticating with server.
    :param site: Optional site name to select within router.
    :param ssl_verify: Require valid certificate from server.
    :param ssl_capem: Optional path to certificate authority.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    server: str
    timeout: int = 30

    username: str
    password: str
    site: str = 'default'

    ssl_verify: bool = True
    ssl_capem: Optional[str] = None
