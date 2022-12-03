import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class John_Day1_Input {
    private ArrayList<Integer> intList = new ArrayList<>();
    private String fileName;

    public John_Day1_Input(String fileName){
        this.fileName = fileName;
        File file = new File(this.fileName);
        try {
            Scanner fileScanner = new Scanner(file);
            while (fileScanner.hasNextLine()){
                Integer nextNum = Integer.parseInt(fileScanner.nextLine());
                intList.add(nextNum);
            }
            System.out.println("File successfully Loaded");
        } catch (FileNotFoundException e) {
            System.out.println("File Failed to Load");
        }
    }

    public ArrayList<Integer> getIntList() {
        return intList;
    }
}
