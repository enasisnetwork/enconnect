"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from typing import Annotated
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import BaseModel
from encommon.types import DictStrAny

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

    data: Annotated[
        Optional[DictStrAny],
        Field(None,
              description='Payload with the event data',
              min_length=1)]

    broadcast: Annotated[
        Optional[DictStrAny],
        Field(None,
              description='Payload with the event data',
              min_length=1)]

    seqno: Annotated[
        Optional[int],
        Field(None,
              description='Event number within squence',
              ge=0)]

    status: Annotated[
        Optional[str],
        Field(None,
              description='Type of event that occurred',
              min_length=1)]

    error: Annotated[
        Optional[DictStrAny],
        Field(None,
              description='Payload with the event data',
              min_length=1)]

    seqre: Annotated[
        Optional[int],
        Field(None,
              description='Reply number within squence',
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
        Optional[str],
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


        type = event.get('event')
        _data = event.get('data')
        bcast = event.get('broadcast')
        seqno = event.get('seq')

        status = event.get('status')
        seqre = event.get('seq_reply')
        error = event.get('error')


        if type is not None:
            data['type'] = type

        if _data is not None:
            data['data'] = _data

        if bcast is not None:
            data['broadcast'] = bcast

        if seqno is not None:
            data['seqno'] = seqno

        if status is not None:
            data['status'] = status

        if error is not None:
            data['error'] = error

        if seqre is not None:
            data['seqre'] = seqre


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


        if type == 'posted':

            assert data is not None

            _type = data[
                'channel_type']

            kind = (
                'privmsg'
                if _type == 'D'
                else 'chanmsg')


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

        post = loads(data['post'])

        unique = post['user_id']
        name = data['sender_name']

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

        post = loads(data['post'])

        channel = post['channel_id']

        self.recipient = channel


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

        post = loads(data['post'])

        message = post['message']

        self.message = message


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
