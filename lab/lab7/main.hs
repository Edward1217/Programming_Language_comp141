doubleMe x = x + x
doubleUs x y = x * 2 + y * 3
func x y z = x^2 + y^3 + z^2

least x y z =
    if x < y && x < z
        then x
    else if y < z
        then y
    else z

circle action radius =
    if action == "area" then pi * radius^2 else
        if action =="circumference" 
        then 2 * pi * radius
        else 0.0

cylinder action radius height=
    if action == "volume" then (circle "area" radius) * height else
        if action =="area" then (circle "area" radius) * 2 + (circle "circumference" radius) * height
            else 0.0

gCD a b = 
    if a == 0 
    then b 
    else gCD (b `mod` a) a

isDivision a b = 
    if b > a then False
        else if (a `mod` b) == 0 then True
            else False

--highway :: Int -> String
highway number =
    if number  >= 1000 || number <= 0 then "Not a valid interstate highway number"
    else if number <= 99 then "Primary interstate highway number"
    else if number `mod` 100 == 0 then "Not a valid interstate highway number"
    else if number `mod` 100 /= 0 then "Auxiliary interstate highway, serving I-" ++ show (number `mod` 100)
    else "Not a valid interstate highway number"

