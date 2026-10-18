
import datetime
import xml.etree.ElementTree as ET
from typing import Any, Dict, Tuple
from xml.sax.saxutils import escape

from logic import OPERATIONS

NS = 'urn:ChatRoom'
ENV = 'http://schemas.xmlsoap.org/soap/envelope/'


def local(tag: str) -> str:
    return tag.rsplit('}', 1)[-1]

def render(name: str, value: Any) -> str:
    if value is None:
        return f'<{name} xsi:nil="true"/>'
    if isinstance(value, list):
        return ''.join((render(name, item) for item in value))
    if isinstance(value, dict):
        inner = ''.join((render(k, v) for k, v in value.items()))
    elif isinstance(value, bool):
        inner = 'true' if value else 'false'
    elif isinstance(value, datetime.datetime):
        inner = value.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        inner = escape(str(value))
    return f'<{name}>{inner}</{name}>'



EMPTY_ROOM = {'roomId': 0, 'roomName': None, 'roomDescription': None}
RESULT = [('success', None), ('error', None)]

SCHEMA = {
    'CreateAccount': RESULT, 'JoinRoom': RESULT, 'Broadcast': RESULT,
    'SendPrivate': RESULT, 'Leave': RESULT, 'LogOut': RESULT,
    'LogIn': [('success', None), ('sessionToken', None), ('error', None)],
    'CreateRoom': [('success', None), ('room', EMPTY_ROOM), ('error', None)],
    'ListRooms': [('success', None), ('error', None), ('rooms', {'room': []})],
    'DisplayJoined': [('success', None), ('error', None), ('usernames', {'item': []})],
    'GetMessages': [('success', None), ('error', None), ('messages', {'message': []})],
}

def render_result(op: str, result: Dict[str, Any]) -> str:
    return ''.join(render(f, result.get(f, d)) for f, d in SCHEMA[op])



def envelope(body: str) -> bytes:
    return (f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<SOAP-ENV:Envelope xmlns:SOAP-ENV="{ENV}" xmlns:ns="{NS}" '
            f'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<SOAP-ENV:Body>{body}</SOAP-ENV:Body></SOAP-ENV:Envelope>').encode()

def fault(message: str) -> bytes:
    return envelope(f'<SOAP-ENV:Fault><faultcode>SOAP-ENV:Client</faultcode>'
                    f'<faultstring>{escape(message)}</faultstring></SOAP-ENV:Fault>')



def handle(request_xml: bytes) -> Tuple[int, bytes]:
    try:
        root = ET.fromstring(request_xml)
        body = next((el for el in root if local(el.tag) == 'Body'))
        call = next(iter(body))
    except (ET.ParseError, StopIteration):
        return (400, fault('malformed SOAP request'))
    op = local(call.tag)
    func = OPERATIONS.get(op)
    if func is None:
        return (500, fault(f'unknown operation {op}'))
    params = {local(c.tag): c.text or '' for c in call}
    result = func(params)
    fields = render_result(op, result)
    return (200, envelope(f'<ns:{op}Response>{fields}</ns:{op}Response>'))