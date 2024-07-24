second x =
    x !! 1

second1 x = 
    head (tail x)

fourth x = 
    x!!3

fourth1 x = 
    head (tail (tail (tail x)))

secondFromLast x =
    x !! (length x -2)

secondFromLast1 x =
    last (init x)

nthFromLast n list =
    list !! (length list - n)

secondHalf list =
    drop (length list `div` 2) list

atIndex n list =
    last(take(n + 1) list)

trimList list=
    drop 1 (take (length list - 1) list)

firstQ list=
    take (length list `div` 4) list