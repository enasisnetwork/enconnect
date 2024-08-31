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



EVENTS = Optional[list[DictStrAny]]

SOCKET = tuple[
    SSLContext,
    MagicMock]



class DSCClientSocket(Protocol):
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



RVENTS: list[DictStrAny] = [

    {'t': 'READY',
     's': 1,
     'op': 0,
     'd': {
         'heartbeat_interval': 1000,
         'session_id': 'mocked'}},

    {'op': 7, 'd': None},

    {'t': 'READY',
     's': 1,
     'op': 0,
     'd': {
         'heartbeat_interval': 1000,
         'session_id': 'mocked'}},

    {'t': None,
     's': None,
     'op': 11,
     'd': None}]



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
     .mock(side_effect=[
         Response(
             status_code=200,
             content=content),
         Response(
             status_code=200,
             content=content)]))


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

        for event in events:

            block_sleep(0.25)

            yield event


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
        rvents: EVENTS = None,
    ) -> SOCKET:

        if rvents is None:
            rvents = []  # NOCVR

        socket = _factory(
            RVENTS + rvents)

        socmod.return_value = socket

        return (socmod, socket)


    return _fixture
