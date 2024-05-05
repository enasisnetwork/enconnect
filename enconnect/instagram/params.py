"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from pydantic import BaseModel



class InstagramParams(BaseModel, extra='forbid'):
    """
    Process and validate the class configuration parameters.

    :param timeout: Timeout when waiting for server response.
    :param token: Token used when authenticating to server.
    :param ssl_verify: Require valid certificate from server.
    :param ssl_capem: Optional path to certificate authority.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    timeout: int = 30

    token: str

    ssl_verify: bool = True
    ssl_capem: Optional[str] = None
