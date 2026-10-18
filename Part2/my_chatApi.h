#include <stdbool.h>
#include <stdint.h>
#include <time.h>

//Types

typedef struct {
    char username[100];
    char passsword[100];
}User;

typedef struct{
    char roomName[100];
    char roomDescription[1000];
    int roomId;
}Room;

typedef struct {
    bool success;
    char sessionToken[50];
    char error[50];
}SessionInfos;

typedef struct{
    char message[1000];
    time_t timestamp;
}Message;

typedef struct {
    Room rooms[50];
    int roomCount;
} Listrooms;

typedef struct {
    char usernames[50][100];
    int userCount;
} UserList;

//Prototypes

User CreateAccount(char* username, char* password);

SessionInfos LogIn(char* username, char* password);

Room CreateRoom(char* token, char* Rname, char* Rdescription);

Listrooms ListRooms(char* token);

SessionInfos JoinRoom(char* token, char* rRame, char* uName);

UserList DisplayJoined(char* token, char* rName, char* user);

bool Broadcast(char* token, char* rRame, char* message);

bool SendPrivate(char* token, char* receiver, char* message);

bool Leave(char* rRame, char* token);

bool LogOut(char* token);