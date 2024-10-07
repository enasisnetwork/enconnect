"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional

from encommon.types import BaseModel

from pydantic import Field



class ClientParams(BaseModel, extra='forbid'):
    """
    Process and validate the class configuration parameters.
    """

    server: Annotated[
        str,
        Field(...,
              description='Server address for connection',
              min_length=1)]

    port: Annotated[
        int,
        Field(6697,
              description='Server address for connection',
              ge=1, le=65535)]

    timeout: Annotated[
        int,
        Field(30,
              description='Timeout connecting to server',
              ge=1, le=300)]

    operate: Annotated[
        Literal['normal', 'service'],
        Field('normal',
              description='Method for server connection')]

    nickname: Annotated[
        str,
        Field('ircbot',
              description='Parameter for the integration',
              min_length=1)]

    username: Annotated[
        str,
        Field('ircbot',
              description='Parameter for the integration',
              min_length=1)]

    realname: Annotated[
        str,
        Field('Chatting Robie',
              description='Parameter for the integration',
              min_length=1)]

    password: Annotated[
        Optional[str],
        Field(None,
              description='Parameter for the integration',
              min_length=1)]

    servername: Annotated[
        str,
        Field('services.invalid',
              description='Parameter for the integration',
              min_length=1)]

    serverid: Annotated[
        str,
        Field('42X',
              description='Unique identifier for services',
              min_length=1)]

    ssl_enable: Annotated[
        bool,
        Field(True,
              description='Enable connection encryption')]

    ssl_verify: Annotated[
        bool,
        Field(True,
              description='Verify the ceritifcate valid')]

    queue_size: Annotated[
        int,
        Field(10000,
              description='Maximum size for queued events',
              ge=1000, le=1000000)]


    def __init__(
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)
