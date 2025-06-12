# 🏆 Nova Judge – Docker-Powered Django Online Judge

[Live Demo 🔗](https://novajudge.onrender.com) • [Source Code 📂](https://github.com/Shraddhabera/Dev_project)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![License](https://img.shields.io/github/license/<your-github-user>/Nova_Judge)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)

> **Nova Judge** is a lightweight, fully-containerised online code-evaluation platform built with **Django**, **PostgreSQL**, and **Docker**.  
> It supports multiple languages, on-demand AI code reviews (OpenAI), per-problem JSON test-cases, rich user profiles, leaderboards, and AWS-friendly deployment.


---

## 🛠 Features

- ✅ User registration & authentication  
- 📋 Problem list with filters by difficulty  
- 📝 Problem detail pages with descriptions and sample I/O  
- 🧪 User code submissions with verdict display  
- 🏆 Leaderboard based on solved problems  
- 👤 User profile with picks for easy/medium/hard problems solved  
- 🌐 Custom admin area for adding problems & test cases  
- 🐳 Dockerized for consistent environments & easy deployment to Render

## 📸 Screenshots

### 📂 Problem List  
![Problem List](/Screenshots/Screenshot%202025-06-12%20191335.png)

### 🧠 Problem Detail View  
![Problem Detail](/Screenshots/Screenshot%202025-06-12%20191355.png)

### 📄 Submission History  
![Submission Page](/Screenshots/Screenshot%202025-06-12%20191507.png)

---

## 🎥 Demo Video

Watch the full walkthrough here:  
▶️ [Loom Video - NovaJudge Demo](https://www.loom.com/share/41b4872052054b82bc8510589864f3ec?sid=3b3f3181-7ad8-41d6-8dbe-d6cb8cdf0585)

Got it! Here's your fixed README section in plain copy-pasteable format (no special box formatting):

---

## 📦 Project Structure

```
Dev_project/
├── accounts/             # Custom user model, auth views  
├── problems/             # Problem models, views, test-case logic  
├── templates/            # HTML templates  
├── static/               # Static assets (CSS, images, JS)  
├── create_superuser.py   # Script to auto-create admin on deploy  
├── Dockerfile            # Docker image configuration  
├── requirements.txt      # Python dependencies  
└── manage.py
```

---

## 🚀 Getting Started

**1. Install dependencies**

```
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt
```

**2. Configure environment variables**
Create a `.env` file or export them manually:

```
OPENAI_API_KEY=<your_api_key>  
DATABASE_URL=sqlite:///db.sqlite3
```

**3. Run migrations**

```
python manage.py migrate
```

**4. Run the server**

```
python manage.py runserver
```

---

## 🧩 Tech Stack

* **Backend**: Python, Django
* **Frontend**: HTML, Bootstrap
* **Static Files**: WhiteNoise
* **Containerization**: Docker
* **Deployment**: Render
* **Database**: SQLite (local), PostgreSQL (Render)

---

## 👤 Maintainer

**Shraddha Bera**
GitHub: [@Shraddhabera](https://github.com/Shraddhabera)
Live App: [https://novajudge.onrender.com](https://novajudge.onrender.com)

---



🎯 Challenges & Learnings
1. First full-stack project—learned Django from scratch
2. Dockerized deployment and CI-friendly setup
3. Built a judge engine with test-case evaluation
4. Developed leaderboards, profiles, and admin UI
5. Learned how to collect static files and deploy correctly

📜 License
This project is licensed under the MIT License. See LICENSE for details.




