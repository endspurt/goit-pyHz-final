import json
import os
import re
from datetime import datetime, timedelta

# File paths for contacts and notes
CONTACTS_FILE = 'contacts.json'
NOTES_FILE = 'notes.json'

# Function to load data from a JSON file
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

# Function to save data to a JSON file
def save_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Function to validate email address format
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to validate phone number format
def validate_phone(phone):
    return re.match(r"^\+?1?\d{9,15}$", phone)

# Function to add a new contact
def add_contact():
    data = load_data(CONTACTS_FILE)
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

# Function to list upcoming birthdays
def list_upcoming_birthdays():
    data = load_data(CONTACTS_FILE)
    days = int(input("Enter number of days: "))
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

# Function to search contacts by name
def search_contacts():
    data = load_data(CONTACTS_FILE)
    query = input("Enter search query: ").strip().lower()
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

# Function to edit an existing contact
def edit_contact():
    data = load_data(CONTACTS_FILE)
    name = input("Enter contact name to edit: ").strip().lower()
    for contact in data:
        if contact["name"].lower() == name:
            contact["address"] = input(f"New address ({contact['address']}): ") or contact["address"]
            contact["phone"] = input(f"New phone ({contact['phone']}): ") or contact["phone"]
            contact["email"] = input(f"New email ({contact['email']}): ") or contact["email"]
            contact["birthday"] = input(f"New birthday ({contact['birthday']}): ") or contact["birthday"]
            save_data(data, CONTACTS_FILE)
            print("Contact updated successfully")
            return
    print("Contact not found")

# Function to delete a contact
def delete_contact():
    data = load_data(CONTACTS_FILE)
    name = input("Enter contact name to delete: ").strip().lower()
    data = [contact for contact in data if contact["name"].lower() != name]
    save_data(data, CONTACTS_FILE)
    print("Contact deleted successfully")

# Function to add a new note
def add_note():
    data = load_data(NOTES_FILE)
    text = input("Note text: ")
    tags = input("Tags (comma-separated): ").split(",")
    note = {"text": text, "tags": [tag.strip() for tag in tags]}
    data.append(note)
    save_data(data, NOTES_FILE)
    print("Note added successfully")

# Function to search notes by text or tags
def search_notes():
    data = load_data(NOTES_FILE)
    query = input("Enter search query: ").strip().lower()
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

# Function to edit an existing note
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

# Function to delete a note
def delete_note():
    data = load_data(NOTES_FILE)
    note_text = input("Enter note text to delete: ").strip().lower()
    data = [note for note in data if note["text"].lower() != note_text]
    save_data(data, NOTES_FILE)
    print("Note deleted successfully")

# Function to display the main menu
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

# Main function to handle user input and call the appropriate functions
def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            list_upcoming_birthdays()
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            edit_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            add_note()
        elif choice == "7":
            search_notes()
        elif choice == "8":
            edit_note()
        elif choice == "9":
            delete_note()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()



'''Importing Modules:

import json: To handle JSON file reading and writing.
import os: To check if files exist.
import re: To use regular expressions for validating email and phone formats.
from datetime import datetime, timedelta: To work with dates and times.
File Paths:

CONTACTS_FILE = 'contacts.json': Path to the JSON file storing contacts.
NOTES_FILE = 'notes.json': Path to the JSON file storing notes.
Load and Save Data Functions:

load_data(file): Loads data from a JSON file. Returns an empty list if the file does not exist.
save_data(data, file): Saves data to a JSON file with indentation for readability.
Validation Functions:

validate_email(email): Validates the email format using a regular expression.
validate_phone(phone): Validates the phone format using a regular expression.
Contact Management Functions:

add_contact(): Adds a new contact to the contacts list.
list_upcoming_birthdays(): Lists contacts with birthdays in the next specified number of days.
search_contacts(): Searches for contacts by name.
edit_contact(): Edits an existing contact.
delete_contact(): Deletes a contact by name.
Note Management Functions:

add_note(): Adds a new note to the notes list.
search_notes(): Searches for notes by text or tags.
edit_note(): Edits an existing note.
delete_note(): Deletes a note by text.
Main Menu and Main Function:

main_menu(): Displays the main menu with options.
main(): Handles user input and calls the appropriate functions based on the user's choice.'''