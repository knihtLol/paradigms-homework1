
import secrets
from typing import Any, Callable, Dict, List, Optional, Tuple

import state  # the shared data

Reply = Dict[str, Any]
Params = Dict[str, str]



def user_of(token: Optional[str]) -> Optional[str]:
    return state.sessions.get(token or '')

def ok(**extra: Any) -> Reply:
    return {'success': True, **extra}

def err(msg: str, **extra: Any) -> Reply:
    return {'success': False, 'error': msg, **extra}



def check_member(token: Optional[str], room_name: Optional[str]
                 ) -> Tuple[Optional[str], Optional[Dict[str, Any]], Optional[str]]:
    user = user_of(token)
    if user is None:
        return (None, None, 'invalid session')
    room = state.rooms.get(room_name or '')
    if room is None:
        return (user, None, 'no such room')
    if user not in room['members']:
        return (user, room, 'you have not joined this room')
    return (user, room, None)

def deliver(to: str, sender: str, room_name: str, text: str, private: bool) -> None:
    state.inboxes.setdefault(to, []).append(
        {'sender': sender, 'roomName': room_name, 'isPrivate': private, 'text': text}
    )



def CreateAccount(p: Params) -> Reply:
    username, password = (p.get('username'), p.get('password'))
    if not username or not password:
        return err('invalid username or password')
    if username in state.accounts:
        return err('username already taken')
    state.accounts[username] = password
    return ok()

def LogIn(p: Params) -> Reply:
    username, password = (p.get('username') or '', p.get('password'))
    if not password or state.accounts.get(username) != password:
        return err('wrong username or password')
    token = secrets.token_hex(16)
    state.sessions[token] = username
    return ok(sessionToken=token)

def CreateRoom(p: Params) -> Reply:
    name, desc = (p.get('roomName'), p.get('roomDescription') or '')
    if user_of(p.get('token')) is None:
        return err('invalid session')
    if not name:
        return err('invalid room name')
    if name in state.rooms:
        return err('room name already exists')
    state.rooms[name] = {'id': state.counters['next_room_id'],
                         'description': desc, 'members': []}
    room = {'roomId': state.counters['next_room_id'],
            'roomName': name, 'roomDescription': desc}
    state.counters['next_room_id'] += 1
    return ok(room=room)

def ListRooms(p: Params) -> Reply:
    if user_of(p.get('token')) is None:
        return err('invalid session')
    return ok(rooms={'room': [{'roomId': r['id'], 'roomName': n,
                               'roomDescription': r['description']}
                              for n, r in state.rooms.items()]})

def JoinRoom(p: Params) -> Reply:
    user = user_of(p.get('token'))
    if user is None:
        return err('invalid session')
    room = state.rooms.get(p.get('roomName') or '')
    if room is None:
        return err('no such room')
    if user in room['members']:
        return err('already in room')
    room['members'].append(user)
    return ok()

def DisplayJoined(p: Params) -> Reply:
    _, room, problem = check_member(p.get('token'), p.get('roomName'))
    if problem:
        return err(problem)
    return ok(usernames={'item': list(room['members'])})

def Broadcast(p: Params) -> Reply:
    user, room, problem = check_member(p.get('token'), p.get('roomName'))
    if problem:
        return err(problem)
    text = p.get('message')
    if not text:
        return err('empty message')
    for member in room['members']:
        if member != user:
            deliver(member, user, p['roomName'], text, False)
    return ok()

def SendPrivate(p: Params) -> Reply:
    user, room, problem = check_member(p.get('token'), p.get('roomName'))
    if problem:
        return err(problem)
    receiver, text = (p.get('receiver'), p.get('message'))
    if receiver not in room['members']:
        return err('receiver is not in this room')
    if not text:
        return err('empty message')
    deliver(receiver, user, p['roomName'], text, True)
    return ok()

def Leave(p: Params) -> Reply:
    user, room, problem = check_member(p.get('token'), p.get('roomName'))
    if problem:
        return err(problem)
    room['members'].remove(user)
    return ok()

def LogOut(p: Params) -> Reply:
    token = p.get('token')
    user = user_of(token)
    if user is None:
        return err('invalid session')
    for room in state.rooms.values():
        if user in room['members']:
            room['members'].remove(user)
    del state.sessions[token]
    return ok()

def GetMessages(p: Params) -> Reply:
    user = user_of(p.get('token'))
    if user is None:
        return err('invalid session')
    return ok(messages={'message': state.inboxes.pop(user, [])})



OPERATIONS: Dict[str, Callable[[Params], Reply]] = {
    f.__name__: f for f in (CreateAccount, LogIn, CreateRoom, ListRooms,
                            JoinRoom, DisplayJoined, Broadcast, SendPrivate,
                            Leave, LogOut, GetMessages)
}