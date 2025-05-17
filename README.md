# Python chatbot named MIA is built using:

* 🧠 **MySQL** for backend storage
* 🖼️ **Tkinter** for the GUI
* 🗃️ **Structured chat logic**, with word tokenization to understand the user queries and a learning-style interface

---

## 🔍 **Project Overview**

### ✅ **Goal**:

Create an educational chatbot that:

* Responds to user queries about **Python modules**
* Tells **jokes**
* Gives **motivational quotes**
* Supports **user login/registration**
* Allows **theming and customization**

---

## 🧱 Project Components Explained

### 1. **Database (`chatbot` in MySQL)**

#### Tables Used:

* `users`: Stores login credentials (`username`, `password`)
* `avap`: Stores question-answer pairs for freeform questions
* `pav`: Stores module names and descriptions
#### (The Database is attached in the chatbot.sql file)

---

### 2. **Login and Registration**

When the program starts:

* A **login window** appears (via `Tkinter.Toplevel`).
* If the username exists:

  * The password is verified.
* If the username does **not** exist:

  * The user is prompted to **register**.

#### Related Functions:

* `login(user, pwd)` – checks credentials
* `insert(user, pwd)` – registers new user

---

### 3. **Main Chat Window**

After login:

* The main chat UI opens (`ChatInterface` class)
* User can enter queries
* Responses come from the MySQL database based on input

---

### 4. **Chat Logic – `chat(user_response)`**

* Cleans up and normalizes input
* If the input is:

  * `"clear"` → clears the screen
  * `"modules"` → fetches list from `pav` table
  * Anything else → checks for matches in `avap` table

If no match is found:

```python
return "I am Sorry!! I don't understand you"
```

---

### 5. **GUI Features**

* Dynamic **font and theme customization**
* **Menu bar** with:

  * File (Clear Chat, Exit, Save)
  * Options (Fonts, Themes)
  * Help (About, Developers)
* Displays timestamp of the last message sent
* Messages display as:

  ```
  Human: how are you?
  MIA: I am fine
  ```

---

### 6. **Special Commands**

* `"clear"`: Clears chat history
* `"modules"`: Lists Python modules from `pav`
* Module names: Triggers an explanation from `pav`
* General queries: Matched against `avap` using a LIKE query

---

## 🧪 Sample Chat Flow

```
User: hello
MIA: i am fine

User: modules
MIA:
1. array
2. csv
3. tkinter
...

User: tkinter
MIA: Python interface to Tcl/Tk...
```

---

## ✅ Key Strengths

* Fully functional login + chat flow
* Modular question-answer support
* Clean UI with themes and fonts
* Easy to extend (just insert more Q\&A pairs in MySQL)

---

## 📌 Conclusion

This chatbot is a solid educational project combining:

* GUI (Tkinter)
* Database (MySQL)
* Text processing
* Real user interactivity

It’s very extensible and educational. Let me know if you want help packaging it into an installer, improving performance, or deploying it as a web app.
