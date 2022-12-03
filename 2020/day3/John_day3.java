import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class John_day3 {
    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day3 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        ArrayList<char[]> slopeArray = loadInput("Input.txt");
        long path1 = slopeCheck(1,1,slopeArray);
        long path2 = slopeCheck(3,1,slopeArray);
        long path3 = slopeCheck(5,1,slopeArray);
        long path4 = slopeCheck(7,1,slopeArray);
        long path5 = slopeCheck(1,2,slopeArray);
        System.out.println("\nThat's a total off: "+path1*path2*path3*path4*path5);

    }

    public static ArrayList<char[]> loadInput(String fileName){
        ArrayList<char[]> inputArray = new ArrayList<>();
        File inputFile = new File(fileName);
        try {
            Scanner fileScanner = new Scanner(inputFile);
            while (fileScanner.hasNextLine()){
                char[] inputRow = fileScanner.nextLine().toCharArray();
                inputArray.add(inputRow);
            }
            System.out.println("File successfully loaded");
            return inputArray;
        } catch (FileNotFoundException e) {
            System.out.println("File failed to Load.");
            return null;
        }
    }

    public static long slopeCheck(int rightStep, int downStep, ArrayList<char[]> slopeArray){
        int impactCount=0;
        int lateralPos=0;
        for (int i=0; i<slopeArray.size();i+=downStep){
            char[] slope = slopeArray.get(i);
            if( slope[lateralPos % slope.length] == '#'){
                impactCount++;
            }
            lateralPos+=rightStep;
        }
        System.out.println("On a path of Right "+rightStep+" and Down "+downStep +" you would make "+impactCount+" collisions.");
        return (long) impactCount;
    }
}
