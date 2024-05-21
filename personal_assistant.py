import json
import re
from datetime import datetime, timedelta

# Contact class to represent a contact
class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "birthday": self.birthday.strftime("%Y-%m-%d")
        }

# Note class to represent a note
class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags or []

    def to_dict(self):
        return {
            "text": self.text,
            "tags": self.tags
        }

# Personal Assistant class
class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.load_data()

    def load_data(self):
        # Load contacts from file
        try:
            with open("contacts.json", "r") as file:
                contacts_data = json.load(file)
                self.contacts = [Contact(c["name"], c["address"], c["phone"], c["email"], datetime.strptime(c["birthday"], "%Y-%m-%d")) for c in contacts_data]
        except FileNotFoundError:
            print("contacts.json not found. Starting with an empty contact list.")
        except json.JSONDecodeError:
            print("Error reading contacts.json. Starting with an empty contact list.")

        # Load notes from file
        try:
            with open("notes.json", "r") as file:
                notes_data = json.load(file)
                self.notes = [Note(n["text"], n["tags"]) for n in notes_data]
        except FileNotFoundError:
            print("notes.json not found. Starting with an empty notes list.")
        except json.JSONDecodeError:
            print("Error reading notes.json. Starting with an empty notes list.")

    def save_data(self):
        with open("contacts.json", "w") as file:
            contacts_data = [c.to_dict() for c in self.contacts]
            json.dump(contacts_data, file, indent=4)

        with open("notes.json", "w") as file:
            notes_data = [n.to_dict() for n in self.notes]
            json.dump(notes_data, file, indent=4)

    def add_contact(self, name, address, phone, email, birthday):
        if not re.match(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$", phone):
            print("Invalid phone number!")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print("Invalid email address!")
            return

        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            print("Invalid birthday date format!")
            return

        contact = Contact(name, address, phone, email, birthday_date)
        self.contacts.append(contact)
        self.save_data()
        print("Contact added successfully!")

    def search_contacts(self, query):
        matching_contacts = [c for c in self.contacts if query.lower() in c.name.lower()]
        self.display_contacts(matching_contacts)

    def display_contacts(self, contacts):
        if not contacts:
            print("No contacts found.")
        else:
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. Name: {contact.name}")
                print(f"   Address: {contact.address}")
                print(f"   Phone: {contact.phone}")
                print(f"   Email: {contact.email}")
                print(f"   Birthday: {contact.birthday.strftime('%Y-%m-%d')}")
                print()

    def edit_contact(self, index, name, address, phone, email, birthday):
        if not re.match(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$", phone):
            print("Invalid phone number!")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print("Invalid email address!")
            return

        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            print("Invalid birthday date format!")
            return

        if 0 <= index < len(self.contacts):
            contact = self.contacts[index]
            contact.name = name
            contact.address = address
            contact.phone = phone
            contact.email = email
            contact.birthday = birthday_date
            self.save_data()
            print("Contact updated successfully!")
        else:
            print("Invalid contact index!")

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save_data()
            print("Contact deleted successfully!")
        else:
            print("Invalid contact index!")

    def list_upcoming_birthdays(self, days):
        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        upcoming_birthdays = [c for c in self.contacts if today <= c.birthday.date() <= end_date]

        if upcoming_birthdays:
            print(f"Upcoming birthdays in the next {days} days:")
            self.display_contacts(upcoming_birthdays)
        else:
            print("No upcoming birthdays found.")

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)
        self.save_data()
        print("Note added successfully!")

    def search_notes(self, query):
        matching_notes = [n for n in self.notes if query.lower() in n.text.lower() or query.lower() in [t.lower() for t in n.tags]]
        self.display_notes(matching_notes)

    def display_notes(self, notes):
        if not notes:
            print("No notes found.")
        else:
            for i, note in enumerate(notes, start=1):
                print(f"{i}. Text: {note.text}")
                print(f"   Tags: {', '.join(note.tags)}")
                print()

    def edit_note(self, index, text, tags=None):
        if 0 <= index < len(self.notes):
            note = self.notes[index]
            note.text = text
            note.tags = tags or []
            self.save_data()
            print("Note updated successfully!")
        else:
            print("Invalid note index!")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_data()
            print("Note deleted successfully!")
        else:
            print("Invalid note index!")

    def suggest_command(self, query):
        if "add" in query.lower() and "contact" in query.lower():
            print("Suggested command: add_contact")
        elif "search" in query.lower() and "contact" in query.lower():
            print("Suggested command: search_contacts")
        elif "edit" in query.lower() and "contact" in query.lower():
            print("Suggested command: edit_contact")
        elif "delete" in query.lower() and "contact" in query.lower():
            print("Suggested command: delete_contact")
        elif "birthday" in query.lower() or "upcoming" in query.lower():
            print("Suggested command: list_upcoming_birthdays")
        elif "add" in query.lower() and "note" in query.lower():
            print("Suggested command: add_note")
        elif "search" in query.lower() and "note" in query.lower():
            print("Suggested command: search_notes")
        elif "edit" in query.lower() and "note" in query.lower():
            print("Suggested command: edit_note")
        elif "delete" in query.lower() and "note" in query.lower():
            print("Suggested command: delete_note")
        else:
            print("No command suggestion available.")

def main():
    assistant = PersonalAssistant()

    while True:
        print("\nPersonal Assistant Menu:")
        print("1. Add Contact")
        print("2. Search Contacts")
        print("3. Edit Contact")
        print("4. Delete Contact")
        print("5. List Upcoming Birthdays")
        print("6. Add Note")
        print("7. Search Notes")
        print("8. Edit Note")
        print("9. Delete Note")
        print("10. Suggest Command")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            address = input("Enter address: ")
            phone = input("Enter phone number: ")
            email = input("Enter email address: ")
            birthday = input("Enter birthday (YYYY-MM-DD): ")
            assistant.add_contact(name, address, phone, email, birthday)
        elif choice == "2":
            query = input("Enter search query: ")
            assistant.search_contacts(query)
        elif choice == "3":
            print("Here are your contacts:")
            assistant.display_contacts(assistant.contacts)
            index = int(input("Enter contact index: ")) - 1
            name = input("Enter updated name: ")
            address = input("Enter updated address: ")
            phone = input("Enter updated phone number: ")
            email = input("Enter updated email address: ")
            birthday = input("Enter updated birthday (YYYY-MM-DD): ")
            assistant.edit_contact(index, name, address, phone, email, birthday)
        elif choice == "4":
            print("Here are your contacts:")
            assistant.display_contacts(assistant.contacts)
            index = int(input("Enter contact index: ")) - 1
            assistant.delete_contact(index)
        elif choice == "5":
            days = int(input("Enter number of days: "))
            assistant.list_upcoming_birthdays(days)
        elif choice == "6":
            text = input("Enter note text: ")
            tags_input = input("Enter tags (comma-separated): ")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            assistant.add_note(text, tags)
        elif choice == "7":
            query = input("Enter search query: ")
            assistant.search_notes(query)
        elif choice == "8":
            print("Here are your notes:")
            assistant.display_notes(assistant.notes)
            index = int(input("Enter note index: ")) - 1
            text = input("Enter updated note text: ")
            tags_input = input("Enter updated tags (comma-separated): ")
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            assistant.edit_note(index, text, tags)
        elif choice == "9":
            print("Here are your notes:")
            assistant.display_notes(assistant.notes)
            index = int(input("Enter note index: ")) - 1
            assistant.delete_note(index)
        elif choice == "10":
            query = input("Enter your query: ")
            assistant.suggest_command(query)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
