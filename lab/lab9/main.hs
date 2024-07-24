divisors x =
    [y | y <- [1..x], x `mod` y == 0]

commonDiv a b =
    [x | x<-[1..a], a `mod` x ==0, b `mod` x ==0]


commonDiv1 a b =
    if a > b     then  [x | x <- [1..b], a `mod` x == 0, b `mod` x == 0]
    else [x | x <- [1..a], a `mod` x == 0, b `mod` x == 0]

greatestCommonDiv a b =
    maximum [x | x<-[1..a], a `mod` x ==0, b `mod` x ==0]
 
sumProduct x =
    (sum x, product x)

sumProduct1 :: [[Int]] -> [(Int, Int)]
sumProduct1 xs = [(sum a, product a) | a <- xs]


tuple1 (a, _, _) =
    a

tuple2 (_, b, _) =
    b

tuple3 (_, _, c) =
    c  

pyth::[(Int,Int,Int)]->[(Int,Int,Int)]
pyth list =
    [(x, y , z) |tuple <-list,let x = tuple1 tuple,let y = tuple2 tuple,let z = tuple3 tuple, x^2 == y^2 + z^2 ]

pyth1 :: [(Int, Int, Int)] -> [(Int, Int, Int)]
pyth1 triples = [(a, b, c) | (a, b, c) <- triples, a^2 == b^2 + c^2] 

trimAlpha string =
    [x | x <- string, not (x `elem` ['A'..'Z']),not (x `elem` ['a'..'z'])]

cartesian3 a b c =
    [(x,y,z)| x <- a,y <- b,z <- c]

--american :: [(String, Int, String)] -> [String]
--american ppl =[x|tuple <- ppl, let x = tuple1 tuple, let y = tuple2 tuple, let z = tuple3 tuple ,z =="usa", y <= 20]

american list =
    [a| tuple <- list, let a = tuple1 tuple,let b = tuple2 tuple,let c = tuple3 tuple,b <= 20, c =="usa"]


addVector [x1, y1, z1] [x2, y2, z2] = (x1 + x2, y1 + y2, z1 + z2)

dotProduct [x1, y1, z1] [x2, y2, z2] = sum [x1 * x2, y1 * y2, z1 * z2]

scalarMult a [x1, y1, z1] = (a * x1, a * y1, a * z1)


isPrime a =
    if length (divisors a) <= 2 then True else False

primeRange a =
    [x| x <- [2..a], isPrime x == True]