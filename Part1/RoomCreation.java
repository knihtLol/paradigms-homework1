import java.io.*;
import java.net.Socket;
import java.util.*;


public class RoomCreation {
    InputStream in;
    OutputStream out;
    BufferedReader headerReader;
    BufferedWriter headerWriter;
    static Rooms room;
    String header = null;

    public RoomCreation(Socket socket) throws Exception{
        in = socket.getInputStream();
        out = socket.getOutputStream();
        headerReader = new BufferedReader(new InputStreamReader(in));
        headerWriter = new BufferedWriter(new OutputStreamWriter(out));
        room = create();

        switch (room.getName()) {
            case "WRONG":
                header = "ERROR 111\n";
                headerWriter.write(header);
                headerWriter.flush();
            break;
            case "NULL":
                header = "ERROR 101\n";
                break;
            default:
                store(room);
                header = "CREATED\n";
                display();
                break;
        }
        headerWriter.write(header);
        headerWriter.flush();
    }

    public final Rooms create() throws IOException{
        header = headerReader.readLine();
        Rooms newRoom;
        if (header == null) {
            return new Rooms("NULL", "NULL");
        }

        StringTokenizer stk = new StringTokenizer(header, "//");
        if (stk.countTokens() < 3) {
            return new Rooms("WRONG", "WRONG");
        }

        if(stk.nextToken().equals("CREATEROOM")){
            String name = stk.nextToken();
            String description = stk.nextToken();
            if(name.isEmpty() || description.isEmpty()){
                newRoom = new Rooms("WRONG", "WRONG");
            }else{
                newRoom = new Rooms(name, description);
            }
        }else{
            newRoom = new Rooms("NULL", "NULL");
        }
        return newRoom;
    }

        static Node head= null;
        static int roomCount = 0;

    public final void store(Rooms newRoom){

    
        Node newNode = new Node(newRoom);

        if (head == null) {
            head = newNode;
        } else {
            Node current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        roomCount++;
    }

    public static synchronized void display() {
        System.out.println("---- Rooms (" + roomCount + ") ----");

        if (head == null) {
            System.out.println("No rooms yet.");
            return;
        }

        Node current = head;
        while (current != null) {
            Rooms r = current.room;
            System.out.println("ID: " + r.getId() + " | Name: " + r.getName() + " | Description: " + r.getDescription());
            current = current.next;
        }
        System.out.println("---------------------");
    }
}




