#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
#include <cmath>

using namespace std;

int main(int argc, char* argv[]) {
    string input(argv[1]);
    int count, i;
    size_t numf;
    string line, re;
    vector<string> fields = {"byr", "iyr", "eyr", "hgt", "hcl","ecl", "pid", "cid"};

    //define each bit: {byr}{iyr}{eyr}{hgt}{hcl}{ecl}{pid}{cid}
    //if larger than 254, valid passport
    int check;

    ifstream fin(input);

    while(getline(fin,line)) {
        //zero-length line signals end of passport and check of validity
        if (!line.size()) {
            if(check >=254) count++;
            check = 0;
        }

        for (i = 0; i < fields.size(); i++) {
            re = "("+fields[i]+")";
            if (regex_search(line, regex(re))) 
                //set the appropriate bit in check (eg if byr is found, set 1000 0000)
                //i+1 to make math work out: left shift to appropriate spot: 1 << 7 = 128 or 1000 0000
                check |= 1 << (fields.size()-(i+1));
        }
    }

    //loop exits before checking last segment
    if(check >=254) count++;

    cout << "Valid passports: " << count << endl;
    
}