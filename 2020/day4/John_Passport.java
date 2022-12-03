import java.util.HashMap;

public class John_Passport {
    private String byr,iyr,eyr,cid;
    private String ecl,hcl,pid,hgt;

    public John_Passport(HashMap<String, String> inputMap) {
        this.byr = inputMap.get("byr");
        this.iyr = inputMap.get("iyr");
        this.eyr = inputMap.get("eyr");
        this.cid = inputMap.get("cid");
        this.ecl = inputMap.get("ecl");
        this.hcl = inputMap.get("hcl");
        this.pid = inputMap.get("pid");
        this.hgt = inputMap.get("hgt");
    }

    public boolean isDataPresent(){
        return (byr!=null & iyr!=null & eyr!=null & ecl!=null & hcl!=null & pid!=null & hgt!=null);
    }

    public boolean isValid(){
        boolean check = true;
        if (this.isDataPresent()){
            try{
                //byr Check
                int birthYear = Integer.parseInt(byr);
                if (birthYear<1920 || birthYear>2002) check = false;
                //iyr Check
                int issueYear = Integer.parseInt(iyr);
                if (issueYear<2010 || issueYear>2020) check = false;
                //eyr Check
                int expYear = Integer.parseInt(eyr);
                if (expYear<2020 || expYear>2030) check = false;
                //hgt Check
                if (hgt.endsWith("cm")){
                    int hgtNum = Integer.parseInt(hgt.split("cm")[0]);
                    if (hgtNum<150 || hgtNum>193) check = false;
                } else if(hgt.endsWith("in")){
                    int hgtNum = Integer.parseInt(hgt.split("in")[0]);
                    if (hgtNum<59 || hgtNum>76) check = false;
                } else{ check = false;}
                //hcl Check
                if (hcl.startsWith("#") & hcl.length()==7) {
                    for (char letter : hcl.replace("#","").toCharArray())
                        if ((letter < '0' || letter > '9') & (letter < 'a' || letter > 'f')) check = false;
                }else {check =false;}
                //ecl Check
                if (!ecl.equals("amb")& !ecl.equals("blu") & !ecl.equals("brn")& !ecl.equals("gry")
                        & !ecl.equals("grn")& !ecl.equals("hzl")& !ecl.equals("oth")) check=false;
                //pid check
                int pidInt = Integer.parseInt(pid);
                if (pid.length()!=9) check=false;
            } catch (Exception e) {check = false;}
        } else {check = false;}
        return check;
    }
}
