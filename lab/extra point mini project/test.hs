-- MaxHeap type definition
type MaxHeap a = [a]

-- Percolate up function
percolateUp :: (Ord a) => Int -> MaxHeap a -> MaxHeap a
percolateUp i heap
    | i <= 0 = heap
    | parent < current = percolateUp parentIndex $ swap parentIndex i heap
    | otherwise = heap
    where
        parentIndex = (i - 1) `div` 2
        parent = heap !! parentIndex
        current = heap !! i
        swap a b lst = let (x,y:ys) = splitAt a lst
                           in x ++ [lst !! b] ++ take (b-a-1) ys ++ [lst !! a] ++ drop (b-a) ys
                           
-- Percolate down function
percolateDown :: (Ord a) => Int -> MaxHeap a -> MaxHeap a
percolateDown i heap
    | leftChild >= length heap = heap
    | rightChild < length heap && (heap !! rightChild) > (heap !! leftChild) && (heap !! rightChild) > (heap !! i) = percolateDown rightChild $ swap i rightChild heap
    | (heap !! leftChild) > (heap !! i) = percolateDown leftChild $ swap i leftChild heap
    | otherwise = heap
    where
        leftChild = 2 * i + 1
        rightChild = 2 * i + 2
        swap a b lst = let (x,y:ys) = splitAt a lst
                           in x ++ [lst !! b] ++ take (b-a-1) ys ++ [lst !! a] ++ drop (b-a) ys

-- Insert function
insert :: (Ord a) => a -> MaxHeap a -> MaxHeap a
insert x heap = percolateUp (length heap) (heap ++ [x])

-- Remove function
remove :: (Ord a) => MaxHeap a -> MaxHeap a
remove heap = case heap of
    [] -> []
    [x] -> []
    xs -> percolateDown 0 $ swap 0 (length xs - 1) xs
    where
        swap a b lst = let (x,y:ys) = splitAt a lst
                           in x ++ [lst !! b] ++ take (b-a-1) ys ++ [lst !! a] ++ drop (b-a) ys

-- Heapify function
heapify :: (Ord a) => [a] -> MaxHeap a
heapify [] = []
heapify xs = foldr percolateDown xs [n `div` 2 - 1, n `div` 2 - 2..0]
    where n = length xs

-- Heap Sort function
heapSort :: (Ord a) => [a] -> [a]
heapSort [] = []
heapSort xs = let heap = heapify xs
                  sorted = sortHeap heap
              in sorted
    where
        sortHeap [] = []
        sortHeap heap = let (x:xs) = remove heap
                        in x : sortHeap xs

-- PQueue type definition
type PQueue a = MaxHeap a

-- Enqueue function
enqueue :: (Ord a) => a -> PQueue a -> PQueue a
enqueue = insert

-- Dequeue function
dequeue :: (Ord a) => PQueue a -> PQueue a
dequeue = remove

-- Peek function
peek :: PQueue a -> Maybe a
peek [] = Nothing
peek (x:_) = Just x
