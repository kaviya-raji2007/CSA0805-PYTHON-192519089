import random
import re
import time
from collections import Counter

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
    "crop damaged due to rainfall",
    "fertiliser subsidy not received"
]

STOP = {"not", "high", "the", "is", "due", "to"}

def frequencies(texts, stop):
    counts = {}

    for text in texts:
        words = re.findall(r'\b\w+\b', text.lower())

        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts

def top(counts, k):
    return sorted(counts.items(),
                  key=lambda x: (-x[1], x[0]))[:k]

def group_by_district(records):
    districts = {}

    for record in records:
        districts.setdefault(record["district"], []).append(record["text"])

    return districts

def group_by_crop(records):
    crops = {}

    for record in records:
        crops.setdefault(record["crop"], []).append(record["text"])

    return crops

records = [
    {"district": "Kanyakumari", "crop": "Rice",
     "text": "Seeds not received"},
    {"district": "Chennai", "crop": "Wheat",
     "text": "Fertiliser price high"},
    {"district": "Kanyakumari", "crop": "Rice",
     "text": "Rainfall damaged crops"},
    {"district": "Madurai", "crop": "Cotton",
     "text": "Cotton seeds delayed"}
]

counts = frequencies(calls, STOP)

print("Word frequencies:", counts)
print("Top words:", top(counts, 5))
print("District complaints:", group_by_district(records))
print("Crop complaints:", group_by_crop(records))

print("\nDictionary views:")
print(counts.keys())
print(counts.values())
print(counts.items())

print("\nPerformance Analysis")

words = ["seeds", "price", "crop", "fertiliser", "seeds"]

start = time.perf_counter()
dictionary_count = frequencies([" ".join(words * 1000)], set())
print("Dictionary time:", time.perf_counter() - start)

start = time.perf_counter()
list_count = {word: words.count(word) for word in set(words)}
print("List count time:", time.perf_counter() - start)

start = time.perf_counter()
counter = Counter(words)
print("Counter time:", time.perf_counter() - start)

for size in [1000, 10000, 100000]:
    data = [
        random.choice(["seeds", "crop", "fertiliser", "water", "price"])
        for _ in range(size)
    ]

    start = time.perf_counter()
    result = {}
    for word in data:
        result[word] = result.get(word, 0) + 1
    print("Dictionary", size, time.perf_counter() - start)

    start = time.perf_counter()
    result = Counter(data)
    print("Counter", size, time.perf_counter() - start)

print("Empty text:", frequencies([""], STOP))
