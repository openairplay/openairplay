
import sys
import socket
import threading
from urllib.parse import urlparse

from requests.structures import CaseInsensitiveDict

from . import log
from ._version import __version__

RTSP_VERSION = "RTSP/1.0"
LINE_SPLIT = "\r\n"
HEADER_END = LINE_SPLIT * 2
USER_AGENT = f"OpenAirPlay/{__version__}"


class RTSPClient():
    def __init__(self, url):
        self.orig_url = url
        self.url = urlparse(url)

        # TODO check for no proto/scheme
        if self.url.scheme.lower() != "rtsp":
            raise ValueError(f"only supports rtsp urls")

        # TODO check and set default port
        # TODO warn against path components / use as base?

        self._cseq = 0 # packet sequence
        self._sock = None # TCP socket in use
        self._session_id = None

        self._thread = None

    @property
    def _remote_ip(self):
        return self.url.hostname

    @property
    def _remote_port(self):
        return self.url.port

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            raise RuntimeError(f"cannot start an already running RTSPClient")

        self._thread = threading.Thread(
            target=self.run,
        )
        log.debug(f"RTSPClient starting thread...")
        self._thread.start()

    def _connect_socket(self):
        try:
            self._sock = socket.create_connection(
                (self._remote_ip, self._remote_port)
            )
        except OSError as e:
            # TODO further useful detail extraction / retry
            log.error(f"RTSPClient socket connection failed: {e}")
            raise e

    @property
    def _default_request_headers(self):
        return CaseInsensitiveDict({
            "User-Agent": USER_AGENT,
        })

    def _recv_msg(self):
        if not self._sock:
            raise RuntimeError(f"RTSPClient socket not connected")
        try:
            status_line = None
            headers = CaseInsensitiveDict()
            header_data = b""
            body_data = b""
            while True:
                data = self._sock.recv(4096)
                header_data += data
                if HEADER_END.encode("ascii") in header_data:
                    # parse header's content-length to know how much more data to expect
                    header_data, body_data = header_data.split(HEADER_END.encode("ascii"), 1)
                    header_lines = header_data.decode().split(LINE_SPLIT)
                    status_line = header_lines.pop(0)
                    for line in header_lines:
                        name, value = line.split(":", 1)
                        headers[name.lower()] = value
                    break # stop parsing header
            # else:
            #     raise ValueError(f"remote end did not send complete header data")
            while len(body_data) < int(headers["content-length"]):
                # don't decode: could be binary plist
                data = self._sock.recv(4096)
                body_data += data
            return (status_line, headers, body_data)
        except OSError as e:
            # TODO determine if socket needs to be closed / reset
            # did not receive enough data to meet content-length
            raise e

    def _send_msg(self, method, args, content=None, version=None, headers={}):
        """Write a message to the server"""
        headline = f"{method.upper()} {args} {RTSP_VERSION}"

        headers = CaseInsensitiveDict({**self._default_request_headers, **headers})

        if content:
            if isinstance(content, str):
                content = content.encode("utf-8")
            if isinstance(content, bytes):
                headers["Content-Length"] = len(content)
            else:
                raise NotImplementedError(f"not sure how to encode {type(content)} for RTSP request")

        # TODO some other checks for matching method, args, and content

        headers["CSeq"] = self._cseq
        self._cseq += 1

        request_data = headline.encode("utf-8")
        for k, v in headers.items():
            request_data += f"{LINE_SPLIT}{k}: {v}".encode("utf-8")
        request_data += HEADER_END.encode("utf-8")
        if content:
            request_data += content

        self._sock.sendall(request_data)

    def _make_request(self, *args, **kwargs):
        self._send_msg(*args, **kwargs)
        return self._recv_msg()

    def run(self):
        try:
            if not self._sock:
                self._connect_socket()

        except Exception as e:
            # TODO
            raise e
