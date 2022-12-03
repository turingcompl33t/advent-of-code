import java.util.ArrayList;
import java.util.Collections;
import java.util.TreeSet;

public class John_CustomsGroup {
    private ArrayList<Character> answers = new ArrayList<>();
    private TreeSet<Character> allAnswers = new TreeSet<>();
    private TreeSet<Character> sharedAnswers = new TreeSet<>();
    private int numPeople;

    public John_CustomsGroup(int numPeople, ArrayList<Character> ansArray){
        Collections.sort(ansArray);
        this.answers = ansArray;
        this.numPeople = numPeople;
        for (Character someAns : ansArray){
            this.allAnswers.add(someAns);
            if (ansArray.lastIndexOf(someAns)-ansArray.indexOf(someAns)==numPeople-1){
                sharedAnswers.add(someAns);
            }
        }
    }

    public TreeSet<Character> getAllAnswers() { return allAnswers; }
    public TreeSet<Character> getSharedAnswers() { return sharedAnswers; }
}
