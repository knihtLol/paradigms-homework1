import java.net.ServerSocket;
import java.net.Socket;

public class CreateRoomServer {
    public static int port= 5000;

    public static void main(String[] args) throws Exception{
        try(ServerSocket ss = new ServerSocket(port)){
            System.out.println("Server connecting to port:" + port);
            while(true){
                System.out.println("Server listen...");
                try(Socket socket = ss.accept()){
                    new RoomCreation(socket); 
                }
            }
        }
    }


}