// kyle_part1.cpp
//
// Advent of Code Day 3 Puzzle 1.
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
#include <string_view>

constexpr static const char* const FILENAME{"input.txt"};

using slope_t = std::pair<std::size_t, std::size_t>;
using enumerated_string_t = std::pair<std::size_t, std::string>;

// a modest implementation of an iterator adaptor
// that implements the stride N algorithm
template <typename Container>
class stride_adaptor
{
    Container const& container;
    std::size_t const stride;
public:
    template <typename IterType>
    class iterator
    {
        IterType iter;
        IterType end;
        std::size_t const stride;
    public:
        iterator(IterType begin_, IterType end_, std::size_t const stride_) 
            : iter{begin_}, end{end_}, stride{stride_} {}

        bool operator==(iterator const& other)
        {
            return iter == other.iter;
        }

        bool operator!=(iterator const& other)
        {
            return iter != other.iter;
        }

        iterator& operator++()
        {
            std::size_t s{0};
            while ((s++ < stride) && (iter != end))
            {
                ++iter;
            }
            return *this;
        }

        IterType::value_type operator*()
        {
            return *iter;
        }
    };

    stride_adaptor(Container const& container_, std::size_t const stride_) 
        : container{container_}, stride{stride_} {}

    auto begin()
    {
        return iterator{container.begin(), container.end(), stride};
    }

    auto end()
    {
        return iterator{container.end(), container.end(), stride};
    }
};

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

template <typename IterType>
std::unique_ptr<std::vector<enumerated_string_t>> 
enumerate(IterType begin, IterType end)
{
    auto dst = std::make_unique<std::vector<enumerated_string_t>>();

    // raw loop :(
    auto idx = std::size_t{};
    for (auto it = begin; it != end; ++it)
    {
        dst->emplace_back(idx++, std::string{*it});
    }
    return dst;
}

std::size_t hits_for_slope(slope_t const& slope)
{
    auto& [right, down] = slope;

    auto lines = parse_lines();

    stride_adaptor strided{*lines, down};
    auto enumerated = enumerate(strided.begin(), strided.end());
    return std::transform_reduce(
        enumerated->begin(),
        enumerated->end(),
        0,
        std::plus<>{},
        [=](enumerated_string_t const& s)
        { return s.second[(right*s.first)%s.second.length()] == '#'; });
}

int main()
{
    std::vector<slope_t> slopes{{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}};
    auto const prod = std::transform_reduce(
        slopes.begin(),
        slopes.end(),
        1UL,
        std::multiplies<>{},
        hits_for_slope);

    std::cout << prod << std::endl;

    return EXIT_SUCCESS;
}