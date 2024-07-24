module Graph where

-- Polymorphic data type for a vertex
data Vertex a = Vertex a deriving (Show, Eq)

-- Polymorphic data type for an edge
data Edge a = Edge (Vertex a) (Vertex a) Float deriving (Show, Eq)

-- Make Edge a an instance of Ord explicitly by comparing the weights on the edges
instance (Ord a) => Ord (Edge a) where
    (Edge _ _ weight1) `compare` (Edge _ _ weight2) = weight1 `compare` weight2

-- Polymorphic data type for a graph
data Graph a = Graph [Vertex a] [Edge a] deriving (Show, Eq)

-- Function kruskaHelper: finds the minimum spanning tree (MST)
kruskaHelper :: (Eq a) => [Edge a] -> [[Vertex a]] -> [Edge a] -> Int -> Graph a
kruskaHelper sortedEdges connectedVertices mstEdges numEdgesAdded
    | numEdgesAdded == length connectedVertices - 1 = Graph (concat connectedVertices) mstEdges
    | otherwise = kruskaHelper remainingEdges updatedConnectedVertices updatedMstEdges updatedNumEdgesAdded
    where
        (Edge v1 v2 _) = head sortedEdges
        updatedConnectedVertices = if sameSet v1 v2 connectedVertices then connectedVertices else mergeSets v1 v2 connectedVertices
        updatedMstEdges = head sortedEdges : mstEdges
        updatedNumEdgesAdded = numEdgesAdded + 1
        remainingEdges = tail sortedEdges

-- Function kruskal: finds the minimum spanning tree (MST) of a graph
kruskal :: (Ord a, Eq a) => Graph a -> Graph a
kruskal (Graph vertices edges) = kruskaHelper sortedEdges [[v] | v <- vertices] [] 0
    where
        sortedEdges = quickSort edges

-- Function sameSet: checks if two vertices belong to the same set in the list of connected vertices
sameSet :: (Eq a) => Vertex a -> Vertex a -> [[Vertex a]] -> Bool
sameSet v1 v2 connectedVertices = any (\set -> v1 `elem` set && v2 `elem` set) connectedVertices

-- Function mergeSets: merges the sets containing two vertices in the list of connected vertices
mergeSets :: (Eq a) => Vertex a -> Vertex a -> [[Vertex a]] -> [[Vertex a]]
mergeSets v1 v2 connectedVertices = [if v1 `elem` set || v2 `elem` set then unionSet else set | set <- connectedVertices]
    where
        unionSet = concat $ filter (\set -> v1 `elem` set || v2 `elem` set) connectedVertices

-- Function quickSort: sorts a list of edges using quicksort algorithm
quickSort :: (Ord a) => [a] -> [a]
quickSort [] = []
quickSort (x:xs) = quickSort [y | y <- xs, y <= x] ++ [x] ++ quickSort [y | y <- xs, y > x]





-- Example graph data
exampleVertices :: [Vertex Char]
exampleVertices = map Vertex ['A', 'B', 'C', 'D', 'E']

exampleEdges :: [Edge Char]
exampleEdges =
    [ Edge (Vertex 'A') (Vertex 'B') 4
    , Edge (Vertex 'A') (Vertex 'C') 2
    , Edge (Vertex 'B') (Vertex 'C') 5
    , Edge (Vertex 'B') (Vertex 'D') 10
    , Edge (Vertex 'C') (Vertex 'D') 3
    , Edge (Vertex 'C') (Vertex 'E') 7
    , Edge (Vertex 'D') (Vertex 'E') 8
    ]

exampleGraph :: Graph Char
exampleGraph = Graph exampleVertices exampleEdges

-- Function to print the result
printMST :: Graph Char -> IO ()
printMST (Graph _ mstEdges) = putStrLn $ "Minimum Spanning Tree (MST): " ++ show mstEdges

-- Main function to test the Kruskal's algorithm
main :: IO ()
main = do
    putStrLn "Example graph:"
    print exampleGraph
    putStrLn "\nFinding Minimum Spanning Tree (MST) using Kruskal's algorithm:"
    printMST $ kruskal exampleGraph