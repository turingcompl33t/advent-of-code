// kyle_part1.cpp
//
// Advent of Code Day 3 Puzzle 1.
//
// Build
//  g++ -std=c++2a -o kyle_part1 kyle_part1.cpp

#include <tuple>
#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <numeric>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <string_view>

constexpr static const char* const FILENAME{"input.txt"};

using enumerated_string = std::pair<std::size_t, std::string_view>;

std::unique_ptr<std::vector<std::string>> parse_lines()
{
    auto lines = std::make_unique<std::vector<std::string>>();

    std::string line{};
    std::ifstream file{};
    file.open(FILENAME, std::ios_base::in);

    while (std::getline(file, line))
    {
        lines->push_back(line);
    }

    file.close();
    return lines;
}

// non-lazy, non-generic enumerate()... ouch
std::unique_ptr<std::vector<enumerated_string>> 
enumerate(std::vector<std::string> const& src)
{
    auto dst = std::make_unique<std::vector<enumerated_string>>();
    std::transform(
        src.begin(), 
        src.end(), 
        std::back_inserter(*dst),
        [idx = 0](std::string const& s) mutable
        {
            return std::make_pair(idx++, std::string_view{s});
        });

    return dst;
}

int main()
{
    auto lines = parse_lines();

    auto enumerated = enumerate(*lines);
    auto const s = std::transform_reduce(
        enumerated->begin(),
        enumerated->end(),
        0,
        std::plus<>{},
        [](enumerated_string const& s)
        { return s.second[(3*s.first)%s.second.length()] == '#'; });

    std::cout << "Hit " << s << " trees" << std::endl;
    
    return EXIT_SUCCESS;
}