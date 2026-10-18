import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.*;


public class CreateRoomClient {

    public static void main(String[] args) throws Exception{

        try(Socket connection = new Socket("localhost", 5000)){
            InputStream in = connection.getInputStream();
            OutputStream out = connection.getOutputStream();
            BufferedReader headerReader = new BufferedReader(new InputStreamReader(in));
            BufferedWriter headerWriter = new BufferedWriter(new OutputStreamWriter(out));
            String header;

            Scanner scanner = new Scanner(System.in);

            System.out.println("Enter your command: ");
            String command = scanner.nextLine();

            if (!command.equals("create room")){
                System.out.println("The command you entered is unvalid or does not match any of our operations\n");
                scanner.close();
                return;
            }

            System.out.println("Enter the name of your room: ");
            String rName = scanner.nextLine();

            System.out.println("Enter a description for your room:");
            String rDescription = scanner.nextLine();

            header = "CREATEROOM" + "//" + rName + "//" + rDescription +"\n";
            headerWriter.write(header);                headerWriter.flush();
            scanner.close();
            header = headerReader.readLine();

            if("CREATED".equals(header)){
                System.out.println("The room was created successfully\n");
            }else{
                System.out.println("Something went wrong, please try again");
            }
        }
    }
}
