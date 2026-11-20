from pathlib import Path


def save_returns(books):
    with open("returns.log", "a", encoding="utf-8") as log:
        for book in books:
            log.write(book + "\n")


def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = [line.strip() for line in file if line.strip()]

        save_returns(books)

    except FileNotFoundError as error:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {error}\n")

    except PermissionError as error:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {error}\n")

    except OSError as error:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {error}\n")


if __name__ == "__main__":
    Path("day1.txt").write_text("Python Basics\nJava Programming\n")
    Path("day2.txt").write_text("Data Structures\nComputer Networks\n")
    Path("day3.txt").write_text("Database Systems\nCompiler Design\n")

    for filename in ["day1.txt", "day2.txt", "day3.txt"]:
        process(filename)

    process("missing_day.txt")

    with open("returns.log", "r", encoding="utf-8") as file:
        print(file.read())

    if Path("error.log").exists():
        with open("error.log", "r", encoding="utf-8") as file:
            print(file.read())
