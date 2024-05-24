import json
import os
import re
from datetime import datetime
from functools import wraps


CONTACTS_FILE = 'contacts.json'
NOTES_FILE = 'notes.json'


def load_data_decorator(file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = load_data(file)
            return func(data, *args, **kwargs)
        return wrapper
    return decorator


def save_data_decorator(file):
    def decorator(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            result = func(data, *args, **kwargs)
            save_data(data, file)
            return result
        return wrapper
    return decorator


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


class PersonalAssistant:
    def __init__(self):
        self.contacts_file = CONTACTS_FILE
        self.notes_file = NOTES_FILE

    def get_user_input(self, prompt, validation_func=None, error_msg="Invalid input"):
        while True:
            value = input(prompt).strip()
            if validation_func and not validation_func(value):
                print(error_msg)
            else:
                return value

    @load_data_decorator(CONTACTS_FILE)
    @save_data_decorator(CONTACTS_FILE)
    def add_contact(self, data):
        name = self.get_user_input("Name: ")
        address = self.get_user_input("Address: ")
        phone = self.get_user_input("Phone: ", validate_phone, "Invalid phone format")
        email = self.get_user_input("Email: ", validate_email, "Invalid email format")
        birthday = self.get_user_input("Birthday (YYYY-MM-DD): ")

        contact = {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "birthday": birthday
        }
        data.append(contact)
        print("Contact added successfully")

    @load_data_decorator(CONTACTS_FILE)
    def list_upcoming_birthdays(self, data):
        days = int(self.get_user_input("Enter number of days: "))
        today = datetime.today()
        upcoming = []
        for contact in data:
            try:
                birthday = datetime.strptime(contact["birthday"], "%Y-%m-%d")
                this_year_birthday = birthday.replace(year=today.year)
                if 0 <= (this_year_birthday - today).days <= days:
                    upcoming.append(contact)
            except ValueError:
                print(f"Invalid birthday format for contact: {contact['name']}")

        if not upcoming:
            print("No upcoming birthdays in the next", days, "days")
        else:
            for contact in upcoming:
                print(contact)

    @load_data_decorator(CONTACTS_FILE)
    def search_contacts(self, data):
        query = self.get_user_input("Enter search query: ").lower()
        results = [contact for contact in data if query in contact["name"].lower()]
        if results:
            print("Search results:")
            for result in results:
                print(json.dumps(result, indent=4))
        else:
            print("No contacts found with the name:", query)

    @load_data_decorator(CONTACTS_FILE)
    @save_data_decorator(CONTACTS_FILE)
    def edit_contact(self, data):
        name = self.get_user_input("Enter contact name to edit: ").lower()
        for contact in data:
            if contact["name"].lower() == name:
                contact["address"] = self.get_user_input(f"New address ({contact['address']}): ") or contact["address"]
                contact["phone"] = self.get_user_input(f"New phone ({contact['phone']}): ", validate_phone, "Invalid phone format") or contact["phone"]
                contact["email"] = self.get_user_input(f"New email ({contact['email']}): ", validate_email, "Invalid email format") or contact["email"]
                contact["birthday"] = self.get_user_input(f"New birthday ({contact['birthday']}): ") or contact["birthday"]
                print("Contact updated successfully")
                return
        print("Contact not found")

    @load_data_decorator(CONTACTS_FILE)
    @save_data_decorator(CONTACTS_FILE)
    def delete_contact(self, data):
        name = self.get_user_input("Enter contact name to delete: ").lower()
        data[:] = [contact for contact in data if contact["name"].lower() != name]
        print("Contact deleted successfully")

    @load_data_decorator(NOTES_FILE)
    @save_data_decorator(NOTES_FILE)
    def add_note(self, data):
        text = self.get_user_input("Note text: ")
        tags = self.get_user_input("Tags (comma-separated): ").split(",")
        note = {"text": text, "tags": [tag.strip() for tag in tags]}
        data.append(note)
        print("Note added successfully")

    @load_data_decorator(NOTES_FILE)
    def search_notes(self, data):
        query = self.get_user_input("Enter search query: ").lower()
        results = [note for note in data if query in note["text"].lower() or query in [tag.lower() for tag in note["tags"]]]
        if results:
            print("Search results:")
            for result in results:
                print(json.dumps(result, indent=4))
        else:
            print("No notes found with the query:", query)

    @load_data_decorator(NOTES_FILE)
    @save_data_decorator(NOTES_FILE)
    def edit_note(self, data):
        note_text = self.get_user_input("Enter note text to edit: ").lower()
        for note in data:
            if note["text"].lower() == note_text:
                note["text"] = self.get_user_input(f"New text ({note['text']}): ") or note["text"]
                note["tags"] = self.get_user_input(f"New tags (comma-separated) ({', '.join(note['tags'])}): ").split(",") or note["tags"]
                print("Note updated successfully")
                return
        print("Note not found")

    @load_data_decorator(NOTES_FILE)
    @save_data_decorator(NOTES_FILE)
    def delete_note(self, data):
        note_text = self.get_user_input("Enter note text to delete: ").lower()
        data[:] = [note for note in data if note["text"].lower() != note_text]
        print("Note deleted successfully")

    def main_menu(self):
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

    def main(self):
        while True:
            self.main_menu()
            choice = self.get_user_input("Enter your choice: ")
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid choice. Please enter a number between 1 and 10.")
                continue

            if choice == 1:
                self.add_contact()
            elif choice == 2:
                self.list_upcoming_birthdays()
            elif choice == 3:
                self.search_contacts()
            elif choice == 4:
                self.edit_contact()
            elif choice == 5:
                self.delete_contact()
            elif choice == 6:
                self.add_note()
            elif choice == 7:
                self.search_notes()
            elif choice == 8:
                self.edit_note()
            elif choice == 9:
                self.delete_note()
            elif choice == 10:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.main()
