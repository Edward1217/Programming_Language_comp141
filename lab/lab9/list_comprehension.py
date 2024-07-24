# x = ['even' if x %2 ==0 else 'odd' for x in range(20)]

# print(x)

# y = [x for x in range(20)]

# new_list = list(filter(lambda x: x%2 ==0, y))

# z = [int(x) for x in range(20) if x %2 == 0 if 10 < x < 20] 
 
# w = [int(x * y) for x in [[2,3,5]] for y in [[8,10,11]]] 
# print(w)

x = [x for x in range(1,10)]
# y = [x for x in range(20) if x % 2 ==0]

# z = list(zip(x,y))
# print(type(z[0]))

w = map(lambda x:x*2, x)
print(type(w))
print(list(w))

even_result = filter (lambda x :x %2,x)
print(list(even_result))

# a = [1,2,3,4]
# print(2 in a)
# tuple(a)
# b =([0,1],3,4,5)
# print(tuple(a))

