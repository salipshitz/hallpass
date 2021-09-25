from include import *

import window
import database
import printer
import password

import datetime
import atexit
import csv
from PIL import Image
import os
import glob

root = window.create_window("Hall Pass Printer", 1000, 750)
handler_id = ''
headerframe = window.frame(root, anchor=window.N, fill='x')
contentframe = window.frame(root, anchor=window.N, fill='both')
conn = database.open_connection(STORAGE_LOCATION + "hallpass.db")
p = printer.get_usb_printer()
img: Union[Image.Image, None] = None
for fname in glob.glob(STORAGE_LOCATION + "printimage.*"):
    try:
        img = Image.open(fname)
    except FileNotFoundError:
        pass

database.execute(conn, TABLE_STUDENTS)
database.execute(conn, TABLE_RECORDS)
atexit.register(database.close_connection, conn)


def key_handler(event: window.Event):
    """Handles barcode/key input"""
    if key_handler.barcode > 0 and datetime.datetime.now() - key_handler.last_entered > datetime.timedelta(seconds=1):
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
    key_handler.last_entered = datetime.datetime.now()


key_handler.last_entered = datetime.datetime.now()
key_handler.barcode = 0


def barcode_handler(barcode: int):
    """Handles full barcode entered"""
    matches = database.query(conn, QUERY_STUDENT, barcode)
    if len(matches) > 0:
        match = matches[0]
        global p
        if p is None:
            p = printer.get_usb_printer()
        if p is not None:
            printer.print_text(p, "HALL PASS\n\n", size=2)
            printer.print_text(p, "NAME: {}\n".format(match[1]), size=1)
            printer.print_text(p, "ID: {}\n".format(match[0]))
            if img is not None:
                printer.print_image(p, img)
            printer.cut(p)
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
    window.button(contentframe, "Setup Program",
                  lambda: check_password(setup_program))
    window.button(contentframe, "Hall Pass Printing Program", scan)
    window.button(contentframe, "Statistics", statistics)
    window.button(contentframe, "Exit", exit)


def setup_program():
    clear_screen()
    window.text(headerframe, "Setup Program", fontsize=40)
    window.button(headerframe, "Back", main_menu, anchor=window.NW)
    window.button(contentframe, "Reset Password", reset_password)
    window.button(contentframe, "Upload student list", upload_student_list)
    window.button(contentframe, "Upload hall pass picture", upload_picture)


def scan():
    clear_screen()
    window.text(headerframe, "Hall Pass Printing Program", fontsize=40)
    window.button(headerframe, "Back",
                  lambda: check_password(main_menu), anchor=window.NW)
    window.text(contentframe,
                "Please scan your ID card to print out a hall pass.", anchor=window.NW)
    window.bind_key_event(root, key_handler)


def statistics():
    clear_screen()
    begin_time = datetime.date.today() - datetime.timedelta(days=7)
    end_time = datetime.date.today()
    window.text(headerframe, "Statistics", fontsize=40)
    window.button(headerframe, "Back", main_menu, anchor=window.NW)

    dateframe = window.frame(contentframe)
    window.text(dateframe, "Begin: ", side=window.LEFT)
    begin = window.date_entry(dateframe, side=window.LEFT, month=begin_time.month,
                              day=begin_time.day, year=begin_time.year)
    window.text(dateframe, "End: ", side=window.LEFT)
    end = window.date_entry(dateframe, side=window.LEFT, month=end_time.month,
                            day=end_time.day, year=end_time.year)

    def reprint_statistics(): return print_statistics(
        gridframe, begin.get_date(), end.get_date())
    window.button(dateframe, "Update Dates", reprint_statistics, side=window.LEFT)
    gridframe = window.frame(contentframe)

    print_statistics(gridframe, begin_time, end_time)


def print_statistics(frame: window.tk.Frame, begin: datetime.date, end: datetime.date):
    stats = calculate_statistics(begin, end)
    for widget in frame.winfo_children():
        window.destroy_widget(widget)
    window.text(frame, "ID",
                grid=True, gridx=0, gridy=0, padx=10)
    window.text(frame, "NAME",
                grid=True, gridx=1, gridy=0, padx=10)
    window.text(frame, "NUMBER OF PASSES",
                grid=True, gridx=2, gridy=0, padx=10)
    id_length = max(len(str(student[0])) for student in stats)
    for i, student in enumerate(stats):
        window.text(frame, str(student[0]).zfill(id_length),
                    grid=True, gridx=0, gridy=i + 1, padx=10)
        window.text(frame, student[1],
                    grid=True, gridx=1, gridy=i + 1, padx=10)
        window.text(frame, student[2],
                    grid=True, gridx=2, gridy=i + 1, padx=10)
    window.button(contentframe, "Export to CSV file", lambda: export_statistics(stats), side=window.LEFT)


def calculate_statistics(begin: datetime.date, end: datetime.date) -> List[Tuple[int, str, int]]:
    begin_td = datetime.datetime.combine(begin, datetime.time.min) - \
        datetime.datetime(1970, 1, 1)
    end_td = datetime.datetime.combine(end, datetime.time.max) - \
         datetime.datetime(1970, 1, 1)
    students = [(student[0], student[1], len(database.query(conn, QUERY_RECORDS_STUDENT, student[0], begin_td.total_seconds(), end_td.total_seconds())))
                for student in database.query(conn, QUERY_STUDENT_ALL)]
    students.sort(key=lambda s: s[2], reverse=True)
    return students


def export_statistics(stats: List[Tuple[int, str, int]]):
    fname = window.file_save_dialog([("Comma Separated Value Files", "*.csv")], "statistics.csv")
    if fname == '':
        return
    f = open(fname, 'w')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["ID", "Name", "Number of Passes"])
    csv_writer.writerows(stats)
    f.close()

def upload_student_list():
    fname = window.file_open_dialog([("Comma Separated Value Files", "*.csv")])
    if fname == '':
        return
    f = open(fname)
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


def reset_password():
    clear_screen()
    window.text(headerframe, "Reset Password", fontsize=40)

    formframe = window.frame(contentframe)

    gridy = 0
    if not password.isempty():
        window.button(headerframe, "Back", setup_program, anchor=window.NW)
        window.text(formframe, "Old Password:",
                    grid=True, gridx=0, gridy=0)
        window.entry(formframe, reset_password.old, password=True,
                     grid=True, gridx=1, gridy=0)
        gridy = 1
    window.text(formframe, "New Password:",
                grid=True, gridx=0, gridy=gridy)
    window.entry(formframe, reset_password.new, password=True,
                 grid=True, gridx=1, gridy=gridy)
    window.text(formframe, "Confirm Password:",
                grid=True, gridx=0, gridy=gridy + 1)
    window.entry(formframe, reset_password.confirm, password=True,
                 grid=True, gridx=1, gridy=gridy + 1)
    window.button(contentframe, "Submit", reset_password_submit)


reset_password.old = window.StringVar()
reset_password.new = window.StringVar()
reset_password.confirm = window.StringVar()


def reset_password_submit():
    old: str = reset_password.old.get()
    new: str = reset_password.new.get()
    confirm: str = reset_password.confirm.get()
    first_set = password.isempty()
    if not first_set and old == '':
        window.error_dialog("Blank Field", "Old Password field is blank.")
    elif new == '':
        window.error_dialog("Blank Field", "New Password field is blank.")
    elif confirm == '':
        window.error_dialog("Blank Field", "Confirm Password field is blank.")
    elif new != confirm:
        window.error_dialog("Passwords Don't Match",
                            "Confirm Password field does not match New Password field.")
    elif not first_set and not password.verify(old):
        window.error_dialog("Incorrect Password", "Old Password is incorrect.")
    else:
        password.write(new)
        if first_set:
            main_menu()
        else:
            window.info_dialog("Password Changed",
                               "Password has been changed successfully.")
            setup_program()


def check_password(if_successful: Callable[[], Any]):
    valid_pwd = False
    entry = window.input_dialog(
        "Enter Password", "Please enter your password to continue this operation.", True)
    if entry is None:
        return
    if password.verify(entry):
        valid_pwd = True
    while not valid_pwd:
        entry = window.input_dialog(
            "Incorrect Password", "You entered an incorrect password. Please try again.", True)
        if entry is None:
            return
        valid_pwd = password.verify(entry)
    if_successful()


def upload_picture():
    fname = window.file_open_dialog([("Image Files", "*.jpg *.jpeg *.png *.gif")])
    if fname == '':
        return
    global img
    img = Image.open(fname)
    for file in glob.glob(STORAGE_LOCATION + "printimage.*"):
        os.remove(file)
    img.save(STORAGE_LOCATION + "printimage" + os.path.splitext(fname)[1])


try:
    password.load()
    main_menu()
except:
    reset_password()

window.loop_window(root)
