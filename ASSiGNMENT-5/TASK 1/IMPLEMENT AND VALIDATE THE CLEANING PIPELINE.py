import csv
import io
import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Adyar,2026-10-04,60
Guindy,2026-10-04,1500
"""


def load_clean(text):
    rows = []

    reader = csv.DictReader(io.StringIO(text))

    for row in reader:
        value = row["pm25"].strip()

        if value == "" or value.upper() == "NA":
            continue

        try:
            pm25 = float(value)
        except ValueError:
            continue

        if pm25 < 0 or pm25 > 999:
            continue

        rows.append((row["station"].strip(), row["date"].strip(), pm25))

    return rows


def min_max(values):
    if not values:
        return []

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [0.0 for value in values]

    return [
        round((value - minimum) / (maximum - minimum), 3)
        for value in values
    ]


clean = load_clean(RAW)

print("Cleaned Data:")
print(clean)

print("Min-Max Normalisation:")
print(min_max([pm for _, _, pm in clean]))

con = sqlite3.connect("air_quality.db")

con.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.execute("DELETE FROM readings")

con.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    clean
)

con.commit()

print("\nAverage PM2.5:")
print(con.execute(
    "SELECT station, AVG(pm25) FROM readings GROUP BY station"
).fetchall())

print("\nAdyar Readings:")
print(con.execute(
    "SELECT * FROM readings WHERE station = ?",
    ("Adyar",)
).fetchall())

print("\nHighest PM2.5:")
print(con.execute(
    "SELECT station, day, pm25 FROM readings ORDER BY pm25 DESC LIMIT 1"
).fetchone())

daily = defaultdict(list)

for station, day, pm25 in clean:
    daily[(station, day)].append(pm25)

for (station, day), values in daily.items():
    print(
        station, day,
        "Minimum:", min(values),
        "Maximum:", max(values),
        "Mean:", sum(values) / len(values),
        "Count:", len(values)
    )

stations = list(set(row[0] for row in clean))

for station in stations:
    dates = [row[1] for row in clean if row[0] == station]
    values = [row[2] for row in clean if row[0] == station]

    plt.plot(dates, values, marker="o", label=station)

plt.xlabel("Date")
plt.ylabel("PM2.5")
plt.title("Daily PM2.5 Trend")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("pm25_trend.png")
plt.show()

plt.bar(
    [row[0] for row in clean],
    [row[2] for row in clean]
)
plt.xlabel("Station")
plt.ylabel("PM2.5")
plt.title("Station PM2.5 Comparison")
plt.savefig("station_comparison.png")
plt.show()

con.close()
