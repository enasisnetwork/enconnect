"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from queue import Queue
from re import compile
from re import match as re_match
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket
from ssl import CERT_NONE
from ssl import CERT_REQUIRED
from ssl import SSLSocket
from ssl import create_default_context as default
from threading import Event
from typing import Iterator
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types.strings import SEMPTY

from .models import ClientEvent

if TYPE_CHECKING:
    from .params import ClientParams



PING = compile(
    r'^PING \:(\S+)$')

HELO = compile(
    r'^\:\S+\s001\s'
    r'(?P<crrnt>\S+)')

NICK = compile(
    r'^\:(?P<nick1>[^\!]+)'
    r'(\!\S+)?\sNICK\s\:'
    r'(?P<nick2>\S+)')



class Client:
    """
    Establish and maintain connection with the chat service.

    :param params: Parameters used to instantiate the class.
    """

    __params: 'ClientParams'

    __socket: Optional[socket | SSLSocket]
    __conned: Event
    __exited: Event
    __mynick: Optional[str]

    __mqueue: Queue[ClientEvent]
    __cancel: Event


    def __init__(
        self,
        params: 'ClientParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params

        self.__socket = None
        self.__conned = Event()
        self.__exited = Event()
        self.__mynick = None

        self.__mqueue = Queue(
            params.queue_size)

        self.__cancel = Event()


    @property
    def params(
        self,
    ) -> 'ClientParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def connected(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__conned.is_set()


    @property
    def nickname(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__mynick


    @property
    def mqueue(
        self,
    ) -> Queue[ClientEvent]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__mqueue


    @property
    def canceled(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return (
            self.__cancel.is_set()
            or self.__exited.is_set())


    def operate(
        self,
    ) -> None:
        """
        Operate the client and populate queue with the messages.
        """

        try:

            self.__socket = None
            self.__conned.clear()
            self.__exited.clear()
            self.__mynick = None

            self.__cancel.clear()

            self.__operate()

        finally:

            self.__socket = None
            self.__conned.clear()
            self.__exited.clear()
            self.__mynick = None

            self.__cancel.clear()


    def __operate(
        self,
    ) -> None:
        """
        Operate the client and populate queue with the messages.
        """

        self.__connect()

        socket = self.__socket

        assert socket is not None

        while not self.canceled:

            receive = (
                self.socket_recv())

            for event in receive:
                self.__event(event)

        socket.close()

        if self.__exited.is_set():
            raise ConnectionError


    def __event(
        self,
        event: str,
    ) -> None:
        """
        Operate the client and populate queue with the messages.

        :param event: Raw event received from the network peer.
        """

        mqueue = self.__mqueue
        crrnt = self.__mynick

        model = ClientEvent


        match = re_match(
            HELO, event)

        if match is not None:

            crrnt = (
                match.group('crrnt'))

            self.__mynick = crrnt


        match = re_match(
            PING, event)

        if match is not None:

            ping = match.group(1)
            pong = f'PONG {ping}'

            self.socket_send(pong)

            return None


        match = re_match(
            NICK, event)

        if match is not None:

            nick1 = (
                match.group('nick1'))

            nick2 = (
                match.group('nick2'))

            if nick1 == crrnt:
                self.__mynick = nick2


        object = model(event)

        mqueue.put(object)


    def stop(
        self,
    ) -> None:
        """
        Gracefully close the connection with the server socket.
        """

        if self.connected:

            self.socket_send(
                'QUIT :Adios')

        self.__cancel.set()


    def __wrapper(
        self,
        socket: socket,
    ) -> SSLSocket:
        """
        Construct the object from wrapping SSL context settings.

        :param socket: Socket instance that will be SSL wrapped.
        """

        params = self.__params

        server = params.server
        verify = params.ssl_verify

        context = default()


        setattr(
            context,
            'check_hostname',
            verify)


        _verify = (
            CERT_REQUIRED
            if verify is True
            else CERT_NONE)

        setattr(
            context,
            'verify_mode',
            _verify)


        wrapper = context.wrap_socket

        return wrapper(
            socket,
            server_hostname=server)


    def __connect(
        self,
    ) -> None:
        """
        Establish the connection with the upstream using socket.
        """

        params = self.__params

        server = params.server
        port = params.port
        nick = params.nickname
        user = params.username
        real = params.realname

        senable = params.ssl_enable

        address = (server, port)


        handle = socket(
            AF_INET, SOCK_STREAM)

        handle.settimeout(1)


        if senable is True:
            wrapper = self.__wrapper
            handle = wrapper(handle)


        handle.connect(address)


        self.__socket = handle


        self.socket_send(
            f'NICK {nick}')

        self.socket_send(
            f'USER {user} . '
            f'{nick} :{real}')


        self.__conned.set()
        self.__exited.clear()

        self.__mynick = None


    def socket_send(
        self,
        send: str,
    ) -> None:
        """
        Transmit provided content through the socket connection.

        :param send: Content which will be sent through socket.
        """

        socket = self.__socket

        assert socket is not None

        transmit = (
            f'{send}\r\n'
            .encode('utf-8'))

        socket.send(transmit)


    def socket_recv(
        self,
    ) -> Iterator[str]:
        """
        Return the content received from the socket connection.

        .. note::
           Method could be further optimized using an internal
           buffer within the class after receiving more bytes.

        :returns: Content received from the socket connection.
        """

        exited = self.__exited
        socket = self.__socket

        assert socket is not None

        lastrd = SEMPTY
        buffer: list[str] = []


        def _receive() -> str:

            recev = socket.recv(1)

            return (
                recev
                .decode('utf-8'))


        def _returned() -> str:

            return (
                SEMPTY.join(buffer)
                .strip('\r\n'))


        while (len(buffer) < 4096
               and lastrd != '\n'):

            try:
                lastrd = _receive()

            except TimeoutError:
                break

            buffer.append(lastrd)


            if lastrd == '\n':

                event = _returned()

                buffer = []

                if event == '':
                    exited.set()

                if event[:5] == 'ERROR':
                    exited.set()

                if len(event) >= 1:
                    yield event