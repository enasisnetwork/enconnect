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
from ...fixtures import DSCClientSocket



@fixture
def client() -> Client:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    params = ClientParams(
        token='mocked')

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
        '_Client__client',
        '_Client__socket',
        '_Client__conned',
        '_Client__exited',
        '_Client__mynick',
        '_Client__lsnick',
        '_Client__resume',
        '_Client__ping',
        '_Client__path',
        '_Client__sesid',
        '_Client__seqno',
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
    client_dscsock: DSCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Class instance for connecting to service.
    :param client_dscsock: Object to mock client connection.
    """

    client_dscsock()


    with raises(ConnectionError):
        client.operate()

    assert not client.canceled
    assert not client.connected

    mqueue = client.mqueue

    assert mqueue.qsize() == 5
