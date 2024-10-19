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



_EVENTS = Optional[list[str]]

_SOCKET = tuple[
    SSLContext,
    MagicMock]

_TUBLYTES = tuple[bytes, ...]



EVENTS: list[str] = [

    (':mocked 376 ircbot '
     ':End of /MOTD command.'),

    (':nick!user@host PRIVMSG'
     ' ircbot :Hello ircbot'),

    (':nick!user@host PRIVMSG'
     ' # :Hello world'),

    (':nick!user@host PRIVMSG'
     ' #funchat :Hello world'),

    (':ircbot!user@host'
     ' NICK :botirc'),

    (':botirc!user@host PRIVMSG'
     ' # :Hello nick'),

    ('ERROR :Closing Link: botirc'
     '[mocked] (Quit: botirc)')]



SVENTS: list[str] = [

    ('SERVER jupiter.invalid 1'
     ' :U6100-Fhn6OoErmM-0AD IRC Network'),

    (':0AD SID neptune.invalid'
     ' 2 0PS :IRC Network'),

    ('@s2s-md/tls_cipher='
     'TLSv1.3-TLS_CHACHA20_POLY1305_SHA256;'
     's2s-md/creationtime=1727476461'
     ' :0PS UID ircbot 0'
     ' 1727476461 ircbot'
     ' localhost 0PS3FGG02'
     ' 0 +iwxz * irc-5DE79E97'
     ' fwAAAQ== :ircbot'),

    (':0AD MD client 0PS3FGG02'
     ' creationtime :1727476461'),

    (':0AD MD client'
     ' 0PS3FGG02 tls_cipher '
     ':TLSv1.3-TLS_CHACHA20_POLY1305_SHA256'),

    ('@s2s-md/tls_cipher='
     'TLSv1.3-TLS_CHACHA20_POLY1305_SHA256;'
     's2s-md/creationtime=1727476468;'
     's2s-md/operlogin=robert;'
     's2s-md/operclass=netadmin'
     ' :0AD UID robert 0'
     ' 1727508036 robert'
     ' localhost 0AD1QCV03'
     ' 0 +iowxz * irc-5DE79E97'
     ' AAAAAAAAAAAAAAAAAAAAAQ== :robert'),

    (':0AD MD client 0AD1QCV03'
     ' operclass :netadmin'),

    (':0AD MD client 0AD1QCV03'
     ' operlogin :robert'),

    (':0AD MD client 0AD1QCV03'
     ' creationtime :1727476468'),

    (':0AD MD client'
     ' 0AD1QCV03 tls_cipher '
     ':TLSv1.3-TLS_CHACHA20_POLY1305_SHA256'),

    (':42X UID ChatServ 0'
     ' 1727569796 service'
     ' services.invalid 42X000009'
     ' 0 +Sio services.invalid'
     ' services.invalid * '
     ':Invitable LLM chatting'),

    ('@msgid=Z48DNGsGfMhR8UwXhAljGz;'
     'time=2024-09-29T00:29:56.463Z'
     ' :0AD SJOIN 1727476468'
     ' #opers +nt :@0AD1QCV03'),

    ('NETINFO 11 1727569796 6100'
     ' SHA256:b94e96b5d7fbba92fc0a36c2'
     '667d4d1581a6281ac1440a741d5556f3'
     ' 0 0 0 :EnasisNET'),

    (':0AD1QCV03 SAJOIN'
     ' 0PS3FGG02 #funchat'),

    ('@time=2024-09-29T00:53:42.190Z;'
     'msgid=bdVQ13oQfRcdUnxX2hbb4C;'
     'unrealircd.org/issued-by='
     'OPER:robert@jupiter.invalid:robert'
     ' :0PS SJOIN 1727571222'
     ' #funchat :0PS3FGG02'),

    ('@unrealircd.org/issued-by='
     'OPER:robert@jupiter.invalid:robert;'
     'msgid=bdVQ13oQfRcdUnxX2hbb4C'
     '-6D9mg3IKCGFgtCeraInDIA;'
     'time=2024-09-29T00:53:42.190Z'
     ' :0PS MODE #funchat'
     ' +nt  1727571222'),

    ('@msgid=mjvxur6dNstbXFajGoPjrU;'
     'time=2024-09-29T00:53:45.577Z'
     ' :0AD SJOIN 1727571222'
     ' #funchat :0AD1QCV03')]



RVENTS: list[str] = [

    (':mocked 001 ircbot'
     ' :Welcome to network'),

    (':mocked 376 ircbot '
     ':End of /MOTD command.'),

    'PING :123456789',

    (':mocked 376 ircbot '
     ':End of /MOTD command.'),

    'PING :123456789']



class IRCClientSocket(Protocol):
    """
    Typing protocol which the developer does not understand.
    """

    @overload
    def __call__(
        self,
        rvents: _EVENTS,
    ) -> _SOCKET:
        ...  # NOCVR

    @overload
    def __call__(
        self,
    ) -> _SOCKET:
        ...  # NOCVR

    def __call__(
        self,
        rvents: _EVENTS = None,
    ) -> _SOCKET:
        """
        Construct the instance for use in the downstream tests.

        :param rvents: Raw events for playback from the server.
        """
        ...  # NOCVR



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
    ) -> _TUBLYTES:

        event += '\r\n'

        split = [
            x.encode('utf-8')
            for x in event]

        return tuple(split)


    def _encode(
        resps: list[str],
    ) -> list[_TUBLYTES]:

        items = [
            _split(x)
            for x in resps]

        return items


    def _delayed(
        events: list[_TUBLYTES],
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
        rvents: _EVENTS = None,
    ) -> _SOCKET:

        rvents = rvents or []

        socket = _factory(
            RVENTS + rvents)

        secmod.return_value = socket
        mckmod.return_value = socket

        return (secket, socket)


    return _fixture
