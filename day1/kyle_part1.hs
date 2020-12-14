-- puzzle1.hs
-- Advent of Code Day 1 Puzzle 1.

main = interact $ (++"\n") . show . solve . lines

solve :: [String] -> Int
solve = prod . head . filter (\(x, y) -> x + y == 2020) . selfProduct . readLines

prod :: (Int, Int) -> Int
prod (x, y) = x*y 

readLines :: [String] -> [Int]
readLines = map read

selfProduct :: [a] -> [(a, a)]
selfProduct xs = cartesianProduct xs xs

cartesianProduct :: [a] -> [b] -> [(a, b)]
cartesianProduct xs ys = [(x, y) | x <- xs, y <- ys ]