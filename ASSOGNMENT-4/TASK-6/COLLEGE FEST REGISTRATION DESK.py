from pathlib import Path


def read_files(folder):
    records = []
    errors = []

    for file_path in sorted(Path(folder).glob("*.txt")):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    records.append(
                        (file_path.name, line_number, line.strip())
                    )

        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            errors.append(f"{file_path.name}: {error}")

    return records, errors


def validate_record(line):
    parts = line.split(",")

    if len(parts) != 5:
        raise ValueError("Invalid number of fields")

    register, name, department, email, events = parts

    register = register.strip()
    name = name.strip()
    department = department.strip()
    email = email.strip()

    if not register or not name or not department:
        raise ValueError("Required field is empty")

    if "@" not in email:
        raise ValueError("Invalid email address")

    email_parts = email.split("@")

    if len(email_parts) != 2:
        raise ValueError("Invalid email address")

    if not email_parts[0] or "." not in email_parts[1]:
        raise ValueError("Invalid email address")

    if email_parts[1].startswith(".") or email_parts[1].endswith("."):
        raise ValueError("Invalid email address")

    event_list = [event.strip() for event in events.split(";")]

    if not event_list or any(not event for event in event_list):
        raise ValueError("Invalid event list")

    return {
        "register": register,
        "name": name,
        "department": department,
        "email": email,
        "events": event_list
    }


def process_records(records, errors):
    master = []
    seen_registers = set()

    for filename, line_number, line in records:
        try:
            student = validate_record(line)
            register = student["register"]

            if register in seen_registers:
                raise ValueError("Duplicate registration")

            seen_registers.add(register)
            master.append(student)

        except ValueError as error:
            errors.append(
                f"{filename}, Line {line_number}: {error}"
            )

    return master


def write_reports(master, errors):
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    with open(
        output_folder / "master_list.txt",
        "w",
        encoding="utf-8"
    ) as file:
        for student in master:
            file.write(
                f"{student['register']},"
                f"{student['name']},"
                f"{student['department']},"
                f"{student['email']},"
                f"{';'.join(student['events'])}\n"
            )

    event_participants = {}

    for student in master:
        for event in student["events"]:
            event_participants.setdefault(event, []).append(student)

    for event, students in event_participants.items():
        filename = event.replace(" ", "_") + ".txt"

        with open(
            output_folder / filename,
            "w",
            encoding="utf-8"
        ) as file:
            for student in students:
                file.write(
                    f"{student['register']},"
                    f"{student['name']},"
                    f"{student['department']}\n"
                )

    with open(
        output_folder / "summary_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(f"Total valid registrations: {len(master)}\n")

        for event, students in event_participants.items():
            file.write(f"{event}: {len(students)} participants\n")

    with open(
        output_folder / "error_log.txt",
        "w",
        encoding="utf-8"
    ) as file:
        for error in errors:
            file.write(error + "\n")


if __name__ == "__main__":
    input_folder = Path("input")
    input_folder.mkdir(exist_ok=True)

    records, errors = read_files(input_folder)
    master = process_records(records, errors)

    write_reports(master, errors)

    print("College Fest Registration Processing Completed")
    print("Valid registrations:", len(master))
    print("Errors found:", len(errors))
    print("Reports generated in output folder")
