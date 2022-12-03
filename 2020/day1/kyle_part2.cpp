// kyle_part2.cpp
//
// Advent of Code Day 1 Puzzle 2.
//
// Build
//  g++ -std=c++2a -o kyle_part2 kyle_part2.cpp 

#include <memory>
#include <vector>
#include <string>
#include <fstream>
#include <cstdlib>
#include <iostream>
#include <charconv>

constexpr static const char* const FILENAME{"input.txt"};

std::size_t fetch_add_modulo(std::size_t* x, std::size_t const m)
{
    auto const tmp = *x;
    *x = (tmp + 1) % m;
    return tmp;
}

// lazy triple product
class triple_product
{
    std::vector<int> const& values;
public:
    class iterator
    {
        std::vector<int> const& values;

        std::size_t t1_idx;
        std::size_t t2_idx;
        std::size_t t3_idx;

        std::size_t const limit;

    public:
        iterator(
            std::vector<int> const& values_, 
            std::size_t t1_idx_, 
            std::size_t t2_idx_,
            std::size_t t3_idx_,
            std::size_t const limit_)
            : values{values_}
            , t1_idx{t1_idx_}
            , t2_idx{t2_idx_}
            , t3_idx{t3_idx_}
            , limit{limit_} {}

        bool operator==(iterator const& other)
        {
            return (t1_idx == other.t1_idx) 
                && (t2_idx == other.t2_idx) 
                && (t3_idx == other.t3_idx);
        }

        bool operator!=(iterator const& other)
        {
            return !(*this == other);
        }

        iterator& operator++()
        {
            auto const prev_t3 = fetch_add_modulo(&t3_idx, limit);
            if (prev_t3 == (limit - 1))
            {
                auto const prev_t2 = fetch_add_modulo(&t2_idx, limit);
                if (prev_t2 == (limit - 1))
                {
                    ++t1_idx;
                }
            }
            return *this;
        }

        std::tuple<int const, int const, int const> operator*()
        {
            return std::make_tuple(values[t1_idx], values[t2_idx], values[t3_idx]);
        }
    };

    triple_product(std::vector<int> const& values_)
        : values{values_} {}

    iterator begin()
    {
        return iterator{values, 0UL, 0UL, 0UL, values.size()};
    }

    iterator end()
    {
        return iterator{values, values.size(), 0UL, 0UL, values.size()};
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

    triple_product product{*values};
    for (auto it = product.begin(); it != product.end(); ++it)
    {
        auto [first, second, third] = *it;
        if (2020 == first + second + third)
        {
            std::cout << first*second*third << std::endl;
            break;
        }
    }

    return EXIT_SUCCESS;
}