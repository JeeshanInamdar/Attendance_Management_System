import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Database setup
conn = sqlite3.connect("attendance_system.db")
cursor = conn.cursor()

# Functionality
def validate_email(email):
    if not email.endswith("@students.git.edu"):
        messagebox.showerror("Error", "Use College email ID")
        return False
    return True

def validate_phone(phone):
    if len(phone) != 10 or not phone.isdigit():
        messagebox.showerror("Error", "Phone number must be 10 digits long")
        return False
    return True

def save_data():
    branch = branch_var.get()
    course = course_var.get()
    semester = semester_var.get()
    name = name_var.get()
    usn = usn_var.get().upper()
    gender = gender_var.get()
    dob = dob_var.get()
    email = email_var.get()
    phone = phone_var.get()

    if not validate_email(email) or not validate_phone(phone):
        return

    if not all([branch, course, semester, name, usn, gender, dob, email, phone]):
        messagebox.showerror("Error", "All fields are required")
        return

    cursor.execute("INSERT INTO students (branch, course, semester, name, usn, gender, dob, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (branch, course, semester, name, usn, gender, dob, email, phone))
    conn.commit()
    messagebox.showinfo("Success", "Student data saved successfully")
    clear_fields()
    load_data()

def update_data():
    branch = branch_var.get()
    course = course_var.get()
    semester = semester_var.get()
    name = name_var.get()
    usn = usn_var.get().upper()
    gender = gender_var.get()
    dob = dob_var.get()
    email = email_var.get()
    phone = phone_var.get()

    if not validate_email(email) or not validate_phone(phone):
        return

    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No record selected to update")
        return

    student_id = tree.item(selected[0], "values")[0]
    cursor.execute("UPDATE students SET branch=?, course=?, semester=?, name=?, usn=?, gender=?, dob=?, email=?, phone=? WHERE id=?",
                   (branch, course, semester, name, usn, gender, dob, email, phone, student_id))
    conn.commit()
    messagebox.showinfo("Success", "Student data updated successfully")
    clear_fields()
    load_data()

def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No record selected to delete")
        return

    student_id = tree.item(selected[0], "values")[0]
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    messagebox.showinfo("Success", "Student data deleted successfully")
    load_data()

def clear_fields():
    branch_var.set("")
    course_var.set("")
    semester_var.set("")
    name_var.set("")
    usn_var.set("")
    gender_var.set("")
    dob_var.set("")
    email_var.set("")
    phone_var.set("")

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", END, values=row)

def search_data():
    option = search_var.get()
    value = search_entry.get()

    if not option or not value:
        messagebox.showerror("Error", "Select a search option and enter a value")
        return

    query = f"SELECT * FROM students WHERE {option} LIKE ?"
    cursor.execute(query, ('%' + value + '%',))
    rows = cursor.fetchall()

    for row in tree.get_children():
        tree.delete(row)

    for row in rows:
        tree.insert("", END, values=row)

def show_all():
    load_data()

def on_row_select(event):
    selected = tree.selection()
    if not selected:
        return

    student_id, branch, course, semester, name, usn, gender, dob, email, phone = tree.item(selected[0], "values")
    branch_var.set(branch)
    course_var.set(course)
    semester_var.set(semester)
    name_var.set(name)
    usn_var.set(usn)
    gender_var.set(gender)
    dob_var.set(dob)
    email_var.set(email)
    phone_var.set(phone)

# GUI Setup
root = Tk()
root.title("Student Data Management")
root.geometry("1200x700")

# Back Button
Button(root, text="Back", command=root.quit, bg="red", fg="white").pack(anchor="ne", padx=10, pady=10)

# Main Label
Label(root, text="Student Data", font=("Arial", 20)).pack(pady=5)

# Frames
left_frame = Frame(root, bd=2, relief=RIDGE)
left_frame.place(x=10, y=80, width=500, height=600)

right_frame = Frame(root, bd=2, relief=RIDGE)
right_frame.place(x=520, y=80, width=670, height=600)

# Left Frame Widgets
Label(left_frame, text="Branch").grid(row=0, column=0, padx=10, pady=5)
branch_var = StringVar()
branch_dropdown = ttk.Combobox(left_frame, textvariable=branch_var, values=["CSE", "ISE", "EC", "EE", "CIVIL", "MECH", "AERO"], state="readonly")
branch_dropdown.grid(row=0, column=1, padx=10, pady=5)

Label(left_frame, text="Course").grid(row=1, column=0, padx=10, pady=5)
course_var = StringVar()
course_dropdown = ttk.Combobox(left_frame, textvariable=course_var, values=["BE"], state="readonly")
course_dropdown.grid(row=1, column=1, padx=10, pady=5)

Label(left_frame, text="Semester").grid(row=2, column=0, padx=10, pady=5)
semester_var = StringVar()
semester_dropdown = ttk.Combobox(left_frame, textvariable=semester_var, values=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"], state="readonly")
semester_dropdown.grid(row=2, column=1, padx=10, pady=5)

Label(left_frame, text="Name").grid(row=3, column=0, padx=10, pady=5)
name_var = StringVar()
name_entry = Entry(left_frame, textvariable=name_var)
name_entry.grid(row=3, column=1, padx=10, pady=5)

Label(left_frame, text="USN").grid(row=4, column=0, padx=10, pady=5)
usn_var = StringVar()
usn_entry = Entry(left_frame, textvariable=usn_var)
usn_entry.grid(row=4, column=1, padx=10, pady=5)

Label(left_frame, text="Gender").grid(row=5, column=0, padx=10, pady=5)
gender_var = StringVar()
gender_dropdown = ttk.Combobox(left_frame, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly")
gender_dropdown.grid(row=5, column=1, padx=10, pady=5)

Label(left_frame, text="DOB").grid(row=6, column=0, padx=10, pady=5)
dob_var = StringVar()
dob_picker = DateEntry(left_frame, textvariable=dob_var, date_pattern="yyyy-mm-dd")
dob_picker.grid(row=6, column=1, padx=10, pady=5)

Label(left_frame, text="Email").grid(row=7, column=0, padx=10, pady=5)
email_var = StringVar()
email_entry = Entry(left_frame, textvariable=email_var)
email_entry.grid(row=7, column=1, padx=10, pady=5)

Label(left_frame, text="Phone").grid(row=8, column=0, padx=10, pady=5)
phone_var = StringVar()
phone_entry = Entry(left_frame, textvariable=phone_var)
phone_entry.grid(row=8, column=1, padx=10, pady=5)

# Buttons
Button(left_frame, text="SAVE", command=save_data, bg="green", fg="white").grid(row=9, column=0, padx=10, pady=10)
Button(left_frame, text="UPDATE", command=update_data, bg="blue", fg="white").grid(row=9, column=1, padx=10, pady=10)
Button(left_frame, text="DELETE", command=delete_data, bg="red", fg="white").grid(row=10, column=0, padx=10, pady=10)
Button(left_frame, text="RESET", command=clear_fields, bg="orange", fg="white").grid(row=10, column=1, padx=10, pady=10)
Button(left_frame, text="ADD PHOTO").grid(row=11, column=0, padx=10, pady=10)
Button(left_frame, text="UPDATE PHOTO").grid(row=11, column=1, padx=10, pady=10)

# Right Frame Widgets
Label(right_frame, text="Search By").grid(row=0, column=0, padx=10, pady=5, sticky="w")
search_var = StringVar()
search_dropdown = ttk.Combobox(right_frame, textvariable=search_var, values=["branch", "course", "semester", "name", "usn", "gender", "email", "phone"], state="readonly")
search_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

search_entry = Entry(right_frame)
search_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")

Button(right_frame, text="Search", command=search_data).grid(row=0, column=3, padx=10, pady=5, sticky="w")
Button(right_frame, text="Show All", command=show_all).grid(row=0, column=4, padx=10, pady=5, sticky="w")

# Treeview (Table)
tree = ttk.Treeview(right_frame, columns=("ID", "Branch", "Course", "Semester", "Name", "USN", "Gender", "DOB", "Email", "Phone"), show="headings")
tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Scrollbar
scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=1, column=5, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

# Configure grid weights for proper resizing
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(4, weight=1)

# Bind Row Select Event
tree.bind("<ButtonRelease-1>", on_row_select)

root.mainloop()
