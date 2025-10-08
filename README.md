# Reddit Clone

A web application simulating Reddit-like functionality — posting, commenting, and voting — built with **Python** and **Flask**.

---

## 🧾 Overview

This project is a simplified **Reddit Clone** where users can:

- 📝 Create and view posts
- 💬 Comment on posts
- 👍 / 👎 Upvote and downvote posts or comments
- 🧭 Browse posts by popularity or recency
- 🔐 Login and manage user accounts

This project demonstrates **Flask routing**, **templating**, and **ORM**-based data handling with **MongoDB**— ideal for learning backend web development in Python.

---

## 📂 Repository Structure

```
Reddit_Clone/
├── app.py
├── models.py
├── routes/
│   ├── auth.py
│   ├── post.py
│   └── comment.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── post_detail.html
│   └── create_post.html
└── requirements.txt
```

**File Descriptions**
| File / Folder | Purpose |
|----------------|----------|
| `app.py` | Application entry point |
| `models.py` | Database models (ORM) |
| `routes/` | Flask blueprints for different modules |
| `templates/` | Jinja2 HTML templates |
| `static/` | CSS, JS, and image files |
| `requirements.txt` | Python dependencies |

---

## 🛠 Features

- 🔐 User authentication (Signup, Login, Logout)
- 📝 Post creation and deletion
- 💬 Commenting system
- 👍 / 👎 Voting on posts and comments
- 🧭 Sorting posts by “Top” and “New”
- 🎨 Responsive frontend with Jinja2 templates

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/JayantLodhi/Reddit_Clone.git
cd Reddit_Clone
```

### 2️⃣ Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Run the app
```bash
flask run
```

Visit **http://localhost:5000** in your browser.

---

## 🧠 Implementation Highlights

- **Flask Blueprints** — Modular route management  
- **MongoDB ORM** — For database modeling and relationships  
- **Jinja2 Templates** — For rendering dynamic HTML  
- **Session-based Authentication** — With secure login system  

---

## 🧭 Future Improvements

- 🌐 Add user profiles and activity history  
- 🖼 Support image uploads  
- 🧮 Real-time vote updates with AJAX or WebSocket  
- 🧩 Add moderation tools (delete, report) 

---

## 👩‍💻 Contributor

| Name | Role |
|------|------|
| **Jayant Lodhi** | Developer, Designer, Documentation |

---

## 📜 Aknowledgements

this project was developed as the part of coursework / term project.

---

> *Generated README for the Reddit_Clone Flask project. You can update section details or add screenshots before uploading to GitHub.*
