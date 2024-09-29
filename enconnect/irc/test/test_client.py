"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from unittest.mock import Mock

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import fixture
from pytest import raises

from ..client import Client
from ..params import ClientParams
from ...fixtures import IRCClientSocket



@fixture
def client() -> Client:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = ClientParams(
        server='mocked',
        port=6667,
        nickname='client',
        username='client',
        realname='client',
        ssl_enable=False)

    return Client(params)



def test_Client(
    client: Client,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting to service.
    """


    attrs = lattrs(client)

    assert attrs == [
        '_Client__params',
        '_Client__logger',
        '_Client__socket',
        '_Client__conned',
        '_Client__exited',
        '_Client__mynick',
        '_Client__lsnick',
        '_Client__mqueue',
        '_Client__cancel']


    assert inrepr(
        'client.Client object',
        client)

    assert isinstance(
        hash(client), int)

    assert instr(
        'client.Client object',
        client)


    assert client.params

    assert not client.connected

    assert not client.nickname

    assert client.mqueue.qsize() == 0

    assert not client.canceled



def test_Client_cover(
    client: Client,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting to service.
    """

    client.stop()

    client._Client__conned.set()  # type: ignore
    client._Client__socket = Mock()  # type: ignore

    client.stop()



def test_Client_connect(
    client: Client,
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting to service.
    :param client_ircsock: Object to mock client connection.
    """

    params = client.params


    params.port = 6697
    params.ssl_enable = True

    client = Client(params)

    client_ircsock()

    with raises(ConnectionError):
        client.operate()

    assert not client.canceled
    assert not client.connected

    mqueue = client.mqueue

    assert mqueue.qsize() == 3


    params.port = 6667
    params.ssl_enable = False

    client = Client(params)

    client_ircsock()

    with raises(ConnectionError):
        client.operate()

    assert not client.canceled
    assert not client.connected

    mqueue = client.mqueue

    assert mqueue.qsize() == 3


    params.operate = 'service'
    params.port = 6900
    params.password = 'password'
    params.ssl_enable = True

    client = Client(params)

    client_ircsock()

    with raises(ConnectionError):
        client.operate()

    assert not client.canceled
    assert not client.connected

    mqueue = client.mqueue

    assert mqueue.qsize() == 3
