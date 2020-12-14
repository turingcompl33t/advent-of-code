-- puzzle1.hs
-- Advent of Code Day 2 Puzzle 1.

import Data.Char
import Data.List.Split

main = interact $ (++"\n") . show . solve . lines

solve :: [String] -> Int
solve = length . filter id . map isValid

isValid :: String -> Bool
isValid s = count >= minCount && count <= maxCount where
  minCount = read (head $ splitOn ['-'] $ head $ splitOn [' '] $ head $ splitOn [':'] s) :: Int
  maxCount = read (last $ splitOn ['-'] $ head $ splitOn [' '] $ head $ splitOn [':'] s) :: Int
  target   = head $ last $ splitOn [' '] $ head $ splitOn [':'] s
  count    = charCount target $ last $ splitOn [':'] s

charCount :: Char -> String -> Int
charCount c s = length $ filter (==c) s

trim :: String -> String
trim = f . f
  where f = reverse . dropWhile isSpace