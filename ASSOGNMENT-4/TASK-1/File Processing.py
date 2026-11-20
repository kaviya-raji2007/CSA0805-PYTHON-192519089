from decimal import Decimal, InvalidOperation


def process_mess_bill(filename):
    total = Decimal("0.00")
    report = []
    rejected_lines = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    parts = line.split(",")

                    if len(parts) != 3:
                        raise ValueError("Expected 3 fields")

                    register_number, name, amount_text = parts
                    amount = Decimal(amount_text.strip())

                    if amount < 0:
                        raise ValueError("Negative amount")

                    total += amount
                    report.append(f"{name.strip()} - ₹{amount:.2f}")

                except (ValueError, InvalidOperation) as error:
                    rejected_lines.append(
                        (line_number, line, str(error))
                    )

        print("MESS BILL REPORT")
        for item in report:
            print(item)

        print("Total Amount: ₹", total)

        print("\nRejected Lines:")
        for item in rejected_lines:
            print(item)

    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied.")


if __name__ == "__main__":
    process_mess_bill("mess_oct.txt")
