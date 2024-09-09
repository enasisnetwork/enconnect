"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from ssl import SSLContext
from time import sleep as block_sleep
from typing import Iterator
from typing import Optional
from typing import Protocol
from typing import overload
from unittest.mock import MagicMock
from unittest.mock import Mock

from encommon.types import DictStrAny

from httpx import Response

from pytest import fixture

from pytest_mock import MockerFixture

from respx import MockRouter



_EVENTS = Optional[list[DictStrAny]]

_SOCKET = tuple[
    SSLContext,
    MagicMock]



EVENTS: list[DictStrAny] = [

    {'t': 'MESSAGE_CREATE',
     's': 3,
     'op': 0,
     'd': {
         'channel_id': 'privid',
         'author': {
             'id': 'userid',
             'username': 'user'},
         'content': 'Hello dscbot'}},

    {'t': 'MESSAGE_CREATE',
     's': 4,
     'op': 0,
     'd': {
         'channel_id': 'chanid',
         'guild_id': 'guldid',
         'author': {
             'id': 'userid',
             'username': 'user'},
         'content': 'Hello world'}},

    {'t': 'MESSAGE_CREATE',
     's': 5,
     'op': 0,
     'd': {
         'channel_id': 'chanid',
         'guild_id': 'guldid',
         'author': {
             'id': 'dscunq',
             'username': 'dscbot'},
         'content': 'Hello user'}}]



RVENTS: list[DictStrAny] = [

    {'t': 'READY',
     's': 1,
     'op': 0,
     'd': {
         'heartbeat_interval': 100,
         'resume_gateway_url': (
             'wss://resume.dsc.gg'),
         'session_id': 'mocked',
         'user': {
             'username': 'dscbot',
             'id': 'dscunq'}}},

    {'op': 7, 'd': None},

    {'t': None,
     's': None,
     'op': 10,
     'd': {
         'heartbeat_interval': 100,
         '_trace': ['["g....0}]']}},

    {'t': 'RESUMED',
     's': 1,
     'op': 0,
     'd': {
         '_trace': ['["g...3}]}]']}},

    {'op': 11, 'd': None}]



class DSCClientSocket(Protocol):
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
def client_dscsock(  # noqa: CFQ004
    mocker: MockerFixture,
    respx_mock: MockRouter,
) -> DSCClientSocket:
    """
    Construct the instance for use in the downstream tests.

    :param mocker: Object for mocking the Python routines.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    content = dumps({
        'url': 'mocked'})

    (respx_mock
     .get(
         'https://discord.com'
         '/api/v10/gateway')
     .mock(Response(
         status_code=200,
         content=content)))

    (respx_mock
     .post(
         'https://discord.com'
         '/api/v10/channels/'
         'privid/messages')
     .mock(Response(200)))


    socmod = mocker.patch(
        ('enconnect.discord'
         '.client.connect'),
        autospec=True)


    def _encode(
        resps: list[DictStrAny],
    ) -> list[bytes]:

        return [
            dumps(x).encode('utf-8')
            for x in resps]


    def _delayed(
        events: list[bytes],
    ) -> Iterator[bytes]:

        while True:

            for event in events:

                block_sleep(0.1)

                yield event

            block_sleep(0.1)

            yield (
                dumps({'op': 9})
                .encode('utf-8'))


    def _factory(
        rvents: list[DictStrAny],
    ) -> MagicMock:

        effect = _delayed(
            _encode(rvents))

        socket = MagicMock()

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

        socmod.return_value = socket

        return (socmod, socket)


    return _fixture
