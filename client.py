import xmlrpc.client

SERVER_URL = "http://localhost:8000/"

def handle_server_response(response):
    if isinstance(response, str) and response.startswith("An error occurred"):
        print("Error from server:", response)
    else:
        return True  # Proceed with the normal flow
    return False  # Indicates an error occurred

def add_note():
    with xmlrpc.client.ServerProxy(SERVER_URL) as proxy:
        topic = input("Enter topic: ").strip()
        note_name = input("Enter note name: ").strip()
        text = input("Enter text: ").strip()

        if topic and note_name and text:
            # Only proceed if all fields are filled
            result = proxy.add_note(topic, note_name, text)
            print(result)
        else:
            print("All fields are required. Please try again.")

def get_notes():
    with xmlrpc.client.ServerProxy(SERVER_URL) as proxy:
        topic = input("Enter topic to retrieve notes: ")
        notes = proxy.get_notes(topic)
        if handle_server_response(notes):
            if notes:
                for note in notes:
                    print(note)
            else:
                print("No notes found for this topic.")

def wikipedia_search():
    with xmlrpc.client.ServerProxy(SERVER_URL) as proxy:
        topic = input("Enter topic to search on Wikipedia: ")
        result = proxy.wikipedia_search(topic)
        if handle_server_response(result):
            print("Wikipedia search result:", result)

def append_wikipedia():
    with xmlrpc.client.ServerProxy(SERVER_URL) as proxy:
        topic = input("Enter topic to append Wikipedia data: ")
        wikipedia_url = proxy.wikipedia_search(topic)
        if handle_server_response(wikipedia_url):
            if wikipedia_url.startswith("http"):
                print(f"Appending Wikipedia link to topic '{topic}'")
                result = proxy.append_wikipedia_to_topic(topic, wikipedia_url)
                if handle_server_response(result):
                    print(result)

def main():
    while True:
        print("\n1. Add Note")
        print("2. Get Notes")
        print("3. Search Wikipedia")
        print("4. Append Wikipedia Result to Topic")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_note()
        elif choice == '2':
            get_notes()
        elif choice == '3':
            wikipedia_search()
        elif choice == '4':
            append_wikipedia()
        elif choice == '5':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
