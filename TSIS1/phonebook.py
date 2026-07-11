import csv
import json
from connect import get_connection


def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Username: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    group = cur.fetchone()

    if group is None:
        cur.execute(
            "INSERT INTO groups(name) VALUES(%s) RETURNING id",
            (group_name,)
        )

        group_id = cur.fetchone()[0]

    else:
        group_id = group[0]

    cur.execute(
        """
        INSERT INTO contacts(username,email,birthday,group_id)
        VALUES(%s,%s,%s,%s)
        """,
        (username, email, birthday, group_id)
    )

    conn.commit()

    print("Contact added successfully!")

    cur.close()
    conn.close()


def add_phone():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Username: ")
    phone = input("Phone: ")
    phone_type = input("Type (home/work/mobile): ")

    cur.execute(
        "CALL add_phone(%s,%s,%s)",
        (username, phone, phone_type)
    )

    conn.commit()

    print("Phone added successfully!")

    cur.close()
    conn.close()


def search_contacts():
    conn = get_connection()
    cur = conn.cursor()

    query = input("Search: ")

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("Nothing found.")

    cur.close()
    conn.close()


def search_email():
    conn = get_connection()
    cur = conn.cursor()

    email = input("Part of email: ")

    cur.execute(
        """
        SELECT username,email
        FROM contacts
        WHERE email ILIKE %s
        """,
        ("%" + email + "%",)
    )

    contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("Nothing found.")

    cur.close()
    conn.close()


def filter_group():
    conn = get_connection()
    cur = conn.cursor()

    group_name = input("Group: ")

    cur.execute(
        """
        SELECT c.username,
               c.email,
               c.birthday,
               g.name
        FROM contacts c
        JOIN groups g
        ON c.group_id = g.id
        WHERE g.name = %s
        """,
        (group_name,)
    )

    contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts.")

    cur.close()
    conn.close()

def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()

    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        sql = """
        SELECT username, email, birthday
        FROM contacts
        ORDER BY username
        """

    elif choice == "2":
        sql = """
        SELECT username, email, birthday
        FROM contacts
        ORDER BY birthday
        """

    elif choice == "3":
        sql = """
        SELECT username, email, birthday
        FROM contacts
        ORDER BY created_at
        """

    else:
        print("Invalid option.")
        cur.close()
        conn.close()
        return

    cur.execute(sql)

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()


def pagination():

    conn = get_connection()
    cur = conn.cursor()

    limit = 5
    offset = 0

    while True:

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s,%s)",
            (limit, offset)
        )

        contacts = cur.fetchall()

        print("\n========== PAGE ==========")

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("No contacts.")

        print("\nn - next page")
        print("p - previous page")
        print("q - quit")

        choice = input("Choose: ")

        if choice == "n":
            offset += limit

        elif choice == "p":

            if offset >= limit:
                offset -= limit

        elif choice == "q":
            break

        else:
            print("Invalid option.")

    cur.close()
    conn.close()


def export_json():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        c.username,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c

    LEFT JOIN groups g
    ON c.group_id = g.id

    LEFT JOIN phones p
    ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = []

    for row in rows:

        data.append(
            {
                "username": row[0],
                "email": row[1],
                "birthday": str(row[2]),
                "group": row[3],
                "phone": row[4],
                "type": row[5]
            }
        )

    with open("contacts.json", "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Export completed.")

    cur.close()
    conn.close()

def import_json():

    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for contact in data:

        cur.execute(
            "SELECT id FROM contacts WHERE username=%s",
            (contact["username"],)
        )

        existing = cur.fetchone()

        if existing:

            answer = input(
                f'{contact["username"]} already exists. Overwrite? (y/n): '
            )

            if answer.lower() != "y":
                continue

            cur.execute(
                """
                UPDATE contacts
                SET email=%s,
                    birthday=%s
                WHERE username=%s
                """,
                (
                    contact["email"],
                    contact["birthday"],
                    contact["username"]
                )
            )

        else:

            cur.execute(
                "SELECT id FROM groups WHERE name=%s",
                (contact["group"],)
            )

            group = cur.fetchone()

            if group is None:

                cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                    (contact["group"],)
                )

                group_id = cur.fetchone()[0]

            else:

                group_id = group[0]

            cur.execute(
                """
                INSERT INTO contacts(
                    username,
                    email,
                    birthday,
                    group_id
                )
                VALUES(%s,%s,%s,%s)
                RETURNING id
                """,
                (
                    contact["username"],
                    contact["email"],
                    contact["birthday"],
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones(
                    contact_id,
                    phone,
                    type
                )
                VALUES(%s,%s,%s)
                """,
                (
                    contact_id,
                    contact["phone"],
                    contact["type"]
                )
            )

    conn.commit()

    print("Import completed.")

    cur.close()
    conn.close()


def import_csv():

    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            username = row[0]
            email = row[1]
            birthday = row[2]
            group_name = row[3]
            phone = row[4]
            phone_type = row[5]

            cur.execute(
                "SELECT id FROM groups WHERE name=%s",
                (group_name,)
            )

            group = cur.fetchone()

            if group is None:

                cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                    (group_name,)
                )

                group_id = cur.fetchone()[0]

            else:

                group_id = group[0]

            cur.execute(
                """
                INSERT INTO contacts(
                    username,
                    email,
                    birthday,
                    group_id
                )
                VALUES(%s,%s,%s,%s)
                RETURNING id
                """,
                (
                    username,
                    email,
                    birthday,
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones(
                    contact_id,
                    phone,
                    type
                )
                VALUES(%s,%s,%s)
                """,
                (
                    contact_id,
                    phone,
                    phone_type
                )
            )

    conn.commit()

    print("CSV imported successfully.")

    cur.close()
    conn.close()


while True:

    print("\n========== PHONEBOOK ==========")
    print("1. Add contact")
    print("2. Add phone")
    print("3. Search")
    print("4. Search email")
    print("5. Filter by group")
    print("6. Sort")
    print("7. Pagination")
    print("8. Export JSON")
    print("9. Import JSON")
    print("10. Import CSV")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        add_contact()

    elif choice == "2":
        add_phone()

    elif choice == "3":
        search_contacts()

    elif choice == "4":
        search_email()

    elif choice == "5":
        filter_group()

    elif choice == "6":
        sort_contacts()

    elif choice == "7":
        pagination()

    elif choice == "8":
        export_json()

    elif choice == "9":
        import_json()

    elif choice == "10":
        import_csv()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")