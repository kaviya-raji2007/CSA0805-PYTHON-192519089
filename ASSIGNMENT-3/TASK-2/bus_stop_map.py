import copy
import sys
import time

rows, cols = 3, 4

bad = [[0] * cols] * rows
bad[0][1] = 7

good = [[0 for j in range(cols)] for i in range(rows)]
good[0][1] = 7

print("Bad grid:", bad)
print("Good grid:", good)
print(bad[0] is bad[1], good[0] is good[1])

stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar"
}

for coordinates, name in stops.items():
    latitude, longitude = coordinates
    print(name, latitude, longitude)

original = [[1, 2], [3, 4]]

alias = original
shallow = copy.copy(original)
slicing = original[:]
deep = copy.deepcopy(original)

original[0][0] = 100

print("Original:", original)
print("Alias:", alias)
print("Shallow copy:", shallow)
print("Slicing copy:", slicing)
print("Deep copy:", deep)

print("Identity:", original is alias)
print("Shallow identity:", original[0] is shallow[0])
print("Deep identity:", original[0] is deep[0])

print("List memory:", sys.getsizeof(list(range(1000000))))
print("Tuple memory:", sys.getsizeof(tuple(range(1000000))))

start = time.perf_counter()
a = list(range(1000000))
print("List creation time:", time.perf_counter() - start)

start = time.perf_counter()
b = tuple(range(1000000))
print("Tuple creation time:", time.perf_counter() - start)

start = time.perf_counter()
x = a[500000]
print("List indexing time:", time.perf_counter() - start)

start = time.perf_counter()
y = b[500000]
print("Tuple indexing time:", time.perf_counter() - start)

data = ([10, 20], 30)
data[0].append(40)
print("List inside tuple:", data)

def update_list(values):
    values.append(100)

numbers = [10, 20, 30]
update_list(numbers)
print("Modified list:", numbers)

try:
    test = {[13.0418, 80.2341]: "T Nagar"}
except TypeError as e:
    print("Error:", e)
