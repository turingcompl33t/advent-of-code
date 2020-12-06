#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
   string input(argv[1]);
   static int ROW_CHARS = 7;
   static int COL_CHARS = 3;

    int i, id, row, col, maxID = 0;
    string line;

    ifstream fin(input);

    while (getline(fin, line)) {
      for(row = i = 0; i < ROW_CHARS; i++) 
         if (line[i] == 'B')
            row |= 1 << (ROW_CHARS-(1+i));
      
      for(col = 0, i = ROW_CHARS; i < COL_CHARS; i++)
         if (line[i] == 'R')
            col |= 1 << (COL_CHARS-(1+i));
      
      id = row*8 + col;
      if (id > maxID) maxID = id;
    }

   cout << "Max ID: " << maxID << endl;
}