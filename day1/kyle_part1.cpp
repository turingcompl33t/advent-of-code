// kyle_part1.cpp
//
// Advent of Code Day 1 Puzzle 1.
//
// Build
//  g++ -std=c++2a -o kyle_part1 kyle_part1.cpp 

#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <cstdlib>
#include <iostream>
#include <charconv>

constexpr static const char* const FILENAME{"input.txt"};

// lazy cartesian product;
// this problem screams for a coroutine, but at this point
// it is still more trouble than it is worth to implement 
// your owner generator for such a simple problem **sigh**
class cartesian_product
{
    std::vector<int> const& values;
public:
    class iterator
    {
        std::vector<int> const& values;

        std::size_t outer_idx;
        std::size_t inner_idx;

        std::size_t const limit;

    public:
        iterator(
            std::vector<int> const& values_, 
            std::size_t outer_, 
            std::size_t inner_, 
            std::size_t const limit_)
            : values{values_}
            , outer_idx{outer_}
            , inner_idx{inner_}
            , limit{limit_} {}

        bool operator==(iterator const& other)
        {
            return (outer_idx == other.outer_idx) && (inner_idx == other.inner_idx);
        }

        bool operator!=(iterator const& other)
        {
            return !(*this == other);
        }

        iterator& operator++()
        {
            inner_idx = (inner_idx + 1) % limit;
            if (0 == inner_idx)
            {
                ++outer_idx;
            }
            return *this;
        }

        std::pair<int const, int const> operator*()
        {
            return std::make_pair(values[outer_idx], values[inner_idx]);
        }
    };

    cartesian_product(std::vector<int> const& values_)
        : values{values_} {}

    iterator begin()
    {
        return iterator{values, 0UL, 0UL, values.size()};
    }

    iterator end()
    {
        return iterator{values, values.size(), 0UL, values.size()};
    }
};

std::unique_ptr<std::vector<int>> parse_values()
{
    auto values = std::make_unique<std::vector<int>>();

    std::ifstream stream{};
    stream.open(FILENAME, std::ios_base::in);

    int parsed{};
    std::string line{};
    while (std::getline(stream, line))
    {
        auto [_, ec] = std::from_chars(line.data(), line.data() + line.size(), parsed);
        if (ec == std::errc{})
        {
            values->push_back(parsed);
        }
    }

    return values;
}

int main()
{
    auto values = parse_values();

    cartesian_product product{*values};
    for (auto it = product.begin(); it != product.end(); ++it)
    {
        auto [first, second] = *it;
        if (2020 == first + second)
        {
            std::cout << first*second << std::endl;
            break;
        }
    }

    return EXIT_SUCCESS;
}