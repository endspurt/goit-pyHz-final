import json
import os
import re
from datetime import datetime, timedelta

DATA_FILE = 'assistant_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"contacts": [], "notes": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\+?1?\d{9,15}$", phone)

def add_contact(data):
    name = input("Name: ")
    address = input("Address: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    
    if not validate_email(email):
        print("Invalid email format")
        return
    if not validate_phone(phone):
        print("Invalid phone format")
        return
    
    contact = {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "birthday": birthday
    }
    data["contacts"].append(contact)
    save_data(data)
    print("Contact added successfully")

def list_upcoming_birthdays(data, days):
    today = datetime.today()
    upcoming = []
    for contact in data["contacts"]:
        birthday = datetime.strptime(contact["birthday"], "%Y-%m-%d")
        this_year_birthday = birthday.replace(year=today.year)
        if 0 <= (this_year_birthday - today).days <= days:
            upcoming.append(contact)
    if not upcoming:
        print("No upcoming birthdays in the next", days, "days")
    else:
        for contact in upcoming:
            print(contact)

def search_contacts(data, query):
    results = [contact for contact in data["contacts"] if query.lower() in contact["name"].lower() or query.lower() in contact["address"].lower() or query.lower() in contact["phone"] or query.lower() in contact["email"].lower()]
    if results:
        for result in results:
            print(result)
    else:
        print("No contacts found")

def edit_contact(data, name):
    for contact in data["contacts"]:
        if contact["name"].lower() == name.lower():
            contact["address"] = input(f"New address ({contact['address']}): ") or contact["address"]
            contact["phone"] = input(f"New phone ({contact['phone']}): ") or contact["phone"]
            contact["email"] = input(f"New email ({contact['email']}): ") or contact["email"]
            contact["birthday"] = input(f"New birthday ({contact['birthday']}): ") or contact["birthday"]
            save_data(data)
            print("Contact updated successfully")
            return
    print("Contact not found")

def delete_contact(data, name):
    data["contacts"] = [contact for contact in data["contacts"] if contact["name"].lower() != name.lower()]
    save_data(data)
    print("Contact deleted successfully")

def add_note(data):
    text = input("Note text: ")
    tags = input("Tags (comma-separated): ").split(",")
    note = {"text": text, "tags": tags}
    data["notes"].append(note)
    save_data(data)
    print("Note added successfully")

def search_notes(data, query):
    results = [note for note in data["notes"] if query.lower() in note["text"].lower() or query.lower() in [tag.lower() for tag in note["tags"]]]
    if results:
        for result in results:
            print(result)
    else:
        print("No notes found")

def edit_note(data, note_text):
    for note in data["notes"]:
        if note["text"].lower() == note_text.lower():
            note["text"] = input(f"New text ({note['text']}): ") or note["text"]
            note["tags"] = input(f"New tags (comma-separated) ({', '.join(note['tags'])}): ").split(",") or note["tags"]
            save_data(data)
            print("Note updated successfully")
            return
    print("Note not found")

def delete_note(data, note_text):
    data["notes"] = [note for note in data["notes"] if note["text"].lower() != note_text.lower()]
    save_data(data)
    print("Note deleted successfully")

def main_menu():
    print("\nPersonal Assistant Menu:")
    print("1. Add Contact")
    print("2. List Upcoming Birthdays")
    print("3. Search Contact")
    print("4. Edit Contact")
    print("5. Delete Contact")
    print("6. Add Note")
    print("7. Search Note")
    print("8. Edit Note")
    print("9. Delete Note")
    print("10. Exit")

def main():
    data = load_data()
    
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_contact(data)
        elif choice == "2":
            days = int(input("Enter number of days: "))
            list_upcoming_birthdays(data, days)
        elif choice == "3":
            query = input("Enter search query: ")
            search_contacts(data, query)
        elif choice == "4":
            name = input("Enter contact name to edit: ")
            edit_contact(data, name)
        elif choice == "5":
            name = input("Enter contact name to delete: ")
            delete_contact(data, name)
        elif choice == "6":
            add_note(data)
        elif choice == "7":
            query = input("Enter search query: ")
            search_notes(data, query)
        elif choice == "8":
            note_text = input("Enter note text to edit: ")
            edit_note(data, note_text)
        elif choice == "9":
            note_text = input("Enter note text to delete: ")
            delete_note(data, note_text)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()
