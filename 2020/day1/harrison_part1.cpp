#include <iostream>
#include <fstream>
#include <string>
#include <list>

using namespace std;

int main(int argc, char* argv[]) { 
	int result, sum;
	string input(argv[1]);
	string line;
	list<int> nums;

	//read in to list for processing
	ifstream fin(input);
	while(getline(fin,line)) {
		nums.push_back(stoi(line));
	}
	nums.sort();

	//iterate through from beginning and end, remove values that do not add appropriately
	result = 0;
	while(!nums.empty()){
		sum = nums.front()+nums.back();
		if (sum>2020) nums.pop_back();
		else if (sum < 2020) nums.pop_front();
		else if (sum == 2020) {
			result = nums.front()*nums.back();
			break;
		}
		else break;
	}

	fin.close();

	cout << result << endl;
}

