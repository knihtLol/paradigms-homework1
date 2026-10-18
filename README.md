# paradigms-homework1

# Chat Room Homework

A two-part assignment on designing and implementing a multi-user chat room service.

| Part | Topic | Stack |
|------|-------|-------|
| [Part 1](Part1/) | Raw TCP text protocol and one implemented function (**Create room**) | Java sockets |
| [Part 2](Part2/) | Full chat room service defined by a formal contract | SOAP / WSDL, gSOAP, Python |

## Repository layout

```
.
├── ai_use_disclosure.txt      # Responsible-use-of-AI statement
├── Part1/
│   ├── Protocol.txt           # Text protocol specification
│   ├── System Architecture.pdf
│   ├── CreateRoomServer.java  # Listens on port 5000
│   ├── RoomCreation.java      # Parses requests, handles CREATEROOM
│   ├── Rooms.java, Node.java  # In-memory room list
│   └── CreateRoomClient.java  # Interactive client
└── Part2/
    ├── answers.txt            # Technology choice and contract language
    ├── my_chatApi.h           # Original hand-written C contract
    ├── soap_chatApi.h         # gSOAP version of the contract (input to soapcpp2)
    ├── gen/                   # soapcpp2 output, including ChatRoom.wsdl
    ├── server/                # Python SOAP server
    └── client.py              # Interactive Python client (zeep)
```

---

## Part 1: TCP text protocol

The client opens one TCP connection to the server on port 5000 and keeps it open for the whole session. Each request is a single header line, and each reply starts with a single header line. Fields are separated by `//`, and commands are upper case.

| Command | Request | Success reply |
|---------|---------|---------------|
| Register | `REGISTER//user//pass` | `REGISTERED` |
| Log in | `LOGIN//user//pass` | `OK//token` |
| Create room | `CREATEROOM//token//name//description` | `CREATED//roomId` |
| List rooms | `LISTROOMS//token` | `OK//n`, then `n` lines of `id//name//description` |
| Join room | `JOINROOM//token//roomId` | `JOINED` |

Errors are replies of the form `ERROR <code>`, for example `111` for a malformed request, `121` for a duplicate username, `131` for an invalid token, `141` for a duplicate room name and `151` for an unknown room. The full specification is in [`Part1/Protocol.txt`](Part1/Protocol.txt), and the architecture is described in [`Part1/System Architecture.pdf`](Part1/System%20Architecture.pdf).

Only the **create room** function is implemented in code.

### Run it

Requires a JDK (8 or newer).

```bash
cd Part1
javac *.java

# terminal 1
java CreateRoomServer

# terminal 2
java CreateRoomClient
```

At the `Enter your command:` prompt type `create room`, then enter a room name and a description.

---

## Part 2: SOAP chat room service

The contract is written as a gSOAP header ([`soap_chatApi.h`](Part2/soap_chatApi.h)). The `soapcpp2` compiler turns it into the WSDL and XML Schema in [`Part2/gen/`](Part2/gen/). The reasoning for choosing SOAP/WSDL is in [`Part2/answers.txt`](Part2/answers.txt).

### Operations

| Operation | Purpose |
|-----------|---------|
| `CreateAccount(username, password)` | Register a new user |
| `LogIn(username, password)` | Authenticate and receive a session token |
| `CreateRoom(token, roomName, roomDescription)` | Create a room |
| `ListRooms(token)` | List all rooms |
| `JoinRoom(token, roomName)` | Join a room |
| `DisplayJoined(token, roomName)` | List the users in a room |
| `Broadcast(token, roomName, message)` | Send a message to everyone in a room |
| `SendPrivate(token, roomName, receiver, message)` | Send a private message to one user |
| `Leave(token, roomName)` | Leave a room |
| `LogOut(token)` | End the session |
| `GetMessages(token)` | Poll for incoming messages |

### Server structure

The server uses only the Python standard library and keeps all state in memory, so data is lost when it stops.

| Module | Responsibility |
|--------|----------------|
| `main.py` | Entry point |
| `http_layer.py` | HTTP handling: `GET` serves the WSDL, `POST` receives SOAP requests |
| `soap.py` | Parses the XML request, dispatches to an operation, builds the reply envelope |
| `logic.py` | The eleven operations |
| `state.py` | Shared in-memory data |

### Run it

Requires Python 3.9 or newer. The client needs [`zeep`](https://docs.python-zeep.org/).

```bash
cd Part2
pip install zeep

# terminal 1: start the server from Part2 (default port 8080)
python server/main.py          # optional: python server/main.py <port> <path-to-wsdl>

# terminal 2: start the client, also from Part2
python client.py               # optional: python client.py <wsdl> <endpoint-url>
```

The server serves `gen/ChatRoom.wsdl` at `/?wsdl`, so start it from the `Part2` folder or pass the WSDL path explicitly.

Client commands:

```
register <user> <pass>      login <user> <pass>
createroom <name> <desc>    rooms
join <room>                 users <room>
say <room> <text>           pm <room> <user> <text>
poll                        leave <room>
logout                      quit
```

### Regenerate the contract

If you change the header, regenerate the WSDL with [gSOAP](https://www.genivia.com/):

```bash
cd Part2
soapcpp2 -c -d gen soap_chatApi.h
```

---


