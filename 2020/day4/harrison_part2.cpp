#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
#include <cmath>

using namespace std;

int main(int argc, char* argv[]) {
    string input(argv[1]);
    int count = 0;
    int i;
    string line;
    //list of valid values, as expressed in regex - regex101.com helps a lot
    vector<string> fields = 
        {"byr:(19[2-9]\\d|200[0-2])\\b", 
        "iyr:20(1\\d|20)\\b", 
        "eyr:20(2\\d|30)\\b", 
        "hgt:(1([5-8]\\d|9[0-3])cm|(59|6\\d|7[0-6])in)\\b", 
        "hcl:#[a-f\\d]{6}\\b",
        "ecl:(amb|blu|brn|gry|grn|hzl|oth)\\b", 
        "pid:\\d{9}\\b", 
        "cid"};

    //define each bit: {byr}{iyr}{eyr}{hgt}{hcl}{ecl}{pid}{cid}
    //if larger than 254, valid passport
    int check = 0;
    int numPass = 0;

    ifstream fin(input);

    while(getline(fin,line)) {
        //zero-length line signals end of passport and check of validity
        if (!line.size()) {
            if(check >=254) count++;
            check = 0;
            continue;
        }

        for (i = 0; i < fields.size(); i++) {
            if (regex_search(line, regex(fields[i]))) 
                //set the appropriate bit in check (eg if byr is found, set 1000 0000)
                //i+1 to make math work out: left shift to appropriate spot: 1 << 7 = 128 or 1000 0000
                check |= 1 << (fields.size()-(i+1));
        }
    }

    //loop exits before checking last segment
    if(check >=254) count++;

    cout << "Valid passports: " << count << endl;
}