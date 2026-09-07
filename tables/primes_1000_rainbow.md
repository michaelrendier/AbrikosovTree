# Rainbow table — the first 1000 primes

For each prime p (index 1..1000, p = 2 … 7919):

- **its own factors** are trivially `1, p`  and **prime factors** `p` — every prime, by definition.
- the useful structure is the factorisation of the **neighbours p−1 and p+1** — the smooth-number
  data a factoring machine reads (Pollard p−1 fires when p−1 is smooth; Williams p+1 when p+1 is).

Full data: `tables/primes_1000_rainbow.csv` (1000 rows).  Preview — first 30:

| idx | p | p−1 = prime factorisation | p−1 largest prime | p+1 = prime factorisation | p+1 largest prime |
|----:|--:|:--|--:|:--|--:|
| 1 | 2 | 1 = 1 | 1 | 3 = 3 | 3 |
| 2 | 3 | 2 = 2 | 2 | 4 = 2^2 | 2 |
| 3 | 5 | 4 = 2^2 | 2 | 6 = 2 · 3 | 3 |
| 4 | 7 | 6 = 2 · 3 | 3 | 8 = 2^3 | 2 |
| 5 | 11 | 10 = 2 · 5 | 5 | 12 = 2^2 · 3 | 3 |
| 6 | 13 | 12 = 2^2 · 3 | 3 | 14 = 2 · 7 | 7 |
| 7 | 17 | 16 = 2^4 | 2 | 18 = 2 · 3^2 | 3 |
| 8 | 19 | 18 = 2 · 3^2 | 3 | 20 = 2^2 · 5 | 5 |
| 9 | 23 | 22 = 2 · 11 | 11 | 24 = 2^3 · 3 | 3 |
| 10 | 29 | 28 = 2^2 · 7 | 7 | 30 = 2 · 3 · 5 | 5 |
| 11 | 31 | 30 = 2 · 3 · 5 | 5 | 32 = 2^5 | 2 |
| 12 | 37 | 36 = 2^2 · 3^2 | 3 | 38 = 2 · 19 | 19 |
| 13 | 41 | 40 = 2^3 · 5 | 5 | 42 = 2 · 3 · 7 | 7 |
| 14 | 43 | 42 = 2 · 3 · 7 | 7 | 44 = 2^2 · 11 | 11 |
| 15 | 47 | 46 = 2 · 23 | 23 | 48 = 2^4 · 3 | 3 |
| 16 | 53 | 52 = 2^2 · 13 | 13 | 54 = 2 · 3^3 | 3 |
| 17 | 59 | 58 = 2 · 29 | 29 | 60 = 2^2 · 3 · 5 | 5 |
| 18 | 61 | 60 = 2^2 · 3 · 5 | 5 | 62 = 2 · 31 | 31 |
| 19 | 67 | 66 = 2 · 3 · 11 | 11 | 68 = 2^2 · 17 | 17 |
| 20 | 71 | 70 = 2 · 5 · 7 | 7 | 72 = 2^3 · 3^2 | 3 |
| 21 | 73 | 72 = 2^3 · 3^2 | 3 | 74 = 2 · 37 | 37 |
| 22 | 79 | 78 = 2 · 3 · 13 | 13 | 80 = 2^4 · 5 | 5 |
| 23 | 83 | 82 = 2 · 41 | 41 | 84 = 2^2 · 3 · 7 | 7 |
| 24 | 89 | 88 = 2^3 · 11 | 11 | 90 = 2 · 3^2 · 5 | 5 |
| 25 | 97 | 96 = 2^5 · 3 | 3 | 98 = 2 · 7^2 | 7 |
| 26 | 101 | 100 = 2^2 · 5^2 | 5 | 102 = 2 · 3 · 17 | 17 |
| 27 | 103 | 102 = 2 · 3 · 17 | 17 | 104 = 2^3 · 13 | 13 |
| 28 | 107 | 106 = 2 · 53 | 53 | 108 = 2^2 · 3^3 | 3 |
| 29 | 109 | 108 = 2^2 · 3^3 | 3 | 110 = 2 · 5 · 11 | 11 |
| 30 | 113 | 112 = 2^4 · 7 | 7 | 114 = 2 · 3 · 19 | 19 |

## smoothness summary (over all 1000)

- p−1: largest prime factor — median 71, max 3911 (at p=7823)
- p+1: largest prime factor — median 67, max 3877
- p−1 that are 50-smooth: 424/1000   ·  20-smooth: 245/1000
- p+1 that are 50-smooth: 440/1000

A machine picking B by smoothest neighbour: for each p, min(largest_pf(p−1), largest_pf(p+1))
 is ≤ 50 for 686/1000 of the first 1000 primes.
