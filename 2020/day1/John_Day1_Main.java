public class John_Day1_Main {
    public static void main(String[] args) {
        System.out.println("################################");
        System.out.println("##### ADVENT OF CODE: Day1 #####");
        System.out.println("################################");
        System.out.println("\t\tby: @jtmccorm");
        System.out.println("");
        //load data
        John_Day1_Input myInput = new John_Day1_Input("Input.txt");

        System.out.println("\n### Part 1 ###\n");
        int num1, num2, ans;
        for (int i=0; i<myInput.getIntList().size(); i++){
            for (int j=0; j<myInput.getIntList().size(); j++){
                if (myInput.getIntList().get(i) + myInput.getIntList().get(j) ==2020){
                    num1 = myInput.getIntList().get(i);
                    num2 = myInput.getIntList().get(j);
                    ans = num1*num2;
                    System.out.println(num1+", "+num2+", "+ans);
                }
            }
        }
        System.out.println("\n### Part 2 ###\n");
        int num3;
        for (int i=0; i<myInput.getIntList().size(); i++) {
            for (int j = 0; j < myInput.getIntList().size(); j++) {
                for (int k = 0; k < myInput.getIntList().size(); k++) {
                    if (myInput.getIntList().get(i) + myInput.getIntList().get(j) + myInput.getIntList().get(k) == 2020) {
                        num1 = myInput.getIntList().get(i);
                        num2 = myInput.getIntList().get(j);
                        num3 = myInput.getIntList().get(k);
                        ans = num1*num2*num3;
                        System.out.println(num1+", "+num2+", "+num3+", "+ans);
                    }
                }
            }
        }
    }

}
