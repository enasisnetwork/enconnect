"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import BaseModel
from encommon.types import DictStrAny
from encommon.types import NCNone

from pydantic import Field

if TYPE_CHECKING:
    from .client import Client



KINDS = Literal[
    'event',
    'chanmsg',
    'privmsg']

MESSAGE = [
    'chanmsg',
    'privmsg']



class ClientEvent(BaseModel, extra='ignore'):
    """
    Contains information returned from the upstream server.
    """

    type: Annotated[
        Optional[str],
        Field(None,
              description='Type of event that occurred',
              min_length=1)]

    opcode: Annotated[
        int,
        Field(...,
              description='Type of operation performed',
              ge=0)]

    data: Annotated[
        Optional[DictStrAny],
        Field(None,
              description='Payload with the event data',
              min_length=1)]

    seqno: Annotated[
        Optional[int],
        Field(None,
              description='Event number within squence',
              ge=0)]

    original: Annotated[
        DictStrAny,
        Field(...,
              description='Original received from server',
              min_length=1)]

    kind: Annotated[
        KINDS,
        Field('event',
              description='Dynamic field parsed from event')]

    isme: Annotated[
        bool,
        Field(False,
              description='Indicates message is from client')]

    author: Annotated[
        Optional[tuple[str, str]],
        Field(None,
              description='Dynamic field parsed from event',
              min_length=1)]

    recipient: Annotated[
        Optional[tuple[Optional[str], str]],
        Field(None,
              description='Dynamic field parsed from event',
              min_length=1)]

    message: Annotated[
        Optional[str],
        Field(None,
              description='Dynamic field parsed from event',
              min_length=1)]


    def __init__(
        self,
        /,
        client: 'Client',
        event: DictStrAny,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data: DictStrAny = {
            'original': event}


        type = event.get('t')
        opcode = event.get('op')
        _data = event.get('d')
        seqno = event.get('s')


        if type is not None:
            data['type'] = type

        if opcode is not None:
            data['opcode'] = opcode

        if (isinstance(_data, dict)
                and len(_data) >= 1):
            data['data'] = _data

        if seqno is not None:
            data['seqno'] = seqno


        super().__init__(**data)

        self.__set_kind()
        self.__set_author()
        self.__set_recipient()
        self.__set_message()
        self.__set_isme(client)


    def __set_kind(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        type = self.type
        data = self.data

        kind: KINDS = 'event'


        message = [
            'MESSAGE_CREATE',
            'MESSAGE_UPDATE']

        if type in message:

            assert data is not None

            guild = (
                data.get('guild_id'))

            kind = (
                'chanmsg'
                if guild is not None
                else 'privmsg')


        self.kind = kind


    def __set_author(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        data = self.data

        if (kind not in MESSAGE
                or not data):
            return None

        dscuser = (
            data.get('author'))

        if dscuser is None:
            return NCNone

        unique = dscuser['id']
        name = dscuser['username']

        self.author = (
            name, unique)


    def __set_recipient(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        data = self.data

        if (kind not in MESSAGE
                or not data):
            return None

        guild = (
            data.get('guild_id'))

        channel = (
            data.get('channel_id'))

        if channel is None:
            return NCNone

        self.recipient = (
            guild, channel)


    def __set_message(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        data = self.data

        if (kind not in MESSAGE
                or not data):
            return None

        content = (
            data.get('content'))

        self.message = content


    def __set_isme(
        self,
        client: 'Client',
    ) -> None:
        """
        Update the value for the attribute from class instance.

        :param client: Class instance for connecting to service.
        """

        mynick = client.nickname
        author = self.author

        isme: bool = False

        if mynick and author:

            mine = mynick[1]
            them = author[1]

            isme = mine == them

        self.isme = isme
