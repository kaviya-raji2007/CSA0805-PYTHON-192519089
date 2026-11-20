import csv
import sqlite3
import pandas as pd
import random
import time
import cProfile
import statistics
from collections import defaultdict


def generate_data(station_count):
    rows = []

    for station_number in range(station_count):
        station = f"Station{station_number + 1}"

        for day in range(365):
            for hour in range(24):
                rows.append([
                    station,
                    f"2026-{day + 1:03d}",
                    hour,
                    round(random.uniform(10, 200), 2)
                ])

    return rows


def python_method(filename):
    data = defaultdict(list)

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            key = (row["station"], row["day"])
            data[key].append(float(row["pm25"]))

    result = {}

    for key, values in data.items():
        result[key] = statistics.mean(values)

    return result


def pandas_method(filename):
    df = pd.read_csv(filename)

    result = df.groupby(
        ["station", "day"]
    )["pm25"].mean()

    return result


def sql_method(filename):
    df = pd.read_csv(filename)

    con = sqlite3.connect(":memory:")

    df.to_sql("readings", con, index=False, if_exists="replace")

    result = con.execute("""
        SELECT station, day, AVG(pm25)
        FROM readings
        GROUP BY station, day
    """).fetchall()

    con.close()

    return result


for station_count in [1, 12, 120]:

    print("\nStations:", station_count)

    rows = generate_data(station_count)

    filename = "generated_air_quality.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "day", "hour", "pm25"])
        writer.writerows(rows)

    start = time.perf_counter()
    python_result = python_method(filename)
    python_time = time.perf_counter() - start

    start = time.perf_counter()
    pandas_result = pandas_method(filename)
    pandas_time = time.perf_counter() - start

    start = time.perf_counter()
    sql_result = sql_method(filename)
    sql_time = time.perf_counter() - start

    print("Total readings:", len(rows))
    print("Python Time:", round(python_time, 4), "seconds")
    print("Pandas Time:", round(pandas_time, 4), "seconds")
    print("SQL Time:", round(sql_time, 4), "seconds")

    print("Python and Pandas agree:",
          len(python_result) == len(pandas_result))

    print("Python and SQL agree:",
          len(python_result) == len(sql_result))


print("\nPROFILING PYTHON METHOD")

cProfile.run(
    "python_method('generated_air_quality.csv')",
    sort="cumtime"
)
