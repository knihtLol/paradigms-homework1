
public class Rooms {
    private static int nextId = 12445;
    private String rName;
    private String rDescription;
    private int rId;
   

    public Rooms(String name, String description){
        this.rName = name;
        this.rDescription = description;
        this.rId = nextId++;
    }

    public String getName(){
        return rName;
    }

    public int getId(){
        return rId;
    }

    public String getDescription(){
        return rDescription;
    }
    public static void main(String[] args) {
    
        System.out.println("Room created successfully");
        
    }
}

 



