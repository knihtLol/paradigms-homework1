
from typing import Any, Dict, List

accounts: Dict[str, str] = {}                  # username -> password
sessions: Dict[str, str] = {}                  # session token -> username
rooms: Dict[str, Dict[str, Any]] = {}          # room name -> room record
inboxes: Dict[str, List[Dict[str, Any]]] = {}  # username -> list of messages


counters = {'next_room_id': 1}