//gsoap ns service name:      ChatRoom
//gsoap ns service style:     rpc
//gsoap ns service encoding:  literal
//gsoap ns service namespace: urn:ChatRoom
//gsoap ns service location:  http://localhost:8080
//gsoap ns schema namespace:  urn:ChatRoom


struct ns__Result {
    bool  success;
    char *error;
};

struct ns__SessionInfo {
    bool  success;
    char *sessionToken;
    char *error;
};

struct ns__Room {
    int   roomId;
    char *roomName;
    char *roomDescription;
};

struct ns__RoomInfo {
    bool  success;
    struct ns__Room room;
    char *error;
};

struct ns__Message {
    char   *sender;
    char   *roomName;
    bool    isPrivate;
    char   *text;
};

struct ns__StringList {
    int __sizeitem;
    char **item;
};

struct ns__RoomArray {
    int __sizeroom;
    struct ns__Room *room;
};

struct ns__MessageArray {
    int __sizemessage;
    struct ns__Message *message;
};

struct ns__RoomList {
    bool success;
    char *error;
    struct ns__RoomArray rooms;
};

struct ns__UserList {
    bool success;
    char *error;
    struct ns__StringList usernames;
};

struct ns__MessageList {
    bool success;
    char *error;
    struct ns__MessageArray messages;
};


int ns__CreateAccount (char *username, char *password, struct ns__Result *result);
int ns__LogIn (char *username, char *password, struct ns__SessionInfo *result);
int ns__CreateRoom (char *token, char *roomName, char *roomDescription, struct ns__RoomInfo *result);
int ns__ListRooms (char *token, struct ns__RoomList *result);
int ns__JoinRoom (char *token, char *roomName, struct ns__Result *result);
int ns__DisplayJoined (char *token, char *roomName, struct ns__UserList *result);
int ns__Broadcast (char *token, char *roomName, char *message, struct ns__Result *result);
int ns__SendPrivate (char *token, char *roomName, char *receiver, char *message, struct ns__Result *result);
int ns__Leave (char *token, char *roomName, struct ns__Result *result);
int ns__LogOut (char *token, struct ns__Result *result);
int ns__GetMessages (char *token, struct ns__MessageList *result);