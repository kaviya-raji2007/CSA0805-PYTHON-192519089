from pathlib import Path


def read_attendance(folder):
    records = {}

    for file_path in Path(folder).glob("*.txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(",")

                    if len(parts) == 3 and parts[2] in ("P", "A"):
                        register, date, status = parts
                        records.setdefault(register, []).append(status)

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            print(error)

    return records


def calculate_percentage(records):
    result = {}

    for register, statuses in records.items():
        total = len(statuses)
        present = statuses.count("P")
        result[register] = present / total * 100 if total else 0

    return result


def find_three_day_absences(records):
    absent_students = []

    for register, statuses in records.items():
        for i in range(len(statuses) - 2):
            if statuses[i:i + 3] == ["A", "A", "A"]:
                absent_students.append(register)
                break

    return absent_students


def write_reports(result, absent_students):
    with open("percentage_report.txt", "w", encoding="utf-8") as file:
        for register, percentage in result.items():
            file.write(f"{register}: {percentage:.2f}%\n")

    with open("three_day_absent.txt", "w", encoding="utf-8") as file:
        for register in absent_students:
            file.write(register + "\n")


if __name__ == "__main__":
    records = read_attendance("daily_files")
    result = calculate_percentage(records)
    absent_students = find_three_day_absences(records)

    write_reports(result, absent_students)

    print("Attendance processing completed")
    print("Percentage report generated")
    print("Three-day absence report generated")
