import json
from tkinter import *
from PIL import Image
from tkinter import messagebox
from random import randint, choice, shuffle

# Declare variable and CONSTANT
IMAGE = "./image/logo.png"
WHITE = "#FFFFFF"
FILE = "./json/password_manager.json"

# Get size of image
open_image = Image.open(IMAGE)
width, height = open_image.size


# function to generate random password
def generate_password():
    password_entry.delete(0, END)

    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
        'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # "for" cycle to found random letter
    letters_password = [choice(letters) for _ in range(randint(1, 10))]
    # "for" cycle to found random numbers
    numbers_password = [choice(numbers) for _ in range(randint(2, 4))]
    # "for" cycle to found random symbols
    symbols_password = [choice(symbols) for _ in range(randint(2, 4))]

    easy_password = letters_password + numbers_password + symbols_password

    # Use shuffle() function to mix list
    shuffle(easy_password)

    password = "".join(easy_password)

    password_entry.insert(0, password)


# Function to reset entry value
def reset_entry(*widgets):
    for i, widget in enumerate(widgets):
        for my_object in widget.keys():
            my_object.delete(0, END)


# Function to save item in json file
def save():
    is_ok = False
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) > 0 and len(password) > 0:
        is_ok = messagebox.askokcancel("Check your input!", f"Website: {website}\nEmail: {email}\nPassword: {password}")
    else:
        messagebox.showinfo("title", "some field is empty!")

    if is_ok:
        try:
            with open(FILE, "r") as file_open:
                data = json.load(file_open)
        except FileNotFoundError:
            with open(FILE, "w") as file_open:
                json.dump(new_data, file_open, indent=4)
        else:
            data.update(new_data)

            with open(FILE, "w") as file_open:
                json.dump(data, file_open, indent=4)
        finally:
            # file_open.write(add_text)
            reset_widget = {website_entry: website, password_entry: password}
            reset_entry(reset_widget)
            website_entry.focus()


# Function to search name in json file
def search_website():
    website_research = website_entry.get()
    try:
        with open(FILE, "r") as file_open:
            data = json.load(file_open)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found!")
    else:
        if website_research in data:
            email = data[website_research]["email"]
            password = data[website_research]["password"]
            messagebox.showinfo(website_research, f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showinfo("Error", f"No details for the {website_research} exist!")


# Create window object
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

# Create Canvas object
image_canvas = Canvas(width=width, height=height, bg=WHITE, highlightthickness=0)
logo_image = PhotoImage(file=IMAGE)
image_canvas.create_image(width // 2, height // 2, image=logo_image)
image_canvas.grid(row=0, column=1)

# Create Label, Entry, Button "website"
website_label = Label(text="Website", bg=WHITE)
website_label.grid(row=1, column=0)
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)
website_search_button = Button(text="Search", width=13, command=search_website)
website_search_button.grid(column=2, row=1)

# Create Label, Entry "email"
email_label = Label(text="Email/Username", bg=WHITE)
email_label.grid(column=0, row=2)
email_entry = Entry(width=42)
email_entry.insert(0, "emilio.reforgiato@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

# Create Label, Entry and Button "password"
password_label = Label(text="Password", bg=WHITE)
password_label.grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

# Create Button "add" to save the item
add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
