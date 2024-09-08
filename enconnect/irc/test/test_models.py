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

from ..client import Client
from ..models import ClientEvent
from ..params import ClientParams
from ...fixtures import IRCClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    event = ClientEvent(
        ':server PING :123456789')


    attrs = lattrs(event)

    assert attrs == [
        'prefix',
        'command',
        'params',
        'original',
        'kind',
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(prefix',
        event)

    with raises(TypeError):
        assert hash(event) > 0

    assert instr(
        "prefix='server'",
        event)


    assert event.kind == 'event'

    assert not event.author

    assert not event.recipient

    assert not event.message



def test_ClientEvent_cover(  # noqa: CFQ001
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client_ircsock: Object to mock client connection.
    """

    events = [

        (':mocked 376 ircbot '
         ':End of /MOTD command.'),

        (':nick!user@host PRIVMSG'
         ' ircbot :Hello person'),

        (':nick!user@host PRIVMSG'
         ' # :Hello world'),

        (':nick!user@host PRIVMSG'
         ' #funchat :Hello world'),

        (':ircbot!user@host'
         ' NICK :botirc'),

        ('ERROR :Closing Link: ircbot'
         '[mocked] (Quit: ircbot)')]


    params = ClientParams(
        server='mocked',
        port=6667,
        nickname='ircbot',
        username='ircbot',
        realname='ircbot',
        ssl_enable=False)

    client = Client(params)


    def _operate() -> None:

        client_ircsock(events)

        _raises = ConnectionError

        with raises(_raises):
            client.operate()


    thread = Thread(
        target=_operate)

    thread.start()


    mqueue = client.mqueue


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '001'
    assert item.params == (
        'ircbot :Welcome to network')

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert client.connected
    assert client.nickname == 'ircbot'


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '376'
    assert item.params == (
        'ircbot :End of /MOTD command.')

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '376'
    assert item.params == (
        'ircbot :End of /MOTD command.')

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '376'
    assert item.params == (
        'ircbot :End of /MOTD command.')

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == (
        'nick!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        'ircbot :Hello person')

    assert item.kind == 'privmsg'
    assert item.author == 'nick'
    assert item.recipient == 'ircbot'
    assert item.message == (
        'Hello person')


    item = mqueue.get()

    assert item.prefix == (
        'nick!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        '# :Hello world')

    assert item.kind == 'chanmsg'
    assert item.author == 'nick'
    assert item.recipient == '#'
    assert item.message == (
        'Hello world')


    item = mqueue.get()

    assert item.prefix == (
        'nick!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        '#funchat :Hello world')

    assert item.kind == 'chanmsg'
    assert item.author == 'nick'
    assert item.recipient == '#funchat'
    assert item.message == (
        'Hello world')


    item = mqueue.get()

    assert item.prefix == (
        'ircbot!user@host')
    assert item.command == 'NICK'
    assert item.params == ':botirc'

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert client.nickname == 'botirc'


    item = mqueue.get()

    assert not item.prefix
    assert item.command == 'ERROR'
    assert item.params == (
        ':Closing Link: ircbot'
        '[mocked] (Quit: ircbot)')

    assert item.kind == 'event'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert not client.canceled
    assert not client.connected
    assert not client.nickname


    thread.join(10)


    assert mqueue.empty()
