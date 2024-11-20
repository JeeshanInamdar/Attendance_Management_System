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
lbl_branch = Label(left_frame, text="Branch", font=("goudy old style", 12))
lbl_branch.place(x=10, y=20)

branch_var = StringVar()
cmb_branch = ttk.Combobox(left_frame, textvariable=branch_var, font=("goudy old style", 10),
                          values=["CSE", "ISE", "EC", "EE", "CIVIL", "MECH", "AERO"], state="readonly")
cmb_branch.place(x=150, y=20, width=200)

lbl_course = Label(left_frame, text="Course", font=("goudy old style", 12))
lbl_course.place(x=10, y=60)

course_var = StringVar()
cmb_course = ttk.Combobox(left_frame, textvariable=course_var, font=("goudy old style", 10),
                          values=["BE"], state="readonly")
cmb_course.place(x=150, y=60, width=200)

lbl_semester = Label(left_frame, text="Semester", font=("goudy old style", 12))
lbl_semester.place(x=10, y=100)

semester_var = StringVar()
cmb_semester = ttk.Combobox(left_frame, textvariable=semester_var, font=("goudy old style", 10),
                            values=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"], state="readonly")
cmb_semester.place(x=150, y=100, width=200)

lbl_name = Label(left_frame, text="Name", font=("goudy old style", 12))
lbl_name.place(x=10, y=140)

name_var = StringVar()
txt_name = Entry(left_frame, textvariable=name_var, font=("goudy old style", 10))
txt_name.place(x=150, y=140, width=200)

lbl_usn = Label(left_frame, text="USN", font=("goudy old style", 12))
lbl_usn.place(x=10, y=180)

usn_var = StringVar()
txt_usn = Entry(left_frame, textvariable=usn_var, font=("goudy old style", 10))
txt_usn.place(x=150, y=180, width=200)

lbl_gender = Label(left_frame, text="Gender", font=("goudy old style", 12))
lbl_gender.place(x=10, y=220)

gender_var = StringVar()
cmb_gender = ttk.Combobox(left_frame, textvariable=gender_var, font=("goudy old style", 10),
                          values=["Male", "Female", "Other"], state="readonly")
cmb_gender.place(x=150, y=220, width=200)

lbl_dob = Label(left_frame, text="DOB", font=("goudy old style", 12))
lbl_dob.place(x=10, y=260)

dob_var = StringVar()
txt_dob = DateEntry(left_frame, textvariable=dob_var, font=("goudy old style", 10),
                    date_pattern="yyyy-mm-dd")
txt_dob.place(x=150, y=260, width=200)

lbl_email = Label(left_frame, text="Email", font=("goudy old style", 12))
lbl_email.place(x=10, y=300)

email_var = StringVar()
txt_email = Entry(left_frame, textvariable=email_var, font=("goudy old style", 10))
txt_email.place(x=150, y=300, width=200)

lbl_phone = Label(left_frame, text="Phone", font=("goudy old style", 12))
lbl_phone.place(x=10, y=340)

phone_var = StringVar()
txt_phone = Entry(left_frame, textvariable=phone_var, font=("goudy old style", 10))
txt_phone.place(x=150, y=340, width=200)

# Buttons
btn_save = Button(left_frame, text="SAVE", command=save_data, font=("goudy old style", 10, "bold"),
                  bg="green", fg="white", cursor="hand2")
btn_save.place(x=10, y=400, width=100, height=30)

btn_update = Button(left_frame, text="UPDATE", command=update_data, font=("goudy old style", 10, "bold"),
                    bg="blue", fg="white", cursor="hand2")
btn_update.place(x=120, y=400, width=100, height=30)

btn_delete = Button(left_frame, text="DELETE", command=delete_data, font=("goudy old style", 10, "bold"),
                    bg="red", fg="white", cursor="hand2")
btn_delete.place(x=230, y=400, width=100, height=30)

btn_reset = Button(left_frame, text="RESET", command=clear_fields, font=("goudy old style", 10, "bold"),
                   bg="orange", fg="white", cursor="hand2")
btn_reset.place(x=340, y=400, width=100, height=30)

btn_add_photo = Button(left_frame, text="ADD PHOTO", font=("goudy old style", 10, "bold"), cursor="hand2")
btn_add_photo.place(x=10, y=450, width=100, height=30)

btn_update_photo = Button(left_frame, text="UPDATE PHOTO", font=("goudy old style", 10, "bold"), cursor="hand2")
btn_update_photo.place(x=120, y=450, width=130, height=30)

# Right Frame Widgets
lbl_search_by = Label(right_frame, text="Search By", font=("goudy old style", 12))
lbl_search_by.place(x=10, y=20)

search_var = StringVar()
cmb_search = ttk.Combobox(right_frame, textvariable=search_var, font=("goudy old style", 10),
                          values=["branch", "course", "semester", "name", "usn", "gender", "email", "phone"], state="readonly")
cmb_search.place(x=100, y=20, width=150)

search_entry = Entry(right_frame, font=("goudy old style", 10))
search_entry.place(x=270, y=20, width=200)

btn_search = Button(right_frame, text="Search", command=search_data, font=("goudy old style", 10, "bold"),
                    bg="#4caf50", cursor="hand2")
btn_search.place(x=480, y=15, width=100, height=30)

btn_show_all = Button(right_frame, text="Show All", command=show_all, font=("goudy old style", 10, "bold"),
                      bg="#4caf50", cursor="hand2")
btn_show_all.place(x=590, y=15, width=100, height=30)

# Treeview (Table)
tree = ttk.Treeview(right_frame, columns=("ID", "Branch", "Course", "Semester", "Name", "USN", "Gender", "DOB", "Email", "Phone"),
                    show="headings", height=15)
tree.place(x=10, y=70, width=640, height=500)

# Scrollbar
scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=tree.yview)
scrollbar.place(x=650, y=70, height=500)
tree.configure(yscrollcommand=scrollbar.set)


# Configure grid weights for proper resizing
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(4, weight=1)

# Bind Row Select Event
tree.bind("<ButtonRelease-1>", on_row_select)

root.mainloop()
