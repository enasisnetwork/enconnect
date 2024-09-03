"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread

from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import raises

from ..client import Client
from ..models import ClientEvent
from ..params import ClientParams
from ...fixtures import DSCClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    event = ClientEvent(
        {'op': 1, 'd': None})


    attrs = lattrs(event)

    assert attrs == [
        'type',
        'opcode',
        'data',
        'seqno',
        'original',
        'kind',
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(type',
        event)

    with raises(TypeError):
        assert hash(event) > 0

    assert instr(
        'opcode=1 data=None',
        event)


    assert event.kind == 'event'

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

    events: list[DictStrAny] = [

        {'t': 'MESSAGE_CREATE',
         's': 3,
         'op': 0,
         'd': {
             'id': '33330001',
             'channel_id': '22220001',
             'author': {
                 'id': '44444444',
                 'username': 'Author'},
             'content': 'Hello person'}},

        {'t': 'MESSAGE_CREATE',
         's': 4,
         'op': 0,
         'd': {
             'id': '33330001',
             'channel_id': '22220002',
             'guild_id': '11111111',
             'author': {
                 'id': '44444444',
                 'username': 'Author'},
             'content': 'Hello world'}}]


    params = ClientParams(
        token='mocked')

    client = Client(params)


    def _operate() -> None:

        client_dscsock(events)

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
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert client.connected
    assert client.nickname == (
        'dscbot', '10101010')


    item = mqueue.get()

    assert not item.type
    assert item.opcode == 7
    assert not item.data
    assert not item.seqno

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == 'RESUMED'
    assert item.opcode == 0
    assert not item.data
    assert item.seqno == 2

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == (
        'MESSAGE_CREATE')
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 4
    assert item.seqno == 3

    assert item.kind == 'privmsg'
    assert item.author == (
        '44444444', 'Author')
    assert item.recipient == (
        (None, '22220001'))
    assert item.message == (
        'Hello person')


    item = mqueue.get()

    assert item.type == (
        'MESSAGE_CREATE')
    assert item.opcode == 0
    assert item.data
    assert len(item.data) == 5
    assert item.seqno == 4

    assert item.kind == 'chanmsg'
    assert item.author == (
        '44444444', 'Author')
    assert item.recipient == (
        ('11111111', '22220002'))
    assert item.message == (
        'Hello world')


    item = mqueue.get()

    assert not item.type
    assert item.opcode == 9
    assert not item.data
    assert not item.seqno

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert not client.connected
    assert not client.nickname


    thread.join(10)


    assert mqueue.empty()
