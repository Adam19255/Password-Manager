from tkinter import *
from tkinter import messagebox  # this is not a class, so it wasn't imported by the '*' from before
from random import choice, randint, shuffle
import pyperclip
import json

FONT_NAME = "Clearface"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)  # joining all the elements in the list to one list
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Opps", message="Please don't leave any fields empty!")

    else:
        try:
            with open("Saved Passwords.json", "r") as data_file:
                # json.dump(new_data, data_file, indent=4)
                data = json.load(data_file)  # Reading old data
        except FileNotFoundError:
            with open("Saved Passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)  # Updating old data with new data

            with open("Saved Passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)  # Saving updated data
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("Saved Passwords.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data File wasn't Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(90, 90, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", font=(FONT_NAME, 12, "bold"))
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", font=(FONT_NAME, 12, "bold"))
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=(FONT_NAME, 12, "bold"))
password_label.grid(column=0, row=3)

website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()  # this will make the cursor appear in the entry once we enter the program

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "adam19255@gmail.com")  # making it so that the email will be already filled

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, columnspan=2, row=4)

window.mainloop()
