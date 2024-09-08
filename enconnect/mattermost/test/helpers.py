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



class MTMClientSocket(Protocol):
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

    {'status': 'OK',
     'seq_reply': 1},

    {'event': 'hello',
     'seq': 0},

    {'event': 'status_change',
     'broadcast': {
         'user_id': 'f4nf1ok9bj'},
     'data': {
         'status': 'online',
         'user_id': 'f4nf1ok9bj'},
     'seq': 1},

    {'status': 'OK',
     'seq_reply': 2},

    {'status': 'OK',
     'seq_reply': 3}]



WHOAMI: DictStrAny = {
    'id': 'f4nf1ok9bj',
    'create_at': 1725632524305,
    'update_at': 1725632712874,
    'delete_at': 0,
    'username': 'hal9000',
    'auth_data': '',
    'auth_service': '',
    'email': 'hal9000@mocked',
    'nickname': '',
    'first_name': 'HAL 9000',
    'last_name': '',
    'position': '',
    'roles': 'system_user system_post_all',
    'notify_props': {
        'channel': 'true',
        'comments': 'never',
        'desktop': 'mention',
        'desktop_sound': 'true',
        'desktop_threads': 'all',
        'email': 'true',
        'email_threads': 'all',
        'first_name': 'false',
        'mention_keys': '',
        'push': 'mention',
        'push_status': 'away',
        'push_threads': 'all'},
    'last_password_update': 1725632524305,
    'last_picture_update': 1725632524661,
    'locale': 'en',
    'timezone': {
        'automaticTimezone': '',
        'manualTimezone': '',
        'useAutomaticTimezone': 'true'},
    'is_bot': True,
    'bot_description': (
        "I'm sorry Dave, I'm "
        "afraid I can't do that"),
    'disable_welcome_email': False}



@fixture
def client_mtmsock(  # noqa: CFQ004
    mocker: MockerFixture,
    respx_mock: MockRouter,
) -> MTMClientSocket:
    """
    Construct the instance for use in the downstream tests.

    :param mocker: Object for mocking the Python routines.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    content = dumps(WHOAMI)

    (respx_mock
     .get(
         'https://mocked:443'
         '/api/v4/users/me')
     .mock(Response(
         status_code=200,
         content=content)))

    (respx_mock
     .post(
         'https://mocked:443'
         '/api/v4/posts')
     .mock(Response(200)))


    socmod = mocker.patch(
        ('enconnect.mattermost'
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

            # This event is not using
            # one that actually exist
            tneve = {
                'event': 'discon',
                'seq': 69420,
                'error': {
                    'reason': 'EOF'}}

            yield (
                dumps(tneve)
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
        rvents: EVENTS = None,
    ) -> SOCKET:

        rvents = rvents or []

        socket = _factory(
            RVENTS + rvents)

        socmod.return_value = socket

        return (socmod, socket)


    return _fixture
