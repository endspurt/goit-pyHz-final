import json
import os
import re
from datetime import datetime, timedelta

# Dateipfad für die JSON-Daten
DATA_FILE = 'personal_assistant_data.json'

# Helper-Funktionen
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {'contacts': [], 'notes': []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone(phone):
    return re.match(r"^\+?[1-9]\d{1,14}$", phone) is not None

def find_contacts_by_name(data, name):
    return [contact for contact in data['contacts'] if name.lower() in contact['name'].lower()]

def find_notes_by_tag(data, tag):
    return [note for note in data['notes'] if tag.lower() in note.get('tags', '').lower()]

def upcoming_birthdays(data, days):
    today = datetime.today()
    upcoming = []
    for contact in data['contacts']:
        if 'birthday' in contact:
            birthday = datetime.strptime(contact['birthday'], "%Y-%m-%d")
            birthday_this_year = birthday.replace(year=today.year)
            if 0 <= (birthday_this_year - today).days < days:
                upcoming.append(contact)
    return upcoming

# Hauptfunktionen
def add_contact(data):
    name = input("Name: ")
    address = input("Address: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    
    if not validate_phone(phone):
        print("Invalid phone number.")
        return
    if not validate_email(email):
        print("Invalid email address.")
        return
    
    data['contacts'].append({
        'name': name,
        'address': address,
        'phone': phone,
        'email': email,
        'birthday': birthday
    })
    save_data(data)
    print("Contact added.")

def edit_contact(data):
    name = input("Enter the name of the contact to edit: ")
    contacts = find_contacts_by_name(data, name)
    if not contacts:
        print("No contacts found.")
        return
    
    contact = contacts[0]
    print(f"Editing contact: {contact['name']}")
    contact['address'] = input(f"Address ({contact['address']}): ") or contact['address']
    contact['phone'] = input(f"Phone ({contact['phone']}): ") or contact['phone']
    contact['email'] = input(f"Email ({contact['email']}): ") or contact['email']
    contact['birthday'] = input(f"Birthday ({contact['birthday']}): ") or contact['birthday']
    
    if not validate_phone(contact['phone']):
        print("Invalid phone number.")
        return
    if not validate_email(contact['email']):
        print("Invalid email address.")
        return
    
    save_data(data)
    print("Contact updated.")

def delete_contact(data):
    name = input("Enter the name of the contact to delete: ")
    contacts = find_contacts_by_name(data, name)
    if not contacts:
        print("No contacts found.")
        return
    
    data['contacts'].remove(contacts[0])
    save_data(data)
    print("Contact deleted.")

def search_contact(data):
    name = input("Enter the name to search: ")
    contacts = find_contacts_by_name(data, name)
    if not contacts:
        print("No contacts found.")
        return
    
    for contact in contacts:
        print(contact)

def list_upcoming_birthdays(data):
    days = int(input("Enter the number of days to check for upcoming birthdays: "))
    upcoming = upcoming_birthdays(data, days)
    if not upcoming:
        print("No upcoming birthdays.")
        return
    
    for contact in upcoming:
        print(contact)

def add_note(data):
    title = input("Title: ")
    content = input("Content: ")
    tags = input("Tags (comma-separated): ")
    
    data['notes'].append({
        'title': title,
        'content': content,
        'tags': tags
    })
    save_data(data)
    print("Note added.")

def edit_note(data):
    title = input("Enter the title of the note to edit: ")
    notes = [note for note in data['notes'] if title.lower() in note['title'].lower()]
    if not notes:
        print("No notes found.")
        return
    
    note = notes[0]
    print(f"Editing note: {note['title']}")
    note['content'] = input(f"Content ({note['content']}): ") or note['content']
    note['tags'] = input(f"Tags ({note['tags']}): ") or note['tags']
    
    save_data(data)
    print("Note updated.")

def delete_note(data):
    title = input("Enter the title of the note to delete: ")
    notes = [note for note in data['notes'] if title.lower() in note['title'].lower()]
    if not notes:
        print("No notes found.")
        return
    
    data['notes'].remove(notes[0])
    save_data(data)
    print("Note deleted.")

def search_note_by_tag(data):
    tag = input("Enter the tag to search: ")
    notes = find_notes_by_tag(data, tag)
    if not notes:
        print("No notes found.")
        return
    
    for note in notes:
        print(note)

def help():
    print("Available commands:")
    print("  1. Add contact")
    print("  2. Edit contact")
    print("  3. Delete contact")
    print("  4. Search contact")
    print("  5. Upcoming birthdays")
    print("  6. Add note")
    print("  7. Edit note")
    print("  8. Delete note")
    print("  9. Search note by tag")
    print("  0. Help")
    print("  10. Exit")

# Hauptprogramm
def main():
    data = load_data()
    
    while True:
        help()
        try:
            command = int(input("Enter a command number: ").strip())
        except ValueError:
            print("Invalid command number.")
            continue
        
        if command == 1:
            add_contact(data)
        elif command == 2:
            edit_contact(data)
        elif command == 3:
            delete_contact(data)
        elif command == 4:
            search_contact(data)
        elif command == 5:
            list_upcoming_birthdays(data)
        elif command == 6:
            add_note(data)
        elif command == 7:
            edit_note(data)
        elif command == 8:
            delete_note(data)
        elif command == 9:
            search_note_by_tag(data)
        elif command == 0:
            help()
        elif command == 10:
            break
        else:
            print("Unknown command number. Type '0' for a list of commands.")

if __name__ == "__main__":
    main()
