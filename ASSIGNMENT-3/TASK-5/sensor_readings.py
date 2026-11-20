import random
import time
import sys

readings = [
    4.5, 5.2, 9.5, 3.8, 55,
    -60, 7.2, 1.5, 6.0, 10.5
]

def clean_loop(data):
    result = []

    for value in data:
        if -50 <= value <= 50:
            result.append(value)

    return result

def clean_comprehension(data):
    return [x for x in data if -50 <= x <= 50]

def clean_filter(data):
    return list(filter(lambda x: -50 <= x <= 50, data))

valid = clean_loop(readings)
valid_comp = clean_comprehension(readings)
valid_filter = clean_filter(readings)

print("Original readings:", readings)
print("Loop result:", valid)
print("List comprehension:", valid_comp)
print("Filter result:", valid_filter)

fahrenheit = [(c * 9/5) + 32 for c in valid]

print("Fahrenheit:", fahrenheit)

alarms = [
    (minute, temperature)
    for minute, temperature in enumerate(readings, start=1)
    if -50 <= temperature <= 50
    and not (2 <= temperature <= 8)
]

print("Alarm minutes:", alarms)

temperature_dict = {
    minute: value
    for minute, value in enumerate(valid, start=1)
}

temperature_set = {value for value in valid}

print("Dictionary:", temperature_dict)
print("Set:", temperature_set)

generator = (x for x in readings if -50 <= x <= 50)

print("Generator result:", list(generator))

print("\nPerformance Analysis")

for size in [10000, 100000, 1000000]:
    data = [random.uniform(-60, 60) for _ in range(size)]

    start = time.perf_counter()
    a = clean_loop(data)
    loop_time = time.perf_counter() - start

    start = time.perf_counter()
    b = clean_comprehension(data)
    comp_time = time.perf_counter() - start

    start = time.perf_counter()
    c = clean_filter(data)
    filter_time = time.perf_counter() - start

    print("\nReadings:", size)
    print("Loop:", loop_time)
    print("Comprehension:", comp_time)
    print("Filter:", filter_time)
    print("Same results:", a == b == c)

print("\nMemory Analysis")

data = [1, 2, 3, 4, 5]

list_result = [x for x in data]
generator_result = (x for x in data)

print("List memory:", sys.getsizeof(list_result))
print("Generator memory:", sys.getsizeof(generator_result))

print("\nEdge Cases")
print("All valid:", clean_comprehension([2, 4, 6]))
print("All invalid:", clean_comprehension([60, -60, 70]))
