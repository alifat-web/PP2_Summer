from connect import get_connection


def search_pattern():
    conn = get_connection()
    cur = conn.cursor()

    pattern = input("Enter name or phone: ")

    cur.execute(
        "SELECT * FROM search_pattern(%s)",
        (pattern,)
    )

    contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def show_paginated():
    conn = get_connection()
    cur = conn.cursor()

    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts.")

    cur.close()
    conn.close()


def upsert_contact():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Username: ")
    phone = input("Phone: ")

    cur.execute(
        "CALL upsert_contact(%s, %s)",
        (username, phone)
    )

    conn.commit()

    print("Contact inserted/updated successfully!")

    cur.close()
    conn.close()


def delete_contact():
    conn = get_connection()
    cur = conn.cursor()

    value = input("Enter username or phone: ")

    cur.execute(
        "CALL delete_contact(%s)",
        (value,)
    )

    conn.commit()

    print("Contact deleted successfully!")

    cur.close()
    conn.close()


def insert_many():
    conn = get_connection()
    cur = conn.cursor()

    usernames = []
    phones = []

    count = int(input("How many contacts? "))

    for i in range(count):
        print(f"\nContact {i + 1}")

        usernames.append(input("Username: "))
        phones.append(input("Phone: "))

    cur.execute(
        "CALL insert_many_contacts(%s, %s)",
        (usernames, phones)
    )

    conn.commit()

    print("Bulk insert finished.")

    cur.close()
    conn.close()


while True:

    print("\n===== PHONEBOOK =====")
    print("1. Search by pattern")
    print("2. Insert or update contact")
    print("3. Insert many contacts")
    print("4. Show contacts (pagination)")
    print("5. Delete contact")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        search_pattern()

    elif choice == "2":
        upsert_contact()

    elif choice == "3":
        insert_many()

    elif choice == "4":
        show_paginated()

    elif choice == "5":
        delete_contact()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")