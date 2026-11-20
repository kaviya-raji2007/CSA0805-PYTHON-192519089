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


def calculate_percentage(records):
    result = {}

    for register, statuses in records.items():
        total = len(statuses)
        present = statuses.count("P")
        result[register] = present / total * 100 if total else 0

    return result


def write_reports(result, records):
    with open("percentage_report.txt", "w") as file:
        for register, percentage in result.items():
            file.write(f"{register}: {percentage:.2f}%\n")

    with open("three_day_absent.txt", "w") as file:
        for register, statuses in records.items():
            for i in range(len(statuses) - 2):
                if statuses[i:i + 3] == ["A", "A", "A"]:
                    file.write(register + "\n")
                    break
