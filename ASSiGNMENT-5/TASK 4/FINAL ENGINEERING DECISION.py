import sqlite3
import time
from collections import Counter


POSITIVE = {
    "good", "clean", "fast", "helpful", "improved"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke", "broken"
}

NEGATORS = {
    "not", "never", "no"
}


def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()

    total = 0

    for index, word in enumerate(words):
        value = 0

        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1

        if index > 0 and words[index - 1] in NEGATORS:
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


def summarise(text, count=2):
    sentences = [
        sentence.strip()
        for sentence in text.split(".")
        if sentence.strip()
    ]

    words = text.lower().replace(".", " ").replace(",", " ").split()

    common_words = Counter(
        word for word in words
        if word not in {
            "the", "is", "a", "an", "and", "are", "was",
            "were", "to", "of", "in", "from", "this", "that"
        }
    )

    ranked = []

    for sentence in sentences:
        sentence_words = sentence.lower().split()
        importance = sum(
            common_words[word.strip(",")] for word in sentence_words
        )
        ranked.append((importance, sentence))

    ranked.sort(reverse=True)

    return ". ".join(
        sentence for _, sentence in ranked[:count]
    )


complaints = [
    "The roads are clean. The buses are fast.",
    "The factory smoke is bad. The air is dirty.",
    "The staff are helpful. The service is good.",
    "The roads are broken. Traffic is slow.",
    "The air is clean. Pollution has improved.",
    "The water is dirty. The smell is bad.",
    "The bus service is fast. Drivers are helpful.",
    "The factory smoke is harmful. The air is bad.",
    "The roads are good. The street lights are broken.",
    "The service is not helpful. The staff are rude.",
    "The air is clean. The roads are good.",
    "The traffic is slow. The roads are dirty.",
    "The pollution is bad. Smoke is everywhere.",
    "The bus is fast. The driver is helpful.",
    "The roads are broken. The service is slow.",
    "The air quality is good. Pollution has improved.",
    "The factory smoke is bad. People are suffering.",
    "The staff are helpful. The roads are clean.",
    "The buses are slow. The service is bad.",
    "The environment is clean. The air is good.",
    "The roads are dirty. The traffic is slow.",
    "The bus service is improved. The staff are helpful.",
    "The air is bad. Smoke is increasing.",
    "The roads are clean. The transport is fast.",
    "The service is rude. The system is broken.",
    "The pollution is reduced. The air is clean.",
    "The buses are fast. The roads are good.",
    "The factory smoke is dirty. The air is bad.",
    "The staff are not helpful. The service is slow.",
    "The roads are improved. The area is clean.",
    "The air is dirty. The environment is bad.",
    "The transport is fast. The buses are good.",
    "The roads are broken. The street lights are bad.",
    "The staff are helpful. The service is improved.",
    "The factory smoke is bad. The pollution is high.",
    "The air is clean. The environment is good.",
    "The buses are slow. The roads are dirty.",
    "The service is good. The staff are helpful.",
    "The air is bad. The factory is dirty.",
    "The roads are clean. Transport is improved.",
    "The bus service is not bad. The staff are helpful.",
    "The pollution is never good. The air is dirty.",
    "The roads are fast. The service is good.",
    "The factory smoke is harmful. The air is bad.",
    "The staff are rude. The system is broken.",
    "The environment is clean. The service is improved.",
    "The roads are not clean. The air is dirty.",
    "The buses are fast. The transport is helpful.",
    "The pollution is bad. The factory smoke is increasing.",
    "The air quality is good. The roads are clean."
]


print("SENTIMENT ANALYSIS")

correct = 0

for complaint in complaints:
    result = label(complaint)

    print(result, "|", complaint)

    if result == "positive":
        correct += 1

print("\nTotal Complaints:", len(complaints))
print("Positive Complaints:", correct)


print("\nCOMPLAINT SUMMARY")

all_complaints = ". ".join(complaints)

print(summarise(all_complaints, 5))


print("\nDATABASE INDEX PERFORMANCE")

con = sqlite3.connect("air_quality.db")

con.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.execute("CREATE INDEX IF NOT EXISTS idx_station_day ON readings(station, day)")

con.commit()

start = time.perf_counter()

for i in range(1000):
    con.execute(
        "SELECT AVG(pm25) FROM readings WHERE station = ? AND day = ?",
        ("Adyar", "2026-10-01")
    ).fetchone()

indexed_time = time.perf_counter() - start

print("Indexed query time:", round(indexed_time, 6), "seconds")

con.close()


print("\nFINAL ENGINEERING DECISION")

print("1. Store readings in an SQLite database.")
print("2. Use indexes on station and date columns.")
print("3. Clean missing and invalid sensor readings.")
print("4. Use Pandas for large-scale data analysis.")
print("5. Use Matplotlib for data visualisation.")
print("6. Use sentiment analysis for citizen complaints.")
print("7. Use a trained machine learning model for better accuracy.")
