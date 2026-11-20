import random
import time
import sys

timetable = {
    "12633": {
        "name": "Kanyakumari Express",
        "stops": [
            ("Chennai", "17:00", "17:10"),
            ("Madurai", "23:00", "23:05"),
            ("Tirunelveli", "02:00", "02:05"),
            ("Nagercoil", "04:00", "04:05")
        ],
        "days": {"Monday", "Wednesday", "Friday"}
    },

    "12634": {
        "name": "Pandian Express",
        "stops": [
            ("Chennai", "21:00", "21:10"),
            ("Villupuram", "23:00", "23:05"),
            ("Madurai", "05:00", "05:10"),
            ("Tirunelveli", "07:00", "07:05")
        ],
        "days": {"Tuesday", "Thursday", "Saturday"}
    },

    "12635": {
        "name": "Nellai Express",
        "stops": [
            ("Chennai", "20:00", "20:10"),
            ("Trichy", "02:00", "02:05"),
            ("Madurai", "04:00", "04:05"),
            ("Nagercoil", "08:00", "08:05")
        ],
        "days": {"Monday", "Tuesday", "Friday"}
    },

    "12636": {
        "name": "Vaigai Express",
        "stops": [
            ("Chennai", "13:00", "13:10"),
            ("Villupuram", "15:00", "15:05"),
            ("Trichy", "18:00", "18:05"),
            ("Madurai", "20:00", "20:05")
        ],
        "days": {"Wednesday", "Thursday", "Sunday"}
    },

    "12637": {
        "name": "Cape Express",
        "stops": [
            ("Chennai", "18:00", "18:10"),
            ("Madurai", "01:00", "01:05"),
            ("Tirunelveli", "03:00", "03:05"),
            ("Nagercoil", "05:00", "05:05")
        ],
        "days": {"Monday", "Friday", "Sunday"}
    }
}

def build_index(data):
    index = {}

    for train_no, train in data.items():
        for station, arrival, departure in train["stops"]:
            index.setdefault(station, []).append(
                (train_no, train["name"], departure, train["days"])
            )

    return index

def find_trains(data, station, day):
    result = []

    for train_no, train in data.items():
        if day not in train["days"]:
            continue

        for stop, arrival, departure in train["stops"]:
            if stop == station:
                result.append(
                    (train_no, train["name"], departure)
                )

    return sorted(result, key=lambda x: x[2])

def find_with_index(index, station, day):
    result = []

    for train_no, name, departure, days in index.get(station, []):
        if day in days:
            result.append((train_no, name, departure))

    return sorted(result, key=lambda x: x[2])

print("RAILWAY TIMETABLE")

for train_no, train in timetable.items():
    print("\nTrain:", train_no)
    print("Name:", train["name"])
    print("Running days:", sorted(train["days"]))

    for station, arrival, departure in train["stops"]:
        print(station, arrival, departure)

station = "Madurai"
day = "Monday"

print("\nTrains at", station, "on", day)
print(find_trains(timetable, station, day))

index = build_index(timetable)

print("\nUsing station index")
print(find_with_index(index, station, day))

print("\nThird station departure:")
print(timetable["12633"]["stops"][2][2])

print("\nEdge Cases")
print("Unknown station:", find_trains(timetable, "Mumbai", day))
print("Non-running day:", find_trains(timetable, "Madurai", "Sunday"))

print("\nPerformance Analysis")

def generate_timetable(n):
    data = {}
    stations = ["Chennai", "Madurai", "Trichy",
                "Nagercoil", "Tirunelveli"]

    for i in range(n):
        data[str(i)] = {
            "name": "Train " + str(i),
            "stops": [
                (random.choice(stations), "10:00", "10:10")
                for _ in range(5)
            ],
            "days": {"Monday", "Friday"}
        }

    return data

for size in [100, 1000, 10000]:
    data = generate_timetable(size)
    idx = build_index(data)

    start = time.perf_counter()
    find_trains(data, "Madurai", "Monday")
    normal_time = time.perf_counter() - start

    start = time.perf_counter()
    find_with_index(idx, "Madurai", "Monday")
    indexed_time = time.perf_counter() - start

    print("\nTrains:", size)
    print("Without index:", normal_time)
    print("With index:", indexed_time)

print("Index memory:", sys.getsizeof(index))
