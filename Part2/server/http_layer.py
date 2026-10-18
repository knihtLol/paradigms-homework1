
from http.server import BaseHTTPRequestHandler
from typing import Any

from soap import handle


class Handler(BaseHTTPRequestHandler):
    wsdl_path = 'gen/ChatRoom.wsdl'

    def _send(self, code: int, payload: bytes,
              ctype: str = 'text/xml; charset=utf-8') -> None:
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        try:
            with open(self.wsdl_path, 'rb') as f:
                self._send(200, f.read())
        except OSError:
            self._send(404, b'WSDL file not found', 'text/plain')

    def do_POST(self) -> None:
        length = int(self.headers.get('Content-Length', 0))
        code, payload = handle(self.rfile.read(length))
        self._send(code, payload)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f'{self.address_string()} {fmt % args}')