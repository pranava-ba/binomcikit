{-# LANGUAGE BangPatterns #-}
module Main where

import System.CPUTime (getCPUTime)
import Text.Printf (printf)

clampd :: Double -> Double
clampd v = max 0 (min 1 v)

limits :: Int -> [(Double, Double)]
limits n =
  [ let p = fromIntegral x / fromIntegral n
        half = 1.96 * sqrt (max (p * (1 - p)) 1e-9 / fromIntegral n) + 0.5 / fromIntegral n
     in (clampd (p - half), clampd (p + half))
  | x <- [0 .. n]
  ]

-- coverage at one p: iterative binomial pmf, summed over covered x
covOne :: Int -> [(Double, Double)] -> Double -> Double
covOne n lims p = go 0 pmf0 0.0 lims
  where
    q = 1 - p
    pmf0 = q ^ n
    go :: Int -> Double -> Double -> [(Double, Double)] -> Double
    go _ _ !acc [] = acc
    go !k !pmf !acc ((lo, hi) : rest) =
      let acc' = if lo < p && p < hi then acc + pmf else acc
          pmf' = pmf * (fromIntegral (n - k) / fromIntegral (k + 1)) * (p / q)
       in go (k + 1) pmf' acc' rest

coverage :: Int -> [(Double, Double)] -> [Double] -> Double
coverage n lims = foldr (\p acc -> covOne n lims p + acc) 0.0

main :: IO ()
main = do
  let n = 500
      s = 50000 :: Int
      lims = limits n
      hp = [fromIntegral i / fromIntegral (s + 1) | i <- [1 .. s]]
      reps = 20 :: Int
      -- perturb per rep so GHC cannot hoist the loop-invariant computation
      loop 0 !acc = acc
      loop r !acc = loop (r - 1) (acc + coverage n lims (map (+ (fromIntegral r * 1e-13)) hp))
  let !_warm = coverage n lims hp
  t0 <- getCPUTime
  let !total = loop reps 0.0
  t1 <- getCPUTime
  let ms = fromIntegral (t1 - t0) / 1e9 / fromIntegral reps :: Double
  printf "Haskell (GHC -O2) coverage kernel  n=%d S=%d : %.2f ms/call  (checksum %.4f)\n"
    n s ms (total / fromIntegral reps)
