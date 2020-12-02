#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main(int argc, char* argv[]) { 
	int result, sum, low, hi, mid;
	string input(argv[1]);
	string line;
	vector<int> nums;


	//read in to list for processing
	ifstream fin(input);
	while(getline(fin,line)) {
		nums.push_back(stoi(line));
	}

	sort(nums.begin(), nums.end());

	//loops through middle of list, if no probable values, removes begin or end and starts again.
	result = 0;
	low = 0;
	mid = 1;
	hi = nums.size()-1;
	while ((low != hi) && (mid != hi)) {
		sum = nums[low] + nums[mid] + nums[hi];

		if (sum < 2020) { 
			//lm---h or l--m--h
			if (mid < hi-1) mid++;

			//l---mh
			else {
				low++;
				mid = low + 1;
			}
		}

		else if (sum > 2020) {
			//lm---h
			if (mid == low+1) hi--;
						
			//l--m--h or l---mh
			else {
				mid = low+1;
				hi--;
			}
		}

		else {
			result = nums[low] * nums[mid] * nums[hi];
			break;
		}
	}

	fin.close();

	cout << result << endl;
}