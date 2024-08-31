"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import compile
from re import match as re_match
from typing import Annotated
from typing import Literal
from typing import Optional

from encommon.types import BaseModel
from encommon.types import DictStrAny

from pydantic import Field



EVENT = compile(
    r'^(?::(?P<prefix>[^\s]+)\s)?'
    r'(?P<command>[A-Z0-9]{3,})\s'
    r'(?P<params>.+)$')

KINDS = Literal[
    'event',
    'channel',
    'direct']

MESSAGE = [
    'channel',
    'direct']



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
        str,
        Field(...,
              description='Code or command for the event',
              min_length=1)]

    params: Annotated[
        Optional[str],
        Field(None,
              description='Event or command parameters')]


    def __init__(
        self,
        /,
        event: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data: DictStrAny = {}

        match = re_match(
            EVENT, event)

        assert match is not None


        prefix = (
            match
            .group('prefix'))

        command = (
            match
            .group('command'))

        params = (
            match
            .group('params'))


        if prefix is not None:
            data['prefix'] = (
                prefix.strip())

        if command is not None:
            data['command'] = (
                command.strip())

        if params is not None:
            data['params'] = (
                params.strip())


        super().__init__(**data)


    @property
    def kind(
        self,
    ) -> KINDS:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        command = self.command
        params = self.params


        if command == 'PRIVMSG':

            assert params is not None

            prefix = params[0][:1]

            return (
                'channel'
                if prefix in '#&+!'
                else 'direct')


        return 'event'


    @property
    def author(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        kind = self.kind
        prefix = self.prefix

        if kind not in MESSAGE:
            return None

        return prefix


    @property
    def recipient(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        kind = self.kind
        params = self.params

        if (kind not in MESSAGE
                or not params):
            return None

        split = params.split(' ')

        return split[0]


    @property
    def message(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        kind = self.kind
        params = self.params

        if (kind not in MESSAGE
                or not params):
            return None

        message = (
            params
            .split(':', maxsplit=1))

        return message[1]
