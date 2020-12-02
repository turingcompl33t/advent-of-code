#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

void splitLine(string line, int &lo, int &hi, char &c, string &pass) {
    int space1,dash;
    string range;

    space1 = line.find(" ", 0);

    range = line.substr(0,space1); 
    //find '-' and get the substring to the left, then convert to int
    dash = range.find("-",0);
    lo = stoi(range.substr(0,dash));
    //substring to right of 
    hi = stoi(range.substr(dash+1,range.size()));

    c = line[space1+1];
    
    pass = line.substr(line.find(" ",space1+1),line.size());
}

int main(int argc, char* argv[]) {
    int count = 0;
    int lo, hi, lcount;
    char c;

    string input(argv[1]);
    string line, pass;

    vector<string> lines;

    ifstream fin(input);
    while(getline(fin, line)) lines.push_back(line);

    for (int i = 0; i < lines.size(); i++) {
        lcount = 0;
        splitLine(lines[i],lo,hi, c, pass);
        for (int j = 0; j < pass.size(); j++) 
            if (pass[j] == c) lcount++;
        if (lcount >= lo && lcount <= hi) count++;
    }


    cout << count << endl;
}