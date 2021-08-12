from include import *

import window
import database
import printer

from datetime import datetime, timedelta
import atexit
import csv

root = window.create_window("Hall Pass Printer", 1000, 750)
handler_id = ''
headerframe = window.frame(root, anchor=window.N, fill='x')
contentframe = window.frame(root, anchor=window.N, fill='both')
conn = database.open_connection(STORAGE_LOCATION + "hallpass.db")
p = printer.get_usb_printer()
database.execute(conn, TABLE_STUDENTS)
database.execute(conn, TABLE_RECORDS)
atexit.register(database.close_connection, conn)


def key_handler(event: window.Event):
    """Handles barcode/key input"""
    if key_handler.barcode > 0 and datetime.now() - key_handler.last_entered > timedelta(seconds=1):
        key_handler.barcode = 0
    elif event.char.isnumeric():
        key_handler.barcode = key_handler.barcode * \
            10 + int(event.char)
    elif event.char in ('\r', '\n'):
        if key_handler.barcode != 0:
            barcode_handler(key_handler.barcode)
        key_handler.barcode = 0
    else:
        return
    key_handler.last_entered = datetime.now()


key_handler.last_entered = datetime.now()
key_handler.barcode = 0


def barcode_handler(barcode: int):
    """Handles full barcode entered"""
    matches = database.query(conn, QUERY_STUDENT_ID, barcode)
    if len(matches) > 0:
        match = matches[0]
        if p is not None:
            printer.print_text("HALL PASS")
            printer.print_text(match[1])
        database.execute(conn, INSERT_RECORD, barcode)
        database.commit(conn)
        log("Printed hall pass for {}", matches[0])
    else:
        log("No matches for {}", barcode)


def clear_screen():
    global handler_id

    for widget in headerframe.winfo_children():
        window.destroy_widget(widget)
    for widget in contentframe.winfo_children():
        window.destroy_widget(widget)
    if handler_id != '':
        window.unbind_key_event(handler_id)
        handler_id = ''


def main_menu():
    clear_screen()
    window.text(headerframe, "Main Menu", fontsize=40)
    centeredframe = window.frame(
        contentframe, anchor=window.N, marginx=0, marginy=0)
    window.button(centeredframe, "Setup Program",
                  setup_program, side=window.LEFT, marginx=10)
    window.button(centeredframe, "Hall Pass Printing Program",
                  scan, side=window.LEFT, marginx=10)


def setup_program():
    clear_screen()
    window.text(headerframe, "Setup Program", fontsize=40)
    window.button(headerframe, "Back", main_menu, anchor=window.NW)
    window.button(contentframe, "Upload student list", upload_student_list)


def scan():
    clear_screen()
    window.text(headerframe, "Hall Pass Printing Program", fontsize=40)
    window.button(headerframe, "Back", main_menu, anchor=window.NW)
    window.text(contentframe,
                "Please scan your ID card to print out a hall pass.", anchor=window.NW)
    window.bind_key_event(root, key_handler)


def upload_student_list():
    f = window.file_dialog('r', [("Comma Separated Value Files", "*.csv")])
    if f is None:
        return
    csv_reader = csv.reader(f)
    id_col = -1
    name_col = -1
    lname_col = -1
    mname_col = -1
    for row in csv_reader:
        if id_col == -1:
            for i, col in enumerate(row):
                if "first" in col.lower():
                    name_col = i
                elif "last" in col.lower():
                    lname_col = i
                elif "middle" in col.lower():
                    mname_col = i
                elif "name" in col.lower():
                    name_col = i
                elif "id" in col.lower():
                    id_col = i
            print(id_col)
            if id_col == -1:
                # TODO: Add alert
                log("Error adding student data: no ID column found.")
                return
            if name_col == -1:
                log("Error adding student data: no Name column found.")
                return
        else:
            id = int(row[id_col])
            name = ""
            if lname_col != -1:
                name = "{}, {}".format(
                    row[lname_col].strip(), row[name_col].strip())
                if mname_col != -1 and row[mname_col].strip() != "":
                    name += " " + row[mname_col].strip()
            else:
                name = row[name_col].strip()
            database.execute(conn, INSERT_STUDENT, id, name)

    database.commit(conn)
    f.close()


main_menu()
window.loop_window(root)
