import javax.print.DocFlavor;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class John_day4_Main {
    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day4 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        int validCounter = 0;
        int presentCounter = 0;
        for (John_Passport passport : loadInput("Input.txt")){
            if (passport.isDataPresent()){
                presentCounter++;
            }
            if (passport.isValid()){
                validCounter++;
            }
        }
        System.out.println("I found "+presentCounter+" passports with all data present.");
        System.out.println("I found "+validCounter+" valid passports.");
    }

    public static ArrayList<John_Passport> loadInput(String filename){
        ArrayList<John_Passport> passports = new ArrayList();
        File file =new File(filename);
        try {
            Scanner fileScanner = new Scanner(file);
            HashMap<String, String> inputMap = new HashMap<>();
            while (fileScanner.hasNextLine()){
                String inputLine = fileScanner.nextLine();
                if (!inputLine.equals("")){
                    //if nextLine() has values, continue to add to current HashMap
                    for (String entry : inputLine.split(" ")) {
                        String[] entryValue = entry.split(":");
                        inputMap.put(entryValue[0],entryValue[1]);
                    }
                }else {
                    //if nextLine() has no values, create Passport and reset HashMap
                    passports.add(new John_Passport(inputMap));
                    inputMap = new HashMap<>();
                }
            }
            passports.add(new John_Passport(inputMap));
            System.out.println("File successfully loaded " +passports.size()+" passports.\n");
        } catch (FileNotFoundException e) {
            System.out.println("File failed to load.\n");
        }
        return passports;
    }
}
