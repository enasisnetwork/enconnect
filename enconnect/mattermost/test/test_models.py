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
from ...fixtures import MTMClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    event = ClientEvent({
        'status': 'OK',
        'seq_reply': 1})


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
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(type',
        event)

    with raises(TypeError):
        assert hash(event) > 0

    assert instr(
        'type=None data=None',
        event)


    assert event.kind == 'event'

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

    events: list[DictStrAny] = [

        {'event': 'posted',
         'seq': 4,
         'broadcast': {
             'channel_id': 'nwyxekd4k7'},
         'data': {
             'channel_type': 'D',
             'post': (
                 '{"user_id":"ietyrmdt5b",'
                 '"channel_id":"yxenwkd3w2",'
                 '"message":"Hello person"}'),
             'sender_name': '@robert'}},

        {'event': 'posted',
         'seq': 5,
         'broadcast': {
             'channel_id': 'nwyxekd4k7'},
         'data': {
             'channel_type': 'P',
             'post': (
                 '{"user_id":"ietyrmdt5b",'
                 '"channel_id":"nwyxekd4k7",'
                 '"message":"Hello world"}'),
             'sender_name': '@robert'}}]


    params = ClientParams(
        server='mocked',
        token='mocked',
        teamid='mocked')

    client = Client(params)


    def _operate() -> None:

        client_mtmsock(events)

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
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert client.connected
    assert client.nickname == (
        'hal9000', 'f4nf1ok9bj')


    item = mqueue.get()

    assert item.type == 'hello'
    assert not item.data
    assert not item.broadcast
    assert not item.seqno
    assert not item.status
    assert not item.error
    assert not item.seqre

    assert item.kind == 'event'
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
    assert item.author == (
        'ietyrmdt5b', '@robert')
    assert item.recipient == (
        'yxenwkd3w2')
    assert item.message == (
        'Hello person')


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
    assert item.author == (
        'ietyrmdt5b', '@robert')
    assert item.recipient == (
        'nwyxekd4k7')
    assert item.message == (
        'Hello world')


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
    assert not item.author
    assert not item.recipient
    assert not item.message


    thread.join(10)


    assert mqueue.empty()
