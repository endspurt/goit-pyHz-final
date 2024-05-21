import json

def search_contacts(file_path, query):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format in the file.")
        return

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

# Beispielaufruf der Funktion
file_path = "contacts.json"
while True:
    query = input("Enter a name to search (or 'q' to quit): ")
    if query.lower() == 'q':
        break
    search_contacts(file_path, query)
