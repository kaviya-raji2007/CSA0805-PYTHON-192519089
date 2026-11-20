from pathlib import Path
from collections import defaultdict

def process_attendance(folder):
    attendance = defaultdict(lambda: [0, 0])
    error_log = []

    files = sorted(Path(folder).glob("*.txt"))

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    parts = line.strip().split(",")

                    try:
                        if len(parts) != 3:
                            raise ValueError("Invalid fields")

                        register, date, status = parts

                        if status not in ("P", "A"):
                            raise ValueError("Invalid status")

                        if status == "P":
                            attendance[register][0] += 1
                        else:
                            attendance[register][1] += 1

                    except ValueError as error:
                        error_log.append(
                            f"{file_path.name}, Line {line_number}: {error}"
                        )

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            error_log.append(f"{file_path.name}: {error}")

    with open("attendance_report.txt", "w", encoding="utf-8") as output:
        output.write("Register,Present,Absent,Percentage\n")

        for register, counts in attendance.items():
            present, absent = counts
            total = present + absent
            percentage = present / total * 100 if total else 0

            output.write(
                f"{register},{present},{absent},{percentage:.2f}%\n"
            )

    with open("below_75.txt", "w", encoding="utf-8") as output:
        for register, counts in attendance.items():
            present, absent = counts
            total = present + absent
            percentage = present / total * 100 if total else 0

            if percentage < 75:
                output.write(f"{register}: {percentage:.2f}%\n")

    with open("error_log.txt", "w", encoding="utf-8") as output:
        output.write("\n".join(error_log))

    print("Attendance processing completed")


if __name__ == "__main__":
    process_attendance("daily_files")
