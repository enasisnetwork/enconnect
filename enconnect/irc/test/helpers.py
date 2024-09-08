"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ssl import SSLContext
from ssl import SSLSocket
from time import sleep as block_sleep
from typing import Iterator
from typing import Optional
from typing import Protocol
from typing import overload
from unittest.mock import MagicMock
from unittest.mock import Mock

from pytest import fixture

from pytest_mock import MockerFixture



EVENTS = Optional[list[str]]

SOCKET = tuple[
    SSLContext,
    MagicMock]

TUBLYTES = tuple[bytes, ...]



class IRCClientSocket(Protocol):
    """
    Typing protocol which the developer does not understand.
    """

    @overload
    def __call__(
        self,
        rvents: EVENTS,
    ) -> SOCKET:
        ...  # NOCVR

    @overload
    def __call__(
        self,
    ) -> SOCKET:
        ...  # NOCVR

    def __call__(
        self,
        rvents: EVENTS = None,
    ) -> SOCKET:
        """
        Construct the instance for use in the downstream tests.

        :param rvents: Raw events for playback from the server.
        """
        ...  # NOCVR



RVENTS: list[str] = [

    (':mocked 001 ircbot'
     ' :Welcome to network'),

    (':mocked 376 ircbot '
     ':End of /MOTD command.'),

    'PING :123456789',

    (':mocked 376 ircbot '
     ':End of /MOTD command.'),

    'PING :123456789']



@fixture
def client_ircsock(  # noqa: CFQ004
    mocker: MockerFixture,
) -> IRCClientSocket:
    """
    Construct the instance for use in the downstream tests.

    :param mocker: Object for mocking the Python routines.
    :returns: Newly constructed instance of related class.
    """

    mckctx = mocker.patch(
        ('enconnect.irc'
         '.client.default'),
        autospec=True)

    mckmod = mocker.patch(
        ('enconnect.irc'
         '.client.socket'),
        autospec=True)

    secket = (
        mckctx.return_value)

    secmod = (
        secket.wrap_socket)


    def _split(
        event: str,
    ) -> TUBLYTES:

        event += '\r\n'

        split = [
            x.encode('utf-8')
            for x in event]

        return tuple(split)


    def _encode(
        resps: list[str],
    ) -> list[TUBLYTES]:

        items = [
            _split(x)
            for x in resps]

        return items


    def _delayed(
        events: list[TUBLYTES],
    ) -> Iterator[bytes]:

        while True:

            for event in events:

                block_sleep(0.1)

                yield from event

            block_sleep(0.1)

            yield from [b'']


    def _factory(
        rvents: list[str],
    ) -> MagicMock:

        effect = _delayed(
            _encode(rvents))

        socket = MagicMock(
            SSLSocket)

        socket.send = Mock()

        socket.recv = Mock(
            side_effect=effect)

        socket.close = Mock()

        return socket


    def _fixture(
        rvents: EVENTS = None,
    ) -> SOCKET:

        rvents = rvents or []

        socket = _factory(
            RVENTS + rvents)

        secmod.return_value = socket
        mckmod.return_value = socket

        return (secket, socket)


    return _fixture
