import random
import time

ai_elective = {
    "192311001", "192311004",
    "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004",
    "192311009", "192311010"
}

all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}

both = ai_elective & iot_elective

exactly_one = ai_elective ^ iot_elective

neither = all_students - (ai_elective | iot_elective)

print("Clash:", sorted(both))
print("Exactly one:", sorted(exactly_one))
print("Neither:", sorted(neither))

print("\nUsing set methods")

both_method = ai_elective.intersection(iot_elective)
one_method = ai_elective.symmetric_difference(iot_elective)
neither_method = all_students.difference(
    ai_elective.union(iot_elective)
)

print("Both:", sorted(both_method))
print("Exactly one:", sorted(one_method))
print("Neither:", sorted(neither_method))

print("\nDuplicate removal")

students = [
    "192311001", "192311001",
    "192311004", "192311004"
]

print("Original:", students)
print("Unique:", set(students))

print("\nPerformance Analysis")

for size in [10000, 100000, 1000000]:
    data = list(range(size))
    data_set = set(data)

    target = size - 1

    start = time.perf_counter()
    target in data
    print("List search:", size, time.perf_counter() - start)

    start = time.perf_counter()
    target in data_set
    print("Set search:", size, time.perf_counter() - start)

print("\nEdge cases")

print("Empty:", set() & ai_elective)
print("Identical:", ai_elective & ai_elective)
print("Tuple set:", {(1, 2), (3, 4)})

try:
    invalid = {[1, 2], [3, 4]}
except TypeError as e:
    print("Error:", e)
