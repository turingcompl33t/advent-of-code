-- kyle_part1.hs
-- Advent of Code Day 10 Puzzle 1.

import Data.List

main = interact $ (++"\n") . show . solve . map read . lines

solve:: [Int] -> Int
solve vals = diff1*diff3 where
  full  = [0] ++ vals ++ [maximum vals + 3]
  diffs = differences $ sort full
  diff1 = length $ filter (==1) diffs
  diff3 = length $ filter (==3) diffs

-- std::adjacent_difference
differences:: [Int] -> [Int]
differences xs = zipWith (-) (tail xs) xs 