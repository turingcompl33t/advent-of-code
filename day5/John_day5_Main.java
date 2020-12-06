import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class John_day5_Main {

    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day5 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        //Load the data and sort using compareTo() method
        ArrayList<John_BoardingPass> boardingPasses = loadInput("Input.txt");
        Collections.sort(boardingPasses);
        //Part 1. Top entry is highest SeatID
        John_BoardingPass topPass= boardingPasses.get(0);
        System.out.println("The top pass is row "+topPass.getRow()+" and seat# "+topPass.getSeat());
        System.out.println("It's seatID is "+topPass.getSeatID()+"\n");
        //Part 2. Use CompareTo() to find missing boarding passes
        for (int i =1;i<boardingPasses.size();i++){
            John_BoardingPass thisBoardingPass = boardingPasses.get(i);
            John_BoardingPass lastBoardingPass = boardingPasses.get(i-1);
            if (thisBoardingPass.compareTo(lastBoardingPass)!=1) {
                System.out.println("There's a missing boarding pass between "+thisBoardingPass.getSeatID()+
                        " and "+lastBoardingPass.getSeatID());
            }
        }
    }

    public static ArrayList<John_BoardingPass> loadInput(String filename){
        ArrayList<John_BoardingPass> boardingPasses = new ArrayList<>();
        File file = new File(filename);
        try{
            Scanner fileScanner = new Scanner(file);
            while (fileScanner.hasNextLine()){
                John_BoardingPass someBoardingPass = new John_BoardingPass(fileScanner.nextLine().toCharArray());
                boardingPasses.add(someBoardingPass);
            }
            System.out.println("File loaded "+boardingPasses.size()+" boarding passes.\n");
        } catch (FileNotFoundException e) {
            System.out.println("File failed to load.\n");
        }
        return boardingPasses;
    }
}
