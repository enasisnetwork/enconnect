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
from ...fixtures import MTMClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = ClientParams(
        server='mocked',
        token='mocked',
        teamid='mocked')

    client = Client(params)


    _event = {
        'status': 'OK',
        'seq_reply': 1}

    event = ClientEvent(
        client, _event)


    attrs = lattrs(event)

    assert attrs == [
        'type',
        'data',
        'broadcast',
        'seqno',
        'status',
        'error',
        'seqre',
        'original',
        'kind',
        'isme',
        'hasme',
        'whome',
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(type',
        event)

    with raises(TypeError):
        hash(event)

    assert instr(
        'type=None data=None',
        event)


    assert event.original

    assert event.kind == 'event'

    assert not event.isme

    assert not event.hasme

    assert not event.whome

    assert not event.author

    assert not event.recipient

    assert not event.message



def test_ClientEvent_cover(  # noqa: CFQ001
    client_mtmsock: MTMClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client_ircsock: Object to mock client connection.
    """

    params = ClientParams(
        server='mocked',
        token='mocked',
        teamid='mocked')

    client = Client(params)


    def _operate() -> None:

        client_mtmsock(EVENTS)

        _raises = ConnectionError

        with raises(_raises):
            client.operate()


    thread = Thread(
        target=_operate)

    thread.start()


    mqueue = client.mqueue


    item = mqueue.get()

    assert not item.type
    assert not item.data
    assert not item.broadcast
    assert not item.seqno
    assert item.status == 'OK'
    assert not item.error
    assert item.seqre == 1

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert client.connected
    assert client.nickname == (
        'mtmbot', 'mtmunq')


    item = mqueue.get()

    assert item.type == 'hello'
    assert not item.data
    assert not item.broadcast
    assert not item.seqno
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == (
        'status_change')
    assert item.data
    assert item.broadcast
    assert item.seqno == 1
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert not item.type
    assert not item.data
    assert not item.broadcast
    assert not item.seqno
    assert item.status == 'OK'
    assert not item.error
    assert item.seqre == 2

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert not item.type
    assert not item.data
    assert not item.broadcast
    assert not item.seqno
    assert item.status == 'OK'
    assert not item.error
    assert item.seqre == 3

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.type == 'posted'
    assert item.data
    assert len(item.data) == 3
    assert item.broadcast
    assert len(item.broadcast) == 1
    assert item.seqno == 4
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'privmsg'
    assert not item.isme
    assert item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert item.author == (
        'user', 'userid')
    assert item.recipient == (
        'privid')
    assert item.message == (
        'Hello mtmbot')


    item = mqueue.get()

    assert item.type == 'posted'
    assert item.data
    assert len(item.data) == 3
    assert item.broadcast
    assert len(item.broadcast) == 1
    assert item.seqno == 5
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'chanmsg'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert item.author == (
        'user', 'userid')
    assert item.recipient == (
        'chanid')
    assert item.message == (
        'Hello world')


    item = mqueue.get()

    assert item.type == 'posted'
    assert item.data
    assert len(item.data) == 3
    assert item.broadcast
    assert len(item.broadcast) == 1
    assert item.seqno == 6
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'chanmsg'
    assert item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert item.author == (
        'mtmbot', 'mtmunq')
    assert item.recipient == (
        'chanid')
    assert item.message == (
        'Hello user')


    item = mqueue.get()

    assert item.type == 'discon'
    assert not item.data
    assert not item.broadcast
    assert item.seqno == 69420
    assert not item.status
    assert item.error
    assert len(item.error) == 1
    assert not item.seqre

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome
    assert item.whome[0] == 'mtmbot'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert not client.connected
    assert client.nickname == (
        'mtmbot', 'mtmunq')


    thread.join(10)


    assert mqueue.empty()
