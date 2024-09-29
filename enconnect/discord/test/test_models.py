"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import raises

from .helpers import EVENTS
from ..client import Client
from ..models import ClientEvent
from ..params import ClientParams
from ...fixtures import DSCClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = ClientParams(
        token='mocked')

    client = Client(params)


    _event = {'op': 1}

    event = ClientEvent(
        client, _event)


    attrs = lattrs(event)

    assert attrs == [
        'type',
        'opcode',
        'data',
        'seqno',
        'original',
        'kind',
        'isme',
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(type',
        event)

    with raises(TypeError):
        hash(event)

    assert instr(
        'opcode=1 data=None',
        event)


    assert event.original

    assert event.kind == 'event'

    assert not event.isme

    assert not event.author

    assert not event.recipient

    assert not event.message



def test_ClientEvent_cover(  # noqa: CFQ001
    client_dscsock: DSCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client_dscsock: Object to mock client connection.
    """

    params = ClientParams(
        token='mocked')

    client = Client(params)


    def _operate() -> None:

        client_dscsock(EVENTS)

        _raises = ConnectionError

        with raises(_raises):
            client.operate()


    thread = Thread(
        target=_operate)

    thread.start()


    mqueue = client.mqueue


    item = mqueue.get()

    assert item.type == 'READY'
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 4
    assert item.seqno == 1

    assert item.kind == 'event'
    assert not item.isme
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert client.connected
    assert client.nickname == (
        'dscbot', 'dscunq')


    item = mqueue.get()

    assert not item.type
    assert item.opcode == 7
    assert not item.data
    assert not item.seqno

    assert item.kind == 'event'
    assert not item.isme
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert not item.type
    assert item.opcode == 10
    assert item.data
    assert len(item.data) == 2
    assert not item.seqno

    assert item.kind == 'event'
    assert not item.isme
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == 'RESUMED'
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 1
    assert item.seqno == 1

    assert item.kind == 'event'
    assert not item.isme
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == (
        'MESSAGE_CREATE')
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 3
    assert item.seqno == 3

    assert item.kind == 'privmsg'
    assert not item.isme
    assert item.author == (
        'user', 'userid')
    assert item.recipient == (
        (None, 'privid'))
    assert item.message == (
        'Hello dscbot')


    item = mqueue.get()

    assert item.type == (
        'MESSAGE_CREATE')
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 4
    assert item.seqno == 4

    assert item.kind == 'chanmsg'
    assert not item.isme
    assert item.author == (
        'user', 'userid')
    assert item.recipient == (
        ('guldid', 'chanid'))
    assert item.message == (
        'Hello world')


    item = mqueue.get()

    assert item.type == (
        'MESSAGE_CREATE')
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 4
    assert item.seqno == 5

    assert item.kind == 'chanmsg'
    assert item.isme
    assert item.author == (
        'dscbot', 'dscunq')
    assert item.recipient == (
        ('guldid', 'chanid'))
    assert item.message == (
        'Hello user')


    item = mqueue.get()

    assert not item.type
    assert item.opcode == 9
    assert not item.data
    assert not item.seqno

    assert item.kind == 'event'
    assert not item.isme
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert not client.connected
    assert client.nickname == (
        'dscbot', 'dscunq')


    thread.join(10)


    assert mqueue.empty()
