import json
import os
import re
from datetime import datetime, timedelta

CONTACTS_FILE = 'contacts.json'
NOTES_FILE = 'notes.json'

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

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
    data.append(contact)
    save_data(data, CONTACTS_FILE)
    print("Contact added successfully")

def list_upcoming_birthdays(data, days):
    today = datetime.today()
    upcoming = []
    for contact in data:
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
    query = query.strip().lower()
    if not query:
        print("No contacts found. Please provide a valid search query.")
        return

    results = [contact for contact in data if query in contact["name"].lower()]
    if results:
        print("Search results:")
        for result in results:
            print("Name:", result["name"])
            print("Address:", result["address"])
            print("Phone:", result["phone"])
            print("Email:", result["email"])
            print("Birthday:", result["birthday"])
            print()
    else:
        print("No contacts found with the name:", query)

def edit_contact(data, name):
    for contact in data:
        if contact["name"].lower() == name.lower():
            contact["address"] = input(f"New address ({contact['address']}): ") or contact["address"]
            contact["phone"] = input(f"New phone ({contact['phone']}): ") or contact["phone"]
            contact["email"] = input(f"New email ({contact['email']}): ") or contact["email"]
            contact["birthday"] = input(f"New birthday ({contact['birthday']}): ") or contact["birthday"]
            save_data(data, CONTACTS_FILE)
            print("Contact updated successfully")
            return
    print("Contact not found")

def delete_contact(data, name):
    data = [contact for contact in data if contact["name"].lower() != name.lower()]
    save_data(data, CONTACTS_FILE)
    print("Contact deleted successfully")

def add_note():
    data = load_data(NOTES_FILE)
    text = input("Note text: ")
    tags = input("Tags (comma-separated): ").split(",")
    note = {"text": text, "tags": [tag.strip() for tag in tags]}
    data.append(note)
    save_data(data, NOTES_FILE)
    print("Note added successfully")

def search_notes(query):
    data = load_data(NOTES_FILE)
    query = query.strip().lower()
    if not query:
        print("No notes found. Please provide a valid search query.")
        return

    results = [note for note in data if query in note["text"].lower() or query in [tag.lower() for tag in note["tags"]]]
    if results:
        print("Search results:")
        for result in results:
            print(result)
    else:
        print("No notes found with the query:", query)

def edit_note():
    data = load_data(NOTES_FILE)
    note_text = input("Enter note text to edit: ").strip().lower()
    for note in data:
        if note["text"].lower() == note_text:
            note["text"] = input(f"New text ({note['text']}): ") or note["text"]
            note["tags"] = input(f"New tags (comma-separated) ({', '.join(note['tags'])}): ").split(",") or note["tags"]
            save_data(data, NOTES_FILE)
            print("Note updated successfully")
            return
    print("Note not found")

def delete_note():
    data = load_data(NOTES_FILE)
    note_text = input("Enter note text to delete: ").strip().lower()
    data = [note for note in data if note["text"].lower() != note_text]
    save_data(data, NOTES_FILE)
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
    contacts = load_data(CONTACTS_FILE)
    
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            days = int(input("Enter number of days: "))
            list_upcoming_birthdays(contacts, days)
        elif choice == "3":
            query = input("Enter search query: ")
            search_contacts(contacts, query)
        elif choice == "4":
            name = input("Enter contact name to edit: ")
            edit_contact(contacts, name)
        elif choice == "5":
            name = input("Enter contact name to delete: ")
            delete_contact(contacts, name)
        elif choice == "6":
            add_note()
        elif choice == "7":
            query = input("Enter search query: ")
            search_notes(query)
        elif choice == "8":
            edit_note()
        elif choice == "9":
            delete_note()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()
