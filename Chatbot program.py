from tkinter import *
import time
import tkinter.messagebox
import mysql.connector
from tabulate import tabulate
from tkinter.filedialog import asksaveasfile
import random
import mysql.connector

def chat(user_response):
    user_response=user_response.lower()
    user_response=user_response.strip(""" \n\r\t!@#$%^&*():'";<?>,./~` -_""")
    t=user_response.split()
    if user_response == 'clear':
        ob = "clear"
        return ob
    elif user_response == 'modules':
        ob= "modules"
        return ob
    else:
        try:
           for i in t:
                cursor.execute("""select question from avap;""")
                ans=cursor.fetchall()
                cursor.execute("""select answer from avap where question like %s ;""", (i.lower(),))
                ans = cursor.fetchall()
                if ans:
                    ansindex = random.randint(0, len(ans) - 1)
                    ob = ans[ansindex][0]
                    return ob
                    break
                else:
                    ob = "I am Sorry!! I don't understand you"
                    return ob
                    continue
                
        except Exception as e:
            ob = "I am Sorry!! I don't understand you"
            return ob
conn = mysql.connector.connect(host="localhost", user="root", password="123456", db="chatbot")
cursor = conn.cursor()

window_size="650x650"
root = tkinter.Tk()
# set the geometry, title and icon of the root window
root.geometry(window_size)
root.title("MIA")
root.iconbitmap('i.ico')
# hide the root window until the user clicks the start button
root.withdraw()


opening_page = tkinter.Toplevel(root)
opening_page.title("Login to MIA")
opening_page.iconbitmap('i.ico')
opening_page.geometry("350x200")

# Creating the labels and entries for username and password
tkinter.Label(opening_page, text="Username:").place(x=50, y=50)
username = tkinter.Entry(opening_page)
username.place(x=150, y=50)

tkinter.Label(opening_page, text="Password:").place(x=50, y=80)
password = tkinter.Entry(opening_page, show="*")
password.place(x=150, y=80)

# Defining the function to check the user credentials
def login(user, pwd):
    # Connecting to the database
    db = mysql.connector.connect(host="localhost", user="root", password="123456", database="chatbot")
    cursor = db.cursor()

    # Querying the database to find the user
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (user,))
    result = cursor.fetchone()

    # Checking if the user exists and returning a boolean value
    if result:
        # User exists
        # Querying the database to verify the password
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user, pwd))
        result = cursor.fetchone()
        if result:
            # Password is correct
            return True
        else:
            # Password is incorrect
            return False
    else:
        # User does not exist
        return None

# Defining the function to insert a new user into the database
def insert(user, pwd):
    # Connecting to the database
    db = mysql.connector.connect(host="localhost", user="root", password="123456", database="chatbot")
    cursor = db.cursor()

    # Inserting the user into the database
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (user, pwd))
    db.commit()

# Defining the function to start the chat
def start_chat(event=None):
    # Getting the user input
    user = username.get()
    pwd = password.get()

    # Calling the login function and passing the user input as arguments
    status = login(user, pwd)
    if status == True:
        opening_page.destroy()
        # Show the root window
        root.deiconify()
        # Initialize a ChatInterface object with root
        chat = ChatInterface(root)
    elif status == False:
        # User is invalid
        tkinter.messagebox.showerror("Error", "Invalid username or password!")
    else:
        # User does not exist
        # Creating a new window for password confirmation
        confirm_window = tkinter.Toplevel(opening_page)
        confirm_window.title("Register to Mia")
        confirm_window.geometry("300x200")
        confirm_window.iconbitmap('i.ico')

        # Creating labels and entries for password confirmation
        tkinter.Label(confirm_window, text="Username:").place(x=50, y=50)
        new_username = tkinter.Entry(confirm_window)
        new_username.place(x=150, y=50)

        tkinter.Label(confirm_window, text="Password:").place(x=50, y=80)
        new_password = tkinter.Entry(confirm_window, show="*")
        new_password.place(x=150, y=80)

        # Defining a function to validate and insert the new user
        def confirm(event=None):
            # Getting the user input
            use1 = new_username.get()
            pwd1 = new_password.get()

            # Connecting to the database
            db = mysql.connector.connect(host="localhost", user="root", password="123456", database="chatbot")
            cursor = db.cursor()

            # Inserting the user into the database
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (use1, pwd1))
            db.commit()

            # Displaying a success message
            tkinter.messagebox.showinfo("Success", "You have registered successfully!")
            # Destroying the confirmation window
            confirm_window.destroy()
           
        # Creating a button and binding it to the confirm function
        confirm_btn = tkinter.Button(confirm_window, text="Confirm", command=confirm)
        confirm_btn.place(x=150, y=120)
        confirm_window.bind('<Return>', confirm)


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"
        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)


# Menu bar

    # File
        
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Clear Chat", command=self.clear_chat)      
        file.add_command(label="Exit",command=self.chatexit)
        file.add_command(label="Save Chat", command=self.save_chat)

    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)        

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default",command=self.font_change_default)
        font.add_command(label="Times",command=self.font_change_times)
        font.add_command(label="System",command=self.font_change_system)
        font.add_command(label="Helvetica",command=self.font_change_helvetica)
        font.add_command(label="Fixedsys",command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default",command=self.color_theme_default) 
        color_theme.add_command(label="Night",command=self.color_theme_dark) 
        color_theme.add_command(label="Grey",command=self.color_theme_grey) 
        color_theme.add_command(label="Blue",command=self.color_theme_dark_blue)        
        color_theme.add_command(label="Turquoise",command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker",command=self.color_theme_hacker)       
      
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="About MIA", command=self.msg)
        help_option.add_command(label="Developers", command=self.about)

        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)

        # frame containing send button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        
        self.last_sent_label(date="No messages sent.")
        pr2="Connected to Mia"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr2)
        pr3="\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr3)
        pr4= """Hi! I am Mia, you're chatbot. I am a bot created to teach you about some common python modules, motivate you and also tell you some jokes!!. I am still a learning chatbot and i might not understand some things you ask me. Don't worry I can learn them as soon as you teach me.

        1. Type "modules" to get the list of modules i can tell you about.
        2. Type the name of a module to know more about it.
        3. Apart from this, i could also tell you jokes. Just ask me!"""
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr4)
        pr5="\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr5)
        pr6="\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr6)    
        
    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass
        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)
        
    def save_chat(self):
        files = [('All Files', '*.*'),
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt')] 
        file = asksaveasfile(filetypes = files, defaultextension = files)
        if file is None: 
            return        
        text = self.text_box.get(1.0, END)        
        file.write(text)        
        file.close()        
        
    def chatexit(self):
        exit()
 
    def msg(self):
        tkinter.messagebox.showinfo("MIA v8.0",'MIA is a chatbot for providing you with some simple info on different modules available in python.\nIt is based on data retrival from MYSQL Database.\nGUI is based on tkinter.')

    def about(self):
        tkinter.messagebox.showinfo("MIA Developers","1.Regin Sam Robinson\n2.Dwarkesh\n3.Akshay Balaji\n4.Akhilan Subbiah\n5.Rythwin Singaravel")
    
    def send_message_insert(self, message):        
        user_input = self.entry_field.get()
        user_input=user_input.lower()       
              
        pr1 = "Human : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        ob=chat(user_input)
        
        if ob=='clear':    
            self.text_box.config(state=NORMAL)
            self.last_sent_label(date="No messages sent.")
            self.text_box.delete(1.0, END)
            self.text_box.delete(1.0, END)
            self.text_box.config(state=DISABLED)
            self.entry_field.delete(0,END)
            time.sleep(0)
                       
        elif ob=='modules':
            cursor.execute("""select modules from pav order by modules;""")
            rows = cursor.fetchall()
            c=0
            pr="MIA:"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            pr="\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            
            for i in rows:
                ob=i
                c+=1
                pr=c,'.',str(ob).strip("')(,")
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                pr="\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                
            pr="\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            self.text_box.configure(state=DISABLED)
            self.text_box.see(END)
            self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
            self.entry_field.delete(0,END)
            time.sleep(0)
        else:
            
            pr="MIA : " + str(ob) + "\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            pr="\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            self.text_box.configure(state=DISABLED)
            self.text_box.see(END)
            self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
            self.entry_field.delete(0,END)
            time.sleep(0)        
        
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")
        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")
        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="#444444", fg="#ffffff")
        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"

    # Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")
        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF" 
    

    # Torque
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")
        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")
        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"    

login_btn = tkinter.Button(opening_page, text="Login", command=start_chat)
register_btn = tkinter.Button(opening_page, text="Register", command=start_chat)
title = tkinter.Label(opening_page, text="Welcome to MIA Chatbot",font=("Arial", 12))
# Placing the label at the center of the top
title.place(x=150, y=25, anchor="center")
login_btn.place(x=150, y=120)
register_btn.place(x=200,y=120)
opening_page.bind('<Return>', start_chat)
# Hiding the root window until login is successful
root.withdraw()
# start the GUI
root.mainloop()    
        

