import sys
from typing import Any, List
from zeep import Client
WSDL = sys.argv[1] if len(sys.argv) > 1 else 'gen/ChatRoom.wsdl'
ENDPOINT = sys.argv[2] if len(sys.argv) > 2 else None
HELP = 'commands:\n  register <user> <pass>     login <user> <pass>\n  createroom <name> <desc>   rooms\n  join <room>                users <room>\n  say <room> <text>          pm <room> <user> <text>\n  poll                       leave <room>\n  logout                     quit'

def unwrap(response: Any) -> Any:
    return response if hasattr(response, 'success') else response.result

def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return list(value) if isinstance(value, (list, tuple)) else [value]

def show(name: str, result: Any) -> bool:
    if result.success:
        print(f'{name} OK')
        return True
    print(f'{name} failed: {result.error}')
    return False

def main() -> None:
    client = Client(WSDL)
    if ENDPOINT:
        service = client.create_service(next(iter(client.wsdl.bindings)), ENDPOINT)
    else:
        service = client.service
    token = ''
    print(HELP)
    while True:
        try:
            line = input('> ').strip()
        except EOFError:
            break
        if not line:
            continue
        cmd, _, rest = line.partition(' ')
        try:
            if cmd == 'quit':
                break
            elif cmd == 'help':
                print(HELP)
            elif cmd == 'register':
                username, password = rest.split()[:2]
                show('register', unwrap(service.CreateAccount(username, password)))
            elif cmd == 'login':
                username, password = rest.split()[:2]
                res = unwrap(service.LogIn(username, password))
                if show('login', res):
                    token = res.sessionToken
            elif cmd == 'createroom':
                name, _, desc = rest.partition(' ')
                res = unwrap(service.CreateRoom(token, name, desc))
                if show('createroom', res):
                    print('room id =', res.room.roomId)
            elif cmd == 'rooms':
                res = unwrap(service.ListRooms(token))
                if show('rooms', res):
                    for r in as_list(getattr(res.rooms, 'room', None)):
                        print(f'  [{r.roomId}] {r.roomName} - {r.roomDescription}')
            elif cmd == 'join':
                show('join', unwrap(service.JoinRoom(token, rest)))
            elif cmd == 'users':
                res = unwrap(service.DisplayJoined(token, rest))
                if show('users', res):
                    for u in as_list(getattr(res.usernames, 'item', None)):
                        print('  ' + u)
            elif cmd == 'say':
                room, _, text = rest.partition(' ')
                show('say', unwrap(service.Broadcast(token, room, text)))
            elif cmd == 'pm':
                room, user, text = (rest.split(' ', 2) + ['', ''])[:3]
                show('pm', unwrap(service.SendPrivate(token, room, user, text)))
            elif cmd == 'poll':
                res = unwrap(service.GetMessages(token))
                if res.success:
                    for m in as_list(getattr(res.messages, 'message', None)):
                        tag = ' (private)' if m.isPrivate else ''
                        print(f'  [{m.roomName}]{tag} {m.sender}: {m.text}')
                else:
                    print('poll failed:', res.error)
            elif cmd == 'leave':
                show('leave', unwrap(service.Leave(token, rest)))
            elif cmd == 'logout':
                if show('logout', unwrap(service.LogOut(token))):
                    token = ''
            else:
                print("unknown command (type 'help')")
        except ValueError:
            print("wrong number of arguments (type 'help')")
        except Exception as exc:
            print('error:', exc)
if __name__ == '__main__':
    main()