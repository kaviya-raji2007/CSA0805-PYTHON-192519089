import random
import time

def generate_readings(n):
    return [round(random.uniform(0, 50), 2) for _ in range(n)]

def weekly_totals(readings):
    return [sum(readings[i:i+7]) for i in range(0, len(readings), 7)]

def moving_average_naive(readings):
    if len(readings) < 7:
        return []
    return [sum(readings[i:i+7]) / 7
            for i in range(len(readings) - 6)]

def moving_average_running(readings):
    if len(readings) < 7:
        return []

    result = []
    current_sum = sum(readings[:7])
    result.append(current_sum / 7)

    for i in range(7, len(readings)):
        current_sum += readings[i] - readings[i-7]
        result.append(current_sum / 7)

    return result

def rainfall_analysis(readings):
    if not readings:
        print("No rainfall readings available")
        return

    weekly = weekly_totals(readings)

    print("Total readings:", len(readings))
    print("Weekly totals:", weekly)
    print("Wettest week:", weekly.index(max(weekly)) + 1)
    print("Driest week:", weekly.index(min(weekly)) + 1)
    print("Maximum rainfall:", max(readings))
    print("Minimum rainfall:", min(readings))

    dry_days = [i + 1 for i, value in enumerate(readings) if value == 0]

    print("Dry days:", dry_days)

    average = moving_average_running(readings)
    print("7-day moving averages:", average[:10])

readings = generate_readings(365)

rainfall_analysis(readings)

print("\nPerformance Analysis")

for size in [365, 36500, 365000]:
    data = generate_readings(size)

    start = time.perf_counter()
    moving_average_naive(data)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    moving_average_running(data)
    running_time = time.perf_counter() - start

    print("\nReadings:", size)
    print("Naive time:", naive_time)
    print("Running sum time:", running_time)

print("\nEdge Case Testing")
print("Empty list:", moving_average_running([]))
print("Short list:", moving_average_running([2, 4, 6]))
