import java.io.File;
import java.util.HashMap;
import java.util.Scanner;

public class John_day7_main {
    static HashMap<String, HashMap<String, Integer>> allBagsMap = new HashMap<>();
    public static void main(String[] args) {
        //It's not good code without a nice banner
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day7 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        loadInput("Input.txt");
        int containsCounter = 0;
        for (String someColor: allBagsMap.keySet()){
            if (contains(someColor,"shiny gold")) containsCounter++;
        }
        System.out.println("There are "+containsCounter+" sets of bags that contain 'shiny gold.'");
        System.out.println("There are "+bagsInside("shiny gold")+" bags inside 'shiny gold.'");
    }

    public static void loadInput(String filename){
        File file = new File(filename);
        try{
            Scanner fileScanner = new Scanner(file);
            String color; HashMap<String, Integer> contents = new HashMap<>();
            while (fileScanner.hasNextLine()){
                String inputString = fileScanner.nextLine();
                String[] firstSplit = inputString.split("bags contain");
                color = firstSplit[0].trim();
                if (firstSplit[1].equals(" no other bags.")) {
                    allBagsMap.put(color, null);
                    continue;
                }
                String[] secondSplit = firstSplit[1].split(",");
                for (String content: secondSplit){
                    String[] thirdSplit = content.split(" ");
                    contents.put(thirdSplit[2]+" "+thirdSplit[3], Integer.parseInt(thirdSplit[1]));
                }
                allBagsMap.put(color, contents);
                contents = new HashMap<>();
            }
            System.out.println("File loaded "+allBagsMap.size()+" colored bags.");
        } catch (Exception e) {
            System.out.println("File failed to load.");
        }
    }

    public static boolean contains(String someColor, String myColor){
        HashMap<String, Integer> someContents = allBagsMap.get(someColor);
        if (someContents==null) return false;
        if (someContents.containsKey(myColor)) return true;
        boolean check = false;
        for (String containedColor: someContents.keySet()){
            check= check || contains(containedColor,myColor);
        }
        return check;
    }

    public static int bagsInside(String myColor){
        HashMap<String, Integer> myContents = allBagsMap.get(myColor);
        if (myContents==null) return 0;
        int tot = 0;
        for (String containedColor: myContents.keySet()){
            tot += myContents.get(containedColor)*(1+bagsInside(containedColor));
        }
        return tot;
    }

}
