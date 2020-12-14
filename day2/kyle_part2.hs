-- puzzle2.hs
-- Advent of Code Day 2 Puzzle 2.

import Data.Char
import Data.List.Split

main = interact $ (++"\n") . show . solve . lines

solve :: [String] -> Int
solve = length . filter id . map isValid

isValid :: String -> Bool
isValid s = hasCharAt query target pos1 `xor` hasCharAt query target pos2 where
  pos1   = (read (head $ splitOn ['-'] $ head $ splitOn [' '] $ head $ splitOn [':'] s) :: Int) - 1
  pos2   = (read (last $ splitOn ['-'] $ head $ splitOn [' '] $ head $ splitOn [':'] s) :: Int) - 1
  target = head $ last $ splitOn [' '] $ head $ splitOn [':'] s
  query  = trim $ last $ splitOn [':'] s

xor :: Bool -> Bool -> Bool
xor a b = a /= b

hasCharAt :: String -> Char -> Int -> Bool
hasCharAt s c i = s !! i == c 

trim :: String -> String
trim = f . f
  where f = reverse . dropWhile isSpace