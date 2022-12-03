// kyle_part2.cpp
//
// Advent of Code Day 6 Puzzle 2.
//
// Build
//  g++ -std=c++2a -o kyle_part2 kyle_part2.cpp

#include <tuple>
#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <numeric>
#include <cstdlib>
#include <iostream>
#include <algorithm>

constexpr static const char* const FILENAME{"input.txt"};

using group_t = std::vector<std::string>;

std::unique_ptr<std::vector<group_t>> read_groups()
{
    auto groups = std::make_unique<std::vector<group_t>>();

    std::string line{};
    group_t group{};

    std::ifstream file{};
    file.open(FILENAME, std::ios_base::in);

    while (std::getline(file, line))
    {
        if (line == std::string{})
        {
            groups->push_back(group);
            group.clear();
        } 
        else 
        {
            group.push_back(line);
        }
    }

    groups->push_back(group);
    file.close();

    return groups;
}

std::string string_intersection(std::string const& s1, std::string const& s2)
{
    std::string result{};
    for (const auto& c : s1)
    {
        if (s2.find(c) != std::string::npos)
        {
            result.push_back(c);
        }
    }

    std::cout << result << std::endl;
    return result;
}

std::size_t shared_questions_for_group(group_t& group)
{
    std::string ref{"abcdefghijklmnopqrstuvwxyz"};
    for (const auto &s : group)
    {
        ref = string_intersection(ref, s);
    }

    return ref.size();
}

int main()
{
    auto groups = read_groups();
    auto const s = std::transform_reduce(
        groups->begin(),
        groups->begin() + 1,
        0,
        std::plus<>{},
        shared_questions_for_group);

    std::cout << s << std::endl;

    return EXIT_SUCCESS;
}