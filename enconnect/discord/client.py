"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from json import loads
from queue import Queue
from threading import Event
from time import sleep as block_sleep
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer
from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types import getate
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
    'op': 1,
    'd': None}



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
    __resume: Event

    __ping: Optional[int]
    __path: Optional[str]
    __sesid: Optional[str]
    __seqno: Optional[int]

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
        self.__resume = Event()

        self.__ping = None
        self.__path = None
        self.__sesid = None
        self.__seqno = None

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
        *,
        intents: int = 4609,
    ) -> None:
        """
        Operate the client and populate queue with the messages.

        :param intents: Determine what content will be received.
        """

        logger = self.__logger

        try:

            logger(item='initial')

            self.__mynick = None

            self.__ping = None
            self.__path = None
            self.__sesid = None
            self.__seqno = None

            self.__setpath()

            while not self.canceled:

                logger(item='operate')

                self.__socket = None
                self.__conned.clear()
                self.__exited.clear()

                self.__cancel.clear()

                self.__operate(intents)

                block_sleep(1)

        finally:

            self.__socket = None
            self.__conned.clear()
            self.__exited.clear()
            self.__mynick = None

            self.__ping = None
            self.__path = None

            self.__cancel.clear()

            logger(item='finish')


    def __operate(
        self,
        intents: int,
    ) -> None:
        """
        Operate the client and populate queue with the messages.

        :param intents: Determine what content will be received.
        """

        logger = self.__logger
        resume = self.__resume


        self.__connect()

        socket = self.__socket

        assert socket is not None


        receive = (
            self.socket_recv())

        assert receive is not None

        self.__event(receive)


        beat = getate(
            receive,
            'd/heartbeat_interval')

        if beat is not None:
            self.__ping = beat / 1000


        ping = self.__ping

        if ping is None:  # NOCVR
            raise ConnectionError

        timer = Timer(ping)


        self.__identify(intents)


        def _continue() -> bool:

            return all([
                not resume.is_set()
                and not self.canceled])


        while _continue():

            receive = (
                self.socket_recv())

            if receive is not None:
                self.__event(receive)

            if timer.pause():
                continue  # NOCVR

            logger(item='ping')

            self.socket_send(PING)


        code = (
            4000
            if resume.is_set()
            else 1000)

        logger(
            item='close',
            code=code)

        socket.close(code)


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

        type = event.get('t')
        opcode = event.get('op')

        model = ClientEvent


        if opcode == 11:
            return None


        if type == 'READY':

            logger(item='helo')


            sesid = getate(
                event,
                'd/session_id')

            assert sesid is not None

            self.__sesid = sesid


            path = getate(
                event,
                'd/resume_gateway_url')

            if path is not None:
                self.__path = path


            user = getate(
                event, 'd/user')

            assert user is not None

            self.__mynick = (
                user['username'],
                user['id'])

            self.__lsnick = (
                user['username'],
                user['id'])


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


    def __setpath(
        self,
    ) -> None:
        """
        Collect and store the relevant path for the websockets.
        """

        request = self.request

        response = request(
            'get', 'gateway')

        (response
         .raise_for_status())


        fetch = response.json()

        assert isinstance(fetch, dict)

        path = fetch['url']


        self.__path = path


    def __connect(
        self,
    ) -> None:
        """
        Establish the connection with the upstream using socket.
        """

        logger = self.__logger
        path = self.__path

        assert path is not None

        logger(item='connect')

        socket = connect(path)

        self.__socket = socket

        self.__conned.set()
        self.__exited.clear()


    def __resumify(
        self,
    ) -> None:
        """
        Identify the client once the connection is established.

        :param intents: Determine what content will be received.
        :param client: Value for browser and device properties.
        """

        logger = self.__logger
        sesid = self.__sesid
        seqno = self.__seqno

        _params = self.__params
        token = _params.token

        data = {
            'token': token,
            'session_id': sesid,
            'seq': seqno}

        logger(item='resumify')

        self.socket_send({
            'op': 6, 'd': data})


    def __identify(
        self,
        intents: int,
        client: str = 'enconnect',
    ) -> None:
        """
        Identify the client once the connection is established.

        :param intents: Determine what content will be received.
        :param client: Value for browser and device properties.
        """

        logger = self.__logger
        resume = self.__resume

        if resume.is_set():

            resume.clear()

            self.__resumify()

            return None

        props = {
            '$os': 'linux',
            '$browser': client,
            '$device': client}

        _params = self.__params
        token = _params.token

        data = {
            'intents': intents,
            'properties': props,
            'token': token}

        logger(item='identify')

        self.socket_send({
            'op': 2, 'd': data})


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
        resume = self.__resume
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

        opcode = event.get('op')
        seqno = event.get('s')

        if seqno is not None:
            self.__seqno = seqno

        if opcode == 7:
            resume.set()

        if opcode == 9:
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
        token = _params.token

        tokey = 'Authorization'
        content = 'application/json'

        headers = {
            tokey: f'Bot {token}',
            'Content-Type': content}

        location = (
            'https://discord.com'
            f'/api/v10/{path}')

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
