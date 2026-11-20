import os
import tempfile


class InvalidRecord(Exception):
    pass


def parse_line(line):
    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    if parts[2] not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{parts[2]}'")

    return tuple(parts)


def summarise(path):
    present, absent, errors = 0, 0, []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    register, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as error:
                    errors.append((line_number, str(error)))

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Attendance file not found: {path}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"Cannot access file: {path}"
        ) from error

    else:
        print("File processed successfully")

    finally:
        print("Attendance processing finished")

    return present, absent, errors


data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

with tempfile.NamedTemporaryFile(
    "w", suffix=".csv", delete=False, encoding="utf-8"
) as tmp:
    tmp.write(data)

try:
    print(summarise(tmp.name))
finally:
    os.remove(tmp.name)
