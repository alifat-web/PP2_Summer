import csv
import os
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            phone VARCHAR(20)
        )
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Table created successfully!")



def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            username = row[0]
            phone = row[1]

            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (username, phone)
            )

    conn.commit()

    cur.close()
    conn.close()

    print("Contacts imported successfully!")

def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()

def insert_from_console():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Enter username: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (username, phone)
    )

    conn.commit()

    cur.close()
    conn.close()

    print("Contact added successfully!")

def search_by_name():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Enter username: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE username = %s",
        (username,)
    )

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()

def search_by_phone():
    conn = get_connection()
    cur = conn.cursor()

    prefix = input("Enter phone prefix: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    cur.close()
    conn.close()

def update_contact():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Enter username to update: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE username = %s",
        (new_phone, username)
    )

    conn.commit()

    cur.close()
    conn.close()

    print("Contact updated successfully!")

def delete_contact():
    conn = get_connection()
    cur = conn.cursor()

    username = input("Enter username to delete: ")

    cur.execute(
        "DELETE FROM phonebook WHERE username = %s",
        (username,)
    )

    conn.commit()

    cur.close()
    conn.close()

    print("Contact deleted successfully!")

#create_table()

while True:
    print("\nphonebook")
    print("1 import contacts from CSV")
    print("2 add contact")
    print("3 show all contacts")
    print("4 search by name")
    print("5 search by phone prefix")
    print("6 update")
    print("7 delete")
    print("0 exit")

    choice = input("Выберите действие: ")

    if choice == "1":
        insert_from_csv("Practice7/contacts.csv")

    elif choice == "2":
        insert_from_console()

    elif choice == "3":
        show_contacts()

    elif choice == "4":
        search_by_name()

    elif choice == "5":
        search_by_phone()

    elif choice == "6":
        update_contact()

    elif choice == "7":
        delete_contact()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid option!")