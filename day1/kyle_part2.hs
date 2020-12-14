-- puzzle2.hs
-- Advent of Code Day 1 Puzzle 2.

main = interact $ (++"\n") . show . solve . lines

solve :: [String] -> Int
solve = prod . head . filter (\(x, y, z) -> x + y + z == 2020) . selfProduct . readLines

prod :: (Int, Int, Int) -> Int
prod (x, y, z) = x*y*z 

readLines :: [String] -> [Int]
readLines = map read

selfProduct :: [a] -> [(a, a, a)]
selfProduct xs = tripleProduct xs xs xs

tripleProduct :: [a] -> [b] -> [c] -> [(a, b, c)]
tripleProduct xs ys zs = [(x, y, z) | x <- xs, y <- ys, z <- zs ]