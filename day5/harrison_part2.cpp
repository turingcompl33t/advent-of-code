#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int main(int argc, char* argv[]) {
   string input(argv[1]);
   static int ROW_CHARS = 7;
   static int COL_CHARS = 3;

   int i, id, row, col, missing = 0;
   string line;

   vector<int> seats;

   ifstream fin(input);

   //just converting the seat number to binary where B and R = 1
   while (getline(fin, line)) {
      for(row = 0, i = 0; i < ROW_CHARS; i++) 
         if (line[i] == 'B')
            row |= 1 << (ROW_CHARS-(1+i));
      
      for(col = 0, i = ROW_CHARS; i < ROW_CHARS+COL_CHARS; i++)
         if (line[i] == 'R')
            col |= 1 << (COL_CHARS-(1+i-ROW_CHARS));
      
      seats.push_back(row*8 + col);
   }
   sort(seats.begin(), seats.end());
   //loop through list of sorts to find missing one
   for (i = 1; i < seats.size()-1; i++) {
      if ((seats[i]-seats[i-1])==2) {
         missing = seats[i]-1;
         break;
      }
   }

   cout << "Missing ID: " << missing << endl;
}