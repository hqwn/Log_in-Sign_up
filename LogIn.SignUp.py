# Project Made By Aryan Jain, Used Google So Some Code Might Not be 100% 
# Made By Me
# Hope You like It
import sqlite3
import customtkinter
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkTextbox
import sys
import bcrypt
import re
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import time
import random
from icecream import ic 
from customtkinter import filedialog
from PIL import Image

#validates the password
def validate_password(password):
    if len(password) < 8:
        return False, CTkMessagebox(title="Insecure Password", message="Please Include at least 8 Letters")
    if not re.search(r"[a-z]", password):
        return False, CTkMessagebox(title="Insecure Password", message="Please Include a lowercase Letter")
    if not re.search(r"[A-Z]", password):
        return False, CTkMessagebox(title="Insecure Password", message="Please Include a Capital Letter")
    if not re.search(r"[0-9]", password):
        return False, CTkMessagebox(title="Insecure Password", message="Please Include a Digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
         return False, CTkMessagebox(title="Insecure Password", message="Please Include a Special Charachter")
    return True, "Password is valid."

#sets up email sending protocol
load_dotenv()
servers = "smtp.gmail.com"
port = 587
G_ADDRESS = os.getenv("EMAIL_ADDRESS")
G_PASSWORD = os.getenv("EMAIL_PASSWORD")

#sends email
def send_email(email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = G_ADDRESS
        msg["To"] = email
        msg["subject"] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(servers, port) as server:
            server.starttls()
            server.login(G_ADDRESS, G_PASSWORD)
            server.sendmail(G_ADDRESS, email, msg.as_string())
    except Exception as e:
        ic(f"{e}")
#makes a code    
def code():
    a = random.randint(10000,99999)
    return a

#salt for hashing
salt = bcrypt.gensalt()

#connection/setup
connection = sqlite3.connect("passwod.db")
cursor = connection.cursor()

#creates table
cursor.execute("CREATE TABLE IF NOT EXISTS user_data (name TEXT PRIMARY KEY, password TEXT, info TEXT, gmail TEXT, pic TEXT)")
connection.commit()

#shows database for verification if I need It
def show_database():

    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()

    for row in rows:
        ic(row)
#Log In code
def log_in():

    def Password_Sucessfull():

        def image_click():
            path = filedialog.askopenfilename()
            cursor.execute("UPDATE user_data SET pic = (?) WHERE name = (?)", (path, content,))
            connection.commit()
            profile = customtkinter.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(50,50))
            labels.configure(image=profile)

        #destroying old widggts
        def submits():
            messages = []

            # If updating info
            if edit.get("1.0", "end-1c").strip():
                cursor.execute("UPDATE user_data SET info = ? WHERE name = ?", (edit.get("1.0", "end"), content,))
                connection.commit()
                messages.append(f"✔ Info updated to: {edit.get('1.0', 'end').strip()}")

            # If retrieving info
            if c3.get() == 1:
                cursor.execute("SELECT info FROM user_data WHERE name = ?", (content,))
                l = cursor.fetchone()
                messages.append(f"✔ Retrieved info: {l[0]}")

            # If deleting user
            if c1.get() == 1:
                cursor.execute("DELETE FROM user_data WHERE name = ?", (content,))
                connection.commit()
                messages.append("✔ User successfully deleted from storage.")

            # Show all messages in one messagebox
            if messages:
                CTkMessagebox(
                    title="Success!",
                    message=f"User {content.capitalize()}:\n\n" + "\n".join(messages),
                    icon="check"
                ).show()
                app.after(200, lambda: (app.destroy(), sys.exit()))



        content = text.get()
        submit.destroy()
        label.destroy()
        label2.destroy()
        text.destroy()
        text2.destroy()
        app.geometry("600x600")
        cursor.execute("select pic from user_data where name = (?)", (content,))

        d = cursor.fetchone()
        print(d)
        if d and d != ('',):
            path = d[0]
        else:
            path = 'C:/aryan/python/images.jpg'
        profile = customtkinter.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(50,50))
        hh = customtkinter.CTkButton(bb, text="Submit", command=submits, width=350)
        labels = customtkinter.CTkButton(bb,  image=profile, command=image_click, text='', fg_color="transparent",  hover=False,border_width=0,corner_radius=50 )
        c1 = customtkinter.CTkCheckBox(bb, text="Delete Account")
        c3 = customtkinter.CTkCheckBox(bb, text="Retrieve Info")
        edit = customtkinter.CTkTextbox(bb, width= 300)
        lop = customtkinter.CTkLabel(bb, text=f"Hello, {content}\n what would you like to Do? Type in the box if you want to \nchange Your Info")
        labels.grid(pady=20, padx=0,column=0, row=0)
        edit.grid(pady=10, padx=10, column=1, rowspan=2)
        hh.grid(pady=10, padx=10,  row=4, columnspan=4)
        lop.grid(pady=0, padx=10,column=1, row=0)
        c1.grid(pady=5, padx=10,column=0, row=1)
        c3.grid(pady=5, padx=10,column=0, row=2)

    def Password_Valid(): 
        def p(dds, hg, om, op):
            #if time.monotonic() < om:
                #ic(time.monotonic(), om)
                if hg is not None:
                    if hg:   
                            if  hg == dds:
                                Password_Sucessfull()
                            else:
                                if op <= 3:
                                    l = customtkinter.CTkInputDialog(title="Wrong Code", text="The code is Wrong please try again")
                                    hig = int(l.get_input())
                                    op += 1
                                    p(dds, hig, om, op)
                                else:
                                    CTkMessagebox(title="To Many Attempts", message="You Have Done Too Many Attempts")
                                    app.after(150, lambda: (app.destroy()))
                                    app.after(150, lambda: (sys.exit()))
                                

                               
                    else:
                        msg = customtkinter.CTkInputDialog(title="Authentication", text= f"Please Enter The Code (Not Empty)")
                        hg = msg.get_input()

                        p(dds, hg,om,op)
            #else:
               # msg = customtkinter.CTkInputDialog(title="Your code expired!", text="Your code expired, do you want another code? type yes for yes")
                #if msg.get_input() == "yes":
                    #Password_Valid()   
        # Deciding if password is valid
        content = text.get()
        contentp = text2.get()
        cursor.execute("select password from user_data where name = (?)", (content,))
        hi = cursor.fetchone()
        hi = hi[0]
        while not bcrypt.checkpw(contentp.encode('utf-8'), hi.encode('utf-8')):
            msg = CTkMessagebox(title="Wrong Password", message = f"Wrong password for User {content.capitalize()}", icon="warning")
            msg.show()
            if contentp == "quit":
                app.after(100, app.destroy())
                app.after(150, sys.exit())
        if bcrypt.checkpw(contentp.encode('utf-8'), hi.encode('utf-8')):           
            l = cursor.execute("SELECT gmail from user_data where name = (?)", (content,))
            l = cursor.fetchone()
            dd = int(code())
            k = f'Your Verification code is {dd}, if you accendentally got this meassage, just ignore/delete it'
            olp = random.randint(1,10)
            if olp == 4 or olp == 5:
                    send_email(l[0], "Your Verification Code", k)
                    msg = customtkinter.CTkInputDialog(title="Authentication", text= f"We sent You a Code on your Gmail Please type the code")
                    hg = msg.get_input()
                    om = time.monotonic() + 10
                    p(int(dd), hg, om, 2)

            else:
                Password_Sucessfull()

    def User_exists():
        #Deciding If User Exists/Empty Values
        content = text.get()
        contentp = text2.get()
        if len(contentp) == 0:
            msg = CTkMessagebox(title="Empty Value", message="Either Your Username, Or Password Is Empty Please Fill It Out", icon="warning")
            msg.show()
        else:
            cursor.execute("select * from user_data where name = ?", (content,))
            row = cursor.fetchone()
            if row:
                Password_Valid()
            else:
                ic(f"No name named '{content.capitalize()}' found! ")
                msg = CTkMessagebox(title="No Name found", message=f"No name named {content.capitalize()} found! ", icon="warning")
                msg.show()            








    label = customtkinter.CTkLabel(bb, text="Enter username")
    label2 = customtkinter.CTkLabel(bb, text="Enter password")
    text = customtkinter.CTkEntry(bb, width=220, placeholder_text="Enter Username")
    text2 = customtkinter.CTkEntry(bb, width=220, placeholder_text="Enter Password", show='*')
    submit = customtkinter.CTkButton(bb, text="Submit", width=180, height=40, command=User_exists)
    label.grid(row=0,column=2,sticky="nsew")
    label2.grid(row=2,column=2,sticky="nsew")
    text.grid(row=1,column=2,padx=20,pady=20,sticky="nsew")
    text2.grid(row=3,column=2,padx=20,pady=20,sticky="nsew")
    submit.grid(row=4, column=2)
    app.geometry("265x280")
    button.destroy()
    button2.destroy()
#Sign Up code
def sign_up():
    def is_valid_gmail(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
        return re.match(pattern, email) is not None
    def Add_Data():
        #Adds data in Database
        a = stext.get()
        b = stext2.get()
        c = stext3.get("1.0", "end").strip()
        d = Gmail.get()
        b = bcrypt.hashpw(password=b.encode('utf-8'), salt=salt).decode('utf-8')
        cursor.execute("insert into user_data values (?,?,?,?,?)", (a,b,c,d,''))
        connection.commit()
        msg = CTkMessagebox(title="Sucessful Registration", message= f"The User Named {a.capitalize()} Is Now Sucessfully Registered For Aryan Handsome's Storage ", icon="check")
        msg.show()
        response = msg.get()
        app.after(100, lambda: (app.destroy()))
        app.after(150, lambda: (sys.exit()))

        
    def Validation():
        #Checking if name is taken?
        a = stext.get()
        b = stext2.get()
        c = stext3.get("1.0", "end").strip()
        d = Gmail.get()
        k,l = validate_password(b)
        cursor.execute("select * from user_data where name = ?", (a,))
        row = cursor.fetchone()
        if not a or not b or not c or not d:
            msg = CTkMessagebox(title="Value/s Empty", message= f" Please fill out all of the values ", icon="warning")
            msg.show()
        else:
            while row:
                msg = CTkMessagebox(title="UserName Taken!", message= f"Name {a.capitalize()} Already Exists Please Try A New One! ", icon="warning")
                msg.show()
            if len(a) < 5:
                CTkMessagebox(title="Username Too Short", message="Please Make Your Username more than 5 charachters")
            else:
                if k:
                    if is_valid_gmail(d):
                        d = Gmail.get()
                        dd = int(code())
                        k = f'Your Verification code is {dd}, if you accendentally got this meassage, just ignore/delete it'
                        send_email(d, "Your Verification Code", k)
                        def jj(osa):
                            if osa == 1:
                                msg = customtkinter.CTkInputDialog(title="Authentication", text= f"We sent You a Code on your Gmail Please type the code")
                            msg = msg
                            hg = msg.get_input()
                            if dd == int(hg):
                                    Add_Data()
                            else:
                                msg = customtkinter.CTkInputDialog(title="Authentication", text= f"Wrong Code! Please type the code")
                                hg = msg.get_input()
                                jj(0)
                        jj(1)
                    else:
                        msg = CTkMessagebox(title="Invalid Gmail", message="Please enter a valid Gmail address (e.g., name@gmail.com)", icon="warning")
                        msg.show()
                else:
                    l
    slabel = customtkinter.CTkLabel(bb, text="Enter New username")
    slabel2 = customtkinter.CTkLabel(bb, text="Enter New password")
    slabel3 = customtkinter.CTkLabel(bb, text="Enter Info you Would Like To Store")
    Glabel = customtkinter.CTkLabel(bb, text="Enter your gmail")
    Gmail = customtkinter.CTkEntry(bb, width=220,  placeholder_text="Please Enter your Gmail")
    stext = customtkinter.CTkEntry(bb, width=220, placeholder_text="Enter a Username")
    stext2 = customtkinter.CTkEntry(bb, width=220, placeholder_text="Enter a Password", show='*')
    stext3 = customtkinter.CTkTextbox(bb, width=250, height=100)
    ssubmit = customtkinter.CTkButton(bb, text="Submit", width=180, height=40, command=Validation)
    slabel.grid(row=0,column=2,sticky="nsew")
    slabel2.grid(row=2,column=2,sticky="nsew")
    Glabel.grid(row=4,column=2,sticky="nsew")
    slabel3.grid(row=6,column=2,sticky="nsew")
    stext.grid(row=1,column=2,padx=20,pady=20,sticky="nsew")
    stext2.grid(row=3,column=2,padx=20,pady=20,sticky="nsew")
    stext3.grid(row=7,column=2,padx=20,pady=20,sticky="nsew")
    Gmail.grid(row=5,column=2,padx=20,pady=20,sticky="nsew")
    ssubmit.grid(row=8, column=2)
    app.geometry("350x500")
    button.destroy()
    button2.destroy()


#Inital ask for log in or Sign up
app = customtkinter.CTk()
app.title("Sign up/Log in")
app.geometry("165x200")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
bb = customtkinter.CTkFrame(app)
button = customtkinter.CTkButton(bb, text="Sign up", command=sign_up, height=50, width=150)
button2 = customtkinter.CTkButton(bb, text="Log in", command=log_in, height=50, width=150)
button.grid(row=0, column=0, padx=10,pady=20, sticky="nsew")
button2.grid(row=1, column=0,padx=10,pady=20, sticky="nsew")
bb.grid(row=2, column=2, sticky="nsew")
bb.pack(padx=0, pady=0)
#mainloop
app.mainloop()
# You can use this command to look at the database
#show_database()