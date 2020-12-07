import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.TreeSet;

public class John_Day6_Main {
    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day6 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        ArrayList<John_CustomsGroup> customGroups = loadInput("Input.txt");
        int sizeCounter=0; int sharedCounter =0;
        for (John_CustomsGroup someCustomGroup : customGroups){
            StringBuilder sb = new StringBuilder();
            for (Character someChar : someCustomGroup.getAllAnswers()){
                sb.append(someChar);
            }
            System.out.printf("Group: %-26s || size: %2d || shared: %2d\n",sb.toString(),someCustomGroup.getAllAnswers().size(),someCustomGroup.getSharedAnswers().size());
            sizeCounter+= someCustomGroup.getAllAnswers().size();
            sharedCounter+= someCustomGroup.getSharedAnswers().size();
        }
        System.out.println("\nThe total unique sum is "+sizeCounter);
        System.out.println("The total shared sum is "+sharedCounter);
    }

    public static ArrayList<John_CustomsGroup> loadInput(String filename) {
        ArrayList<John_CustomsGroup> customsGroups = new ArrayList<>();
        File file = new File(filename);
        try {
            Scanner fileScanner = new Scanner(file);
            ArrayList<Character> inputArr = new ArrayList<>(); int numPeople=0;
            while (fileScanner.hasNextLine()) {
                String inputLine = fileScanner.nextLine();
                if (!inputLine.equals("")) {
                    //if nextLine() has values, continue to add to current ArrayList
                    numPeople++;
                    for (char question : inputLine.toCharArray()) {
                        inputArr.add(question);
                    }
                } else{
                    //if nextLine() has no values, create a CustomsGroup and reset ArrayList & counter
                    customsGroups.add( new John_CustomsGroup(numPeople, inputArr));
                    inputArr = new ArrayList<>(); numPeople=0;
                }
            }
            customsGroups.add( new John_CustomsGroup(numPeople, inputArr));
            System.out.println("File successfully loaded "+customsGroups.size()+" custom groups.\n");
        } catch (FileNotFoundException e) {
            System.out.println("File failed to load.\n");
        }
        return customsGroups;
    }
}
