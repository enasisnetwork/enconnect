"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from time import sleep as block_sleep

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import raises

from .helpers import EVENTS
from .helpers import SVENTS
from ..client import Client
from ..models import ClientEvent
from ..params import ClientParams
from ...fixtures import IRCClientSocket



def test_ClientEvent() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = ClientParams(
        server='mocked',
        port=6667,
        nickname='ircbot',
        username='ircbot',
        realname='ircbot',
        ssl_enable=False)

    client = Client(params)


    _event = (
        ':server PING'
        ' :123456789')

    event = ClientEvent(
        client, _event)


    attrs = lattrs(event)

    assert attrs == [
        'prefix',
        'command',
        'params',
        'original',
        'kind',
        'isme',
        'hasme',
        'whome',
        'author',
        'recipient',
        'message']


    assert inrepr(
        'ClientEvent(prefix',
        event)

    with raises(TypeError):
        hash(event)

    assert instr(
        "prefix='server'",
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
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    .. note::
       Duplicative test routine as below but with EVENTS.

    :param client_ircsock: Object to mock client connection.
    """

    params = ClientParams(
        server='mocked',
        port=6667,
        nickname='ircbot',
        username='ircbot',
        realname='ircbot',
        ssl_enable=False)

    client = Client(params)


    def _operate() -> None:

        client_ircsock(EVENTS)

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
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
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
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '376'
    assert item.params == (
        'ircbot :End of /MOTD command.')

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == 'mocked'
    assert item.command == '376'
    assert item.params == (
        'ircbot :End of /MOTD command.')

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
    assert not item.author
    assert not item.recipient
    assert not item.message


    item = mqueue.get()

    assert item.prefix == (
        'nick!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        'ircbot :Hello ircbot')

    assert item.kind == 'privmsg'
    assert not item.isme
    assert item.hasme
    assert item.whome == 'ircbot'
    assert item.author == 'nick'
    assert item.recipient == 'ircbot'
    assert item.message == (
        'Hello ircbot')


    item = mqueue.get()

    assert item.prefix == (
        'nick!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        '# :Hello world')

    assert item.kind == 'chanmsg'
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
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
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'ircbot'
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
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'botirc'
    assert not item.author
    assert not item.recipient
    assert not item.message

    assert client.nickname == 'botirc'


    item = mqueue.get()

    assert item.prefix == (
        'botirc!user@host')
    assert item.command == 'PRIVMSG'
    assert item.params == (
        '# :Hello nick')

    assert item.kind == 'chanmsg'
    assert item.isme
    assert not item.hasme
    assert item.whome == 'botirc'
    assert item.author == 'botirc'
    assert item.recipient == '#'
    assert item.message == (
        'Hello nick')


    item = mqueue.get()

    assert not item.prefix
    assert item.command == 'ERROR'
    assert item.params == (
        ':Closing Link: botirc'
        '[mocked] (Quit: botirc)')

    assert item.kind == 'event'
    assert not item.isme
    assert not item.hasme
    assert item.whome == 'botirc'
    assert not item.author
    assert not item.recipient
    assert not item.message

    block_sleep(1)

    assert not client.canceled
    assert not client.connected
    assert client.nickname == 'botirc'


    thread.join(10)


    assert mqueue.empty()



def test_ClientEvent_service(
    client_ircsock: IRCClientSocket,
) -> None:
    """
    Perform various tests associated with relevant routines.

    .. note::
       Duplicative test routine as above but with SVENTS.

    :param client_ircsock: Object to mock client connection.
    """

    sname = 'jupiter.enasis.net'
    about = 'Network Services'

    params = ClientParams(
        server='mocked',
        port=6900,
        operate='service',
        servername=sname,
        password='password',
        realname=about)

    client = Client(params)


    def _operate() -> None:

        client_ircsock(SVENTS)

        _raises = ConnectionError

        with raises(_raises):
            client.operate()


    thread = Thread(
        target=_operate)

    thread.start()


    mqueue = client.mqueue


    for count in range(20):

        item = mqueue.get()

        assert not item.prefix
        assert not item.command
        assert not item.params

        assert item.kind == 'event'

        assert (
            not item.isme
            if count != 13
            else item.isme)

        assert not item.author
        assert not item.recipient
        assert not item.message


    assert client.nickname == '42X'


    thread.join(10)


    assert mqueue.empty()
