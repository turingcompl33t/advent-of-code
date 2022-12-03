// kyle_part1.cpp
//
// Advent of Code Day 6 Puzzle 1.
//
// Build
//  g++ -std=c++2a -o kyle_part1 kyle_part1.cpp

#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <numeric>
#include <cstdlib>
#include <iostream>
#include <algorithm>

constexpr static const char* const FILENAME{"input.txt"};

std::unique_ptr<std::vector<std::string>> read_groups()
{
    auto groups = std::make_unique<std::vector<std::string>>();

    std::string line{};
    std::string build{};

    std::ifstream file{};
    file.open(FILENAME, std::ios_base::in);

    while (std::getline(file, line))
    {
        if (line == std::string{})
        {
            groups->push_back(build);
            build.clear();
        } 
        else 
        {
            build.append(line);
        }
    }

    groups->push_back(build);
    file.close();

    return groups;
}

std::size_t unique_questions_for_group(std::string& g)
{
    std::sort(g.begin(), g.end());
    auto end = std::unique(g.begin(), g.end());
    return std::distance(g.begin(), end);
}

int main()
{
    auto groups = read_groups();
    auto const s = std::transform_reduce(
        groups->begin(),
        groups->end(),
        0,
        std::plus<>{},
        unique_questions_for_group);

   std::cout << s << std::endl;

    return EXIT_SUCCESS;
}