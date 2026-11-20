import sqlite3
import csv
import io


readings = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

con = sqlite3.connect(":memory:")

con.execute("""
CREATE TABLE aq (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.executemany(
    "INSERT INTO aq VALUES (?, ?, ?)",
    readings
)

con.commit()


def station_average(name):
    result = con.execute(
        "SELECT AVG(pm25) FROM aq WHERE station = ?",
        (name,)
    ).fetchone()

    return result[0]


print("Adyar Average:", station_average("Adyar"))
print("Guindy Average:", station_average("Guindy"))

print(
    "Injection Attempt:",
    station_average("Adyar' OR '1'='1")
)

try:
    data = "station,date,pm25\nAdyar,2026-10-01,48\n"
    reader = csv.DictReader(io.StringIO(data))

    for row in reader:
        print("Valid CSV:", row)

    wrong_data = "station;date;pm25\nAdyar;2026-10-01;48"
    reader = csv.DictReader(io.StringIO(wrong_data))

    for row in reader:
        if "pm25" not in row:
            print("Wrong delimiter detected")

    empty_file = io.StringIO("")
    reader = csv.DictReader(empty_file)

    if reader.fieldnames is None:
        print("Empty file detected")

except (csv.Error, UnicodeDecodeError) as error:
    print("File error:", error)


def score(text):
    positive = {"good", "clean", "fast", "helpful", "improved"}
    negative = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
    negators = {"not", "never", "no"}

    words = text.lower().replace(".", " ").replace(",", " ").split()

    total = 0

    for index, word in enumerate(words):
        value = 0

        if word in positive:
            value = 1
        elif word in negative:
            value = -1

        if index > 0 and words[index - 1] in negators:
            value = -value

        total += value

    return total


def label(text):
    result = score(text)

    if result > 0:
        return "positive"
    elif result < 0:
        return "negative"
    else:
        return "neutral"


complaints = [
    "Roads are clean and the bus was fast.",
    "Smoke from the factory, air is bad.",
    "The staff were not helpful.",
    "Not bad, service improved."
]

for complaint in complaints:
    print(label(complaint), "|", complaint)


con.close()
