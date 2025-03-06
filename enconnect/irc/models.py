"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import IGNORECASE
from re import compile
from re import escape as re_escape
from re import match as re_match
from re import search as re_search
from typing import Annotated
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import BaseModel
from encommon.types import DictStrAny
from encommon.types import NCTrue

from pydantic import Field

if TYPE_CHECKING:
    from .client import Client



EVENT = compile(
    r'^(?::(?P<prefix>[^\s]+)\s)?'
    r'(?P<command>[A-Z0-9]{3,})\s'
    r'(?P<params>.+)$')

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

    prefix: Annotated[
        Optional[str],
        Field(None,
              description='Prefix or origin information',
              min_length=1)]

    command: Annotated[
        Optional[str],
        Field(None,
              description='Code or command for the event',
              min_length=1)]

    params: Annotated[
        Optional[str],
        Field(None,
              description='Event or command parameters')]

    original: Annotated[
        str,
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

    hasme: Annotated[
        bool,
        Field(False,
              description='Indicates message mentions client')]

    whome: Annotated[
        Optional[str],
        Field(None,
              description='Current nickname of when received',
              min_length=1)]

    author: Annotated[
        Optional[str],
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
        event: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data: DictStrAny = {
            'original': event}

        operate = (
            client.params
            .operate)


        match = re_match(
            EVENT, event)

        if (operate == 'normal'
                and match is not None):

            prefix = (
                match
                .group('prefix'))

            if prefix is not None:
                data['prefix'] = (
                    prefix.strip())

            command = (
                match
                .group('command'))

            if command is not None:
                data['command'] = (
                    command.strip())

            params = (
                match
                .group('params'))

            if params is not None:
                data['params'] = (
                    params.strip())


        super().__init__(**data)

        self.__set_kind()
        self.__set_author()
        self.__set_recipient()
        self.__set_message()
        self.__set_isme(client)
        self.__set_hasme(client)
        self.__set_whome(client)


    def __set_kind(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        command = self.command
        params = self.params

        kind: KINDS = 'event'


        if command == 'PRIVMSG':

            assert params is not None

            prefix = params[0][:1]

            kind = (
                'chanmsg'
                if prefix in '#&+!'
                else 'privmsg')


        self.kind = kind


    def __set_author(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        prefix = self.prefix

        if kind not in MESSAGE:
            return None

        assert prefix is not None

        author = prefix.split(
            '!', maxsplit=1)

        self.author = author[0]


    def __set_recipient(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        params = self.params

        if (kind not in MESSAGE
                or not params):
            return None

        split = params.split(' ')

        self.recipient = split[0]


    def __set_message(
        self,
    ) -> None:
        """
        Update the value for the attribute from class instance.
        """

        kind = self.kind
        params = self.params

        if (kind not in MESSAGE
                or not params):
            return None

        message = (
            params
            .split(':', maxsplit=1))

        self.message = message[1]


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
        event = self.original

        operate = (
            client.params
            .operate)

        isme: bool = False


        if operate == 'service':

            prefix = f':{mynick} '

            if event.startswith(prefix):
                isme = True


        elif mynick and author:

            mine = mynick
            them = author

            isme = mine == them


        elif operate == 'normal':

            prefix = f':{mynick}!'

            if event.startswith(prefix):
                isme = NCTrue

            prefix = f':{mynick} '

            if event.startswith(prefix):
                isme = NCTrue


        self.isme = isme


    def __set_hasme(
        self,
        client: 'Client',
    ) -> None:
        """
        Update the value for the attribute from class instance.

        :param client: Class instance for connecting to service.
        """

        mynick = client.nickname
        message = self.message

        if mynick is None:
            return None

        if message is None:
            return None

        needle = re_escape(mynick)
        pattern = rf'\b@?{needle}\b'

        results = bool(
            re_search(
                pattern,
                message,
                IGNORECASE))

        self.hasme = results


    def __set_whome(
        self,
        client: 'Client',
    ) -> None:
        """
        Update the value for the attribute from class instance.

        :param client: Class instance for connecting to service.
        """

        self.whome = client.nickname
