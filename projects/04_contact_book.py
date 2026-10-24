"""Project 4 - Contact book.

A dictionary-based contact manager with search and JSON saving, built from the
Part 4 chapters. Data is only written to a file when you ask for it.

Run:
    python 04_contact_book.py --demo     # deterministic demo using a temporary file
    python 04_contact_book.py            # interactive menu (file: contacts.json in the current folder)
Standard library only. Do not store real secrets or sensitive personal data in a toy project.
"""
import json
import os
import sys
import tempfile


def add_contact(book, name, phone, email=""):
    key = name.strip().lower()
    if not key:
        raise ValueError("name must not be empty")
    if not phone.strip().replace("+", "").replace(" ", "").isdigit():
        raise ValueError("phone must contain digits only (spaces and a leading + are allowed)")
    book[key] = {"name": name.strip(), "phone": phone.strip(), "email": email.strip()}


def search(book, text):
    text = text.lower()
    return [c for c in book.values() if text in c["name"].lower() or text in c["phone"] or text in c["email"].lower()]


def delete_contact(book, name):
    return book.pop(name.strip().lower(), None) is not None


def save(book, path):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(book, handle, indent=2, sort_keys=True)


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def format_contact(contact):
    extra = f" <{contact['email']}>" if contact["email"] else ""
    return f"{contact['name']}: {contact['phone']}{extra}"


def run_demo():
    book = {}
    add_contact(book, "Asha Rao", "+91 98765 43210", "asha@example.com")
    add_contact(book, "Ravi Kumar", "9123456780")
    add_contact(book, "Asha Menon", "9000011111")
    try:
        add_contact(book, "Bad Phone", "abc")
    except ValueError as error:
        print("rejected:", error)
    print([format_contact(c) for c in search(book, "asha")])
    print(delete_contact(book, "ravi kumar"), delete_contact(book, "nobody"))
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "contacts.json")
        save(book, path)
        print("saved and reloaded equal:", load(path) == book)
    print(sorted(c["name"] for c in book.values()))


def main(argv):
    if "--demo" in argv:
        run_demo()
        return 0
    path = "contacts.json"
    book = load(path)
    menu = "1) add  2) search  3) delete  4) list  5) save and quit  6) quit without saving"
    while True:
        print(menu)
        choice = input("> ").strip()
        try:
            if choice == "1":
                add_contact(book, input("name: "), input("phone: "), input("email (optional): "))
            elif choice == "2":
                for contact in search(book, input("search: ")):
                    print(format_contact(contact))
            elif choice == "3":
                print("deleted" if delete_contact(book, input("name: ")) else "not found")
            elif choice == "4":
                for contact in sorted(book.values(), key=lambda c: c["name"].lower()):
                    print(format_contact(contact))
            elif choice == "5":
                save(book, path)
                print("saved to", path)
                return 0
            elif choice == "6":
                return 0
        except ValueError as error:
            print("error:", error)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
