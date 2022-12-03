import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class John_day2 {
    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day2 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        //Data Test 1
        int passedTest = 0;
        for (String[] input : loadInput("Input.txt")){
            int lowerBound = Integer.parseInt(input[0]);
            int upperBound = Integer.parseInt(input[1]);
            char keyChar = input[2].charAt(0);
            char[] password = input[3].toCharArray();
            int charCount = 0;
            for (char pass : password){
                if (pass == keyChar){
                    charCount++;
                }
            }
            if (charCount>=lowerBound & charCount<=upperBound){
                passedTest++;
            }
        }
        System.out.println("I found "+passedTest+" cases that passed the first test.");
        //Data Test 2
        passedTest = 0;
        for (String[] input : loadInput("Input.txt")){
            int posCheck = Integer.parseInt(input[0]);
            int negCheck = Integer.parseInt(input[1]);
            char keyChar = input[2].charAt(0);
            char[] password = input[3].toCharArray();
            if (password[posCheck-1]==keyChar ^ password[negCheck-1]==keyChar){
                passedTest++;
            }
        }
        System.out.println("I found "+passedTest+" cases that passed the second test.");
    }

    public static ArrayList<String[]> loadInput(String fileName) {
        ArrayList<String[]> inputArray = new ArrayList<>();
        File inputFile = new File(fileName);
        try{
            Scanner fileScanner = new Scanner(inputFile);
            while (fileScanner.hasNextLine()){
                String[] initSplit = fileScanner.nextLine().split(": ");
                String[] secondSplit = initSplit[0].split(" ");
                String[] thirdSplit = secondSplit[0].split("-");
                String[] input = {thirdSplit[0], thirdSplit[1],secondSplit[1],initSplit[1]};
                inputArray.add(input);
            }
            System.out.println("File successfully loaded");
            return inputArray;
        } catch (FileNotFoundException e) {
            System.out.println("File failed to Load");
            return null;
        }
    }
}

