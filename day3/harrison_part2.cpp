#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

//returns number of trees hit
int navigate(int right, int down, vector<vector<bool>> map) {
    int x,y, count;
    x = y = count =  0;

    while(y < map.size()-1) {
        x+=right;
        y+=down;
        if (map[y][x % map[0].size()]) count++;
    }

    return count;
}

int main(int argc, char* argv[]){
    string input(argv[1]);
    vector<vector<bool>> map;
    vector<bool> line;
    char c;
    long long result;

    ifstream fin(input);

    while(fin.get(c)) {
        if (c == '\n') {
            map.push_back(line);
            line.clear();
        }
        else if (c == '.') line.push_back(false);
        else if (c == '#') line.push_back(true);
    }

    result = navigate(1,1,map);
    result *= navigate(3,1,map);
    result *= navigate(5,1,map);
    result *= navigate(7,1,map);
    result *= navigate(1,2,map);

    cout << result << endl;
}