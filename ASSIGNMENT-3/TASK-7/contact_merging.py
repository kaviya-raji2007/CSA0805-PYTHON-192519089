import random
import time
import re

contacts = [
    {
        "name": "Dr. Ravi",
        "phone": ["+91 98400 12345"],
        "email": ["ravi@gmail.com"]
    },
    {
        "name": "Ravi Kumar",
        "phone": ["9840012345", "9876543210"],
        "email": ["ravi.kumar@gmail.com"]
    },
    {
        "name": "Priya",
        "phone": ["+91 98765 43210"],
        "email": ["priya@gmail.com"]
    },
    {
        "name": "Arun",
        "phone": ["9123456789"],
        "email": []
    },
    {
        "name": "Ravi",
        "phone": ["9840012345"],
        "email": ["ravi@gmail.com"]
    }
]

def normalize_phone(phone):
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits

def merge_contacts(records):
    groups = []
    phone_index = {}

    for contact in records:
        phones = {
            normalize_phone(p)
            for p in contact.get("phone", [])
            if normalize_phone(p)
        }

        emails = {
            e.strip().lower()
            for e in contact.get("email", [])
            if e.strip()
        }

        matches = {
            phone_index[p]
            for p in phones
            if p in phone_index
        }

        if not matches:
            group = {
                "names": set(),
                "phones": set(),
                "emails": set()
            }
            groups.append(group)
        else:
            group = groups[min(matches)]

            for index in sorted(matches - {min(matches)}, reverse=True):
                other = groups[index]

                group["names"].update(other["names"])
                group["phones"].update(other["phones"])
                group["emails"].update(other["emails"])

                for phone in other["phones"]:
                    phone_index[phone] = min(matches)

                groups[index] = None

        if contact.get("name"):
            group["names"].add(contact["name"].strip())

        group["phones"].update(phones)
        group["emails"].update(emails)

        group_index = groups.index(group)

        for phone in group["phones"]:
            phone_index[phone] = group_index

    return [g for g in groups if g is not None]

merged = merge_contacts(contacts)

print("MERGED CONTACTS")

for i, contact in enumerate(merged, start=1):
    print("\nContact", i)
    print("Names:", sorted(contact["names"]))
    print("Phone numbers:", sorted(contact["phones"]))
    print("Emails:", sorted(contact["emails"]))

print("\nTotal original contacts:", len(contacts))
print("Total merged contacts:", len(merged))

print("\nDuplicate Testing")

test_data = [
    {"name": "Ravi", "phone": ["9840012345"], "email": []},
    {"name": "Dr Ravi", "phone": ["+91 98400 12345"], "email": []}
]

print("Before:", len(test_data))
print("After:", len(merge_contacts(test_data)))

print("\nPerformance Analysis")

for size in [1000, 100000]:
    data = []

    for i in range(size):
        data.append({
            "name": "Person " + str(i),
            "phone": [str(9000000000 + i)],
            "email": ["person" + str(i) + "@gmail.com"]
        })

    start = time.perf_counter()
    result = merge_contacts(data)
    elapsed = time.perf_counter() - start

    print("\nContacts:", size)
    print("Merged contacts:", len(result))
    print("Execution time:", elapsed)

print("\nMissing Fields Testing")

missing = [
    {"name": "Unknown", "phone": [], "email": []},
    {"name": "Person A", "phone": ["9876543210"], "email": []}
]

print(merge_contacts(missing))
