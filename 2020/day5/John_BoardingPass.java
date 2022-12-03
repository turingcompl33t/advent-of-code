import java.util.Arrays;

public class John_BoardingPass implements Comparable<John_BoardingPass>{
    private String ticket;
    private int row, seat;
    private int seatID;

    public John_BoardingPass(char[] input) {
        this.ticket = Arrays.toString(input);
        int lb = 0; int ub = 127;
        for (int i=0; i<7;i++){
            if (input[i]=='F') ub = (ub+lb)/2;
            if (input[i] =='B') lb = (ub+lb)/2+1;
        }
        this.row = lb;
        lb = 0; ub = 7;
        for (int i=7;i<10;i++){
            if (input[i]=='L') ub = (ub+lb)/2;
            if (input[i] =='R') lb = (ub+lb)/2+1;
        }
        this.seat =lb;
        this.seatID= row*8 + seat;
    }

    public String getTicket() { return ticket; }
    public int getRow() { return row; }
    public int getSeat() { return seat; }
    public int getSeatID() { return seatID; }

    @Override
    public int compareTo(John_BoardingPass other) {
        return other.seatID-this.seatID;
    }
}
