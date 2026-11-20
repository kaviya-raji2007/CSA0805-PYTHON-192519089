from pathlib import Path


def read_attendance(folder):
    records = {}

    for file_path in Path(folder).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) == 3 and parts[2] in ("P", "A"):
                    register, date, status = parts
                    records.setdefault(register, []).append(status)

    return records
