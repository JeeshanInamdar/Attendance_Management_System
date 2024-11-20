import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import random  # For OTP generation
import smtplib
import re  # For email validation



# SMTP Email Configuration (Replace with your email settings)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "jeeshaninamdar7@gmail.com"
SENDER_PASSWORD = 'kpnj skqq smom cidd'



# Function to hash the password (simple for now; can use bcrypt for better security)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to check if the login credentials are correct
def check_login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not email or not password:
        messagebox.showerror("Error", "Email and Password are required.")
        return

    # Hash the input password and check against the database
    hashed_password = hash_password(password)

    conn = sqlite3.connect("attendance_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teachers WHERE Email = ? AND Password = ?", (email, hashed_password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful!")
        # Redirect to the main page or the next step of your application here
    else:
        messagebox.showerror("Error", "Invalid Email or Password.")

    conn.close()

#forgot password
def forgot_password():
    login_window.withdraw()  # Hide login window
    open_forgot_password_window()

# Function to send email
def send_email(receiver_email, subject, message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(SENDER_EMAIL, receiver_email, email_message)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")


# Forgot Password Window (Modified for OTP process)
def open_forgot_password_window():
    global forgot_password_window, email_entry_fp, otp_entry, otp_verification_button, reset_password_button

    forgot_password_window = tk.Tk()
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("400x400")

    tk.Label(forgot_password_window, text="Forgot Password", font=("Arial", 16, "bold")).pack(pady=10)

    # Email Entry
    tk.Label(forgot_password_window, text="Enter Registered Email").pack(anchor="w", padx=20)
    email_entry_fp = tk.Entry(forgot_password_window, width=30)
    email_entry_fp.pack(pady=5)

    # OTP Entry (Hidden initially)
    tk.Label(forgot_password_window, text="Enter OTP").pack(anchor="w", padx=20)
    otp_entry = tk.Entry(forgot_password_window, width=30)
    otp_entry.pack(pady=5)
    otp_entry.config(state="disabled")

    # Buttons for OTP and Reset Password
    otp_verification_button = tk.Button(forgot_password_window, text="Send OTP", command=send_otp, bg="blue", fg="white")
    otp_verification_button.pack(pady=10)

    reset_password_button = tk.Button(forgot_password_window, text="Reset Password", command=reset_password,bg="green", fg="black")
    reset_password_button.pack(pady=10)
    reset_password_button.config(state="disabled")

    # Back to Login Button
    back_button = tk.Button(forgot_password_window, text="Back to Login",command=lambda: back_to_login(forgot_password_window), bg="gray", fg="white")
    back_button.pack(pady=5)

    forgot_password_window.mainloop()


# Function to send OTP
def send_otp():
    global otp_code
    email = email_entry_fp.get().strip()

    if not email:
        messagebox.showerror("Error", "Email is required.")
        return

    conn = sqlite3.connect("attendance_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teachers WHERE Email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        otp_code = generate_otp()
        try:
            send_email(email, "Password Reset OTP", f"Your OTP for password reset is: {otp_code}")
            messagebox.showinfo("Success", "OTP sent to your registered email.")
            otp_entry.config(state="normal")
            otp_verification_button.config(text="Verify OTP", command=verify_otp)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send OTP: {e}")
    else:
        messagebox.showerror("Error", "Email not registered.")


# Function to verify OTP
def verify_otp():
    entered_otp = otp_entry.get().strip()

    if not entered_otp:
        messagebox.showerror("Error", "Please enter the OTP.")
        return

    if entered_otp == otp_code:
        messagebox.showinfo("Success", "OTP verified. You can now reset your password.")
        reset_password_button.config(state="normal")
        otp_entry.config(state="disabled")
        otp_verification_button.config(state="disabled")
    else:
        messagebox.showerror("Error", "Invalid OTP. Please try again.")

# Function to reset password (after OTP verification)
def reset_password():
    global new_password_entry, confirm_password_entry_fp

    # Hide OTP fields and show password reset fields
    otp_entry.pack_forget()
    otp_verification_button.pack_forget()
    reset_password_button.pack_forget()

    tk.Label(forgot_password_window, text="Enter New Password").pack(anchor="w", padx=20)
    new_password_entry = tk.Entry(forgot_password_window, width=30, show="*")
    new_password_entry.pack(pady=5)

    tk.Label(forgot_password_window, text="Confirm New Password").pack(anchor="w", padx=20)
    confirm_password_entry_fp = tk.Entry(forgot_password_window, width=30, show="*")
    confirm_password_entry_fp.pack(pady=5)

    tk.Button(forgot_password_window, text="Submit", command=submit_new_password, bg="green", fg="white").pack(pady=10)



# Function to reset password (after OTP verification)
def reset_password():
    global new_password_entry, confirm_password_entry_fp

    # Hide OTP fields and show password reset fields
    otp_entry.pack_forget()
    otp_verification_button.pack_forget()
    reset_password_button.pack_forget()

    tk.Label(forgot_password_window, text="Enter New Password").pack(anchor="w", padx=20)
    new_password_entry = tk.Entry(forgot_password_window, width=30, show="*")
    new_password_entry.pack(pady=5)

    tk.Label(forgot_password_window, text="Confirm New Password").pack(anchor="w", padx=20)
    confirm_password_entry_fp = tk.Entry(forgot_password_window, width=30, show="*")
    confirm_password_entry_fp.pack(pady=5)

    tk.Button(forgot_password_window, text="Submit", command=submit_new_password, bg="green", fg="white").pack(pady=10)


# Submit the new password
def submit_new_password():
    email = email_entry_fp.get().strip()
    new_password = new_password_entry.get().strip()
    confirm_password = confirm_password_entry_fp.get().strip()

    if not new_password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    hashed_password = hash_password(new_password)

    conn = sqlite3.connect("attendance_system.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Teachers SET Password = ? WHERE Email = ?", (hashed_password, email))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Password reset successfully!")
    send_email(email, "Password Reset Successful", "Your password has been reset successfully.")
    back_to_login(forgot_password_window)


# Function to open the registration window
def open_registration():
    login_window.withdraw()  # Hide the login window
    create_account_window()  # Open the registration window


# GUI for login page
def create_login_window():
    global email_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Teacher Login")
    login_window.geometry("400x400")

    # Title Label
    tk.Label(login_window, text="Teacher Login", font=("Arial", 16, "bold")).pack(pady=10)

    # Email Entry
    tk.Label(login_window, text="Email").pack(anchor="w", padx=20)
    email_entry = tk.Entry(login_window, width=30)
    email_entry.pack(pady=5)

    # Password Entry
    tk.Label(login_window, text="Password").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    # Login Button
    login_button = tk.Button(login_window, text="Login", command=check_login, bg="blue", fg="white")
    login_button.pack(pady=10)

    tk.Button(login_window, text="Forgot Password", command=forgot_password, bg="orange", fg="white").pack(pady=5)

    # Create Account Button
    create_account_button = tk.Button(login_window, text="Create Account", command=open_registration, bg="green",
                                      fg="white")
    create_account_button.pack(pady=10)

    # Run the login window
    login_window.mainloop()


def create_account_window():
    global name_entry, email_entry_reg, password_entry_reg, confirm_password_entry_reg, registration_window

    registration_window = tk.Tk()
    registration_window.title("Teacher Registration")
    registration_window.geometry("400x400")

    # Title Label
    tk.Label(registration_window, text="Teacher Registration", font=("Arial", 16, "bold")).pack(pady=10)

    # Name Entry
    tk.Label(registration_window, text="Name").pack(anchor="w", padx=20)
    name_entry = tk.Entry(registration_window, width=30)
    name_entry.pack(pady=5)

    # Email Entry
    tk.Label(registration_window, text="Email").pack(anchor="w", padx=20)
    email_entry_reg = tk.Entry(registration_window, width=30)
    email_entry_reg.pack(pady=5)

    # Password Entry
    tk.Label(registration_window, text="Password").pack(anchor="w", padx=20)
    password_entry_reg = tk.Entry(registration_window, width=30, show="*")
    password_entry_reg.pack(pady=5)

    # Confirm Password Entry
    tk.Label(registration_window, text="Confirm Password").pack(anchor="w", padx=20)
    confirm_password_entry_reg = tk.Entry(registration_window, width=30, show="*")
    confirm_password_entry_reg.pack(pady=5)

    # Register Button
    register_button = tk.Button(registration_window, text="Register", command=register_teacher, bg="green", fg="white")
    register_button.pack(pady=20)

    # Back to Login Button
    back_to_login_button = tk.Button(registration_window, text="Back to Login",command=lambda: back_to_login(registration_window), bg="gray",fg="white")
    back_to_login_button.pack(pady=5)

    # Run the registration window
    registration_window.mainloop()
# Registration window


# Function to handle registration
def register_teacher():
    name = name_entry.get().strip()
    email = email_entry_reg.get().strip()
    password = password_entry_reg.get().strip()
    confirm_password = confirm_password_entry_reg.get().strip()

    # Regex for validating email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not name or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return

    # Check if email format is valid
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    # Hash the password
    hashed_password = hash_password(password)

    # Insert into the database
    try:
        conn = sqlite3.connect("attendance_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Teachers (Name, Email, Password) VALUES (?, ?, ?)",
                       (name, email, hashed_password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
        registration_window.withdraw()  # Close registration window
        login_window.deiconify()  # Show login window again
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists. Please use a different email.")


# Function to go back to the login window
def back_to_login(window_to_close):
    window_to_close.withdraw()  # Hides the current window (passed as a parameter)
    login_window.deiconify()  # Brings back the login window


if __name__=='__main__':
# Start the login page
    create_login_window()