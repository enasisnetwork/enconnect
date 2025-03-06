"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from json import loads
from queue import Queue
from threading import Event
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer
from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types import sort_dict

from httpx import Response

from websockets.exceptions import ConnectionClosedOK
from websockets.sync.client import ClientConnection
from websockets.sync.client import connect

from .models import ClientEvent
from ..utils import HTTPClient
from ..utils import dumlog
from ..utils.http import _METHODS
from ..utils.http import _PAYLOAD

if TYPE_CHECKING:
    from .params import ClientParams



PING = {
    'action': 'ping',
    'seq': 1}



class Client:
    """
    Establish and maintain connection with the chat service.

    :param params: Parameters used to instantiate the class.
    """

    __params: 'ClientParams'
    __logger: Callable[..., None]

    __client: HTTPClient
    __socket: Optional[ClientConnection]
    __conned: Event
    __exited: Event
    __mynick: Optional[tuple[str, str]]
    __lsnick: Optional[tuple[str, str]]

    __mqueue: Queue[ClientEvent]
    __cancel: Event


    def __init__(
        self,
        params: 'ClientParams',
        logger: Optional[Callable[..., None]] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__params = params
        self.__logger = (
            logger or dumlog)

        client = HTTPClient(
            timeout=params.timeout,
            verify=params.ssl_verify,
            capem=params.ssl_capem)

        self.__client = client
        self.__socket = None
        self.__conned = Event()
        self.__exited = Event()
        self.__mynick = None
        self.__lsnick = None

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

        return (
            not self.__exited.is_set()
            and self.__conned.is_set())


    @property
    def nickname(
        self,
    ) -> Optional[tuple[str, str]]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__mynick or self.__lsnick


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

        logger = self.__logger

        try:

            logger(item='initial')

            self.__socket = None
            self.__conned.clear()
            self.__exited.clear()
            self.__mynick = None

            self.__cancel.clear()

            logger(item='operate')

            self.__operate()

        finally:

            self.__socket = None
            self.__conned.clear()
            self.__exited.clear()
            self.__mynick = None

            self.__cancel.clear()

            logger(item='finish')


    def __operate(
        self,
    ) -> None:
        """
        Operate the client and populate queue with the messages.
        """

        logger = self.__logger


        self.__connect()

        socket = self.__socket

        assert socket is not None


        timer = Timer(
            30, start='min')


        self.__identify()


        while not self.canceled:

            receive = (
                self.socket_recv())

            if receive is not None:
                self.__event(receive)

            if timer.pause():
                continue  # NOCVR

            logger(item='ping')

            self.socket_send(PING)


        logger(item='close')

        socket.close(1000)


        if self.__exited.is_set():
            raise ConnectionError


    def __event(
        self,
        event: DictStrAny,
    ) -> None:
        """
        Operate the client and populate queue with the messages.

        :param event: Raw event received from the network peer.
        """

        logger = self.__logger
        mqueue = self.__mqueue

        tneve = event.get('event')

        model = ClientEvent


        if tneve == 'hello':

            logger(item='helo')


        object = model(
            self, event)

        mqueue.put(object)


    def stop(
        self,
    ) -> None:
        """
        Gracefully close the connection with the server socket.
        """

        logger = self.__logger

        logger(item='stop')

        self.__cancel.set()


    def __connect(
        self,
    ) -> None:
        """
        Establish the connection with the upstream using socket.
        """

        logger = self.__logger

        _params = self.__params
        server = _params.server

        logger(item='connect')

        socket = connect(
            f'wss://{server}/'
            'api/v4/websocket')

        self.__socket = socket

        self.__conned.set()
        self.__exited.clear()


    def __identify(
        self,
    ) -> None:
        """
        Identify the client once the connection is established.
        """

        logger = self.__logger
        request = self.request

        _params = self.__params
        token = _params.token

        logger(item='identify')

        action = (
            'authentication'
            '_challenge')

        data = {'token': token}

        self.socket_send({
            'seq': 1,
            'action': action,
            'data': data})


        response = request(
            'get', 'users/me')

        (response
         .raise_for_status())


        fetch = response.json()

        assert isinstance(fetch, dict)

        logger(
            item='whome',
            json=dumps(fetch))

        self.__mynick = (
            (fetch['username']
             .lstrip('@')),
            fetch['id'])

        self.__lsnick = (
            (fetch['username']
             .lstrip('@')),
            fetch['id'])


    def socket_send(
        self,
        send: DictStrAny,
    ) -> None:
        """
        Transmit provided content through the socket connection.

        :param send: Content which will be sent through socket.
        """

        logger = self.__logger
        exited = self.__exited
        socket = self.__socket

        if socket is None:
            return NCNone

        transmit = dumps(send)

        logger(
            item='transmit',
            value=transmit)

        try:
            socket.send(transmit)

        except ConnectionClosedOK:
            exited.set()
            return None


    def socket_recv(  # noqa: CFQ004
        self,
    ) -> Optional[DictStrAny]:
        """
        Return the content received from the socket connection.

        :returns: Content received from the socket connection.
        """

        logger = self.__logger
        exited = self.__exited
        socket = self.__socket

        if socket is None:
            return NCNone


        try:

            recv = socket.recv(1)

            logger(
                item='receive',
                value=recv)

        except TimeoutError:
            return None

        except ConnectionClosedOK:
            exited.set()
            return None


        event = loads(recv)

        assert isinstance(event, dict)

        type = event.get('event')

        if type == 'discon':
            exited.set()

        return sort_dict(event)


    def request(
        self,
        method: _METHODS,
        path: str,
        params: Optional[_PAYLOAD] = None,
        json: Optional[_PAYLOAD] = None,
        *,
        timeout: Optional[int] = None,
    ) -> Response:
        """
        Return the response for upstream request to the server.

        :param method: Method for operation with the API server.
        :param path: Path for the location to upstream endpoint.
        :param params: Optional parameters included in request.
        :param json: Optional JSON payload included in request.
        :param timeout: Timeout waiting for the server response.
            This will override the default client instantiated.
        :returns: Response from upstream request to the server.
        """

        params = dict(params or {})
        json = dict(json or {})

        logger = self.__logger
        client = self.__client

        _params = self.__params
        server = _params.server
        port = _params.port
        token = _params.token

        address = f'{server}:{port}'
        tokey = 'Authorization'
        content = 'application/json'

        headers = {
            tokey: f'Bearer {token}',
            'Content-Type': content}

        location = (
            f'https://{address}'
            f'/api/v4/{path}')

        request = client.request_block

        logger(
            item='request',
            method=method,
            path=path,
            params=params,
            json=(
                dumps(json)
                if len(json) >= 1
                else None))

        return request(
            method=method,
            location=location,
            params=params,
            headers=headers,
            json=json,
            timeout=timeout)
