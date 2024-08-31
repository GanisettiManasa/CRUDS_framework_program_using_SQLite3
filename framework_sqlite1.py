# CRUDS Framework program using SQLite3

import sqlite3

TABLE_NAME = "fwTable"
CONFIG_TABLE_NAME = "fwConfig"

conn = sqlite3.connect('framework.db')
cursor = conn.cursor()
cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
fieldNames = cursor.fetchall()
fields = [field[1] for field in fieldNames]
menuOptions = [addRecords, showRecords, updateRecord, deleteRecord, searchRecord, exitProgram]


def addRecords():
    values = []
    for field in fields:
        value = input(f"Enter {field}: ")
        values.append(f"'{value}'")
    cursor.execute(f"INSERT INTO {TABLE_NAME} ({', '.join(fields)}) VALUES ({', '.join(values)})")
    conn.commit()
    savedMessage = cursor.execute(f"SELECT value FROM {CONFIG_TABLE_NAME} WHERE key='Saved_Message'").fetchone()[0]
    print(savedMessage)

def showRecords():
    showMessage = cursor.execute(f"SELECT value FROM {CONFIG_TABLE_NAME} WHERE key='Show_Message'").fetchone()[0]
    print(showMessage)
    print(" | ".join(fields))

    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    records = cursor.fetchall()
    for record in records:
        print(" | ".join(str(value) for value in record))

def updateRecord():
    recordId = input(f"Enter {fields[0]} to update: ")
    for index, field in enumerate(fields):
        print(f"{index + 1}. {field}")
    choice = int(input("Enter the number of the field to update: ")) - 1
    newValue = input(f"Enter new value for {fields[choice]}: ")
    cursor.execute(f"UPDATE {TABLE_NAME} SET {fields[choice]} = '{newValue}' WHERE {fields[0]} = '{recordId}'")
    conn.commit()
    updateMessage = cursor.execute(f"SELECT value FROM {CONFIG_TABLE_NAME} WHERE key='Update_Message'").fetchone()[0]
    print(updateMessage)

def deleteRecord():
    recordId = input(f"Enter {fields[0]} to delete: ")
    cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE {fields[0]} = '{recordId}'")
    conn.commit()
    deleteMessage = cursor.execute(f"SELECT value FROM {CONFIG_TABLE_NAME} WHERE key='Delete_Message'").fetchone()[0]
    print(deleteMessage)

def searchRecord():
    recordId = input(f"Enter {fields[0]} to search: ")
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {fields[0]} = '{recordId}'")
    print(" | ".join(fields))
    records = cursor.fetchall()
    for record in records:
        print(" | ".join(str(value) for value in record))
    
def exitProgram():
    print("Exiting program.")
    conn.close()
    exit()

def menu():
    while True:
        cursor.execute(f"SELECT value FROM {CONFIG_TABLE_NAME} WHERE key='Menu'")
        menu = cursor.fetchone()
        if menu:
            print(menu[0].replace('\\n', '\n'))      
        choice = int(input("Enter your choice: "))  
        if 1 <= choice <= len(menuOptions):
            menuOptions[choice - 1]()
        else:
            print("Invalid choice, please try again.")
menu()
