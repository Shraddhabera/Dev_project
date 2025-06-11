# 🏆 Nova Judge – Docker-Powered Django Online Judge

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![License](https://img.shields.io/github/license/<your-github-user>/Nova_Judge)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)

> **Nova Judge** is a lightweight, fully-containerised online code-evaluation platform built with **Django**, **PostgreSQL**, and **Docker**.  
> It supports multiple languages, on-demand AI code reviews (OpenAI), per-problem JSON test-cases, rich user profiles, leaderboards, and AWS-friendly deployment.

---

## ✨ Features

| Category | Highlights |
| -------- | ---------- |
| **Core Judge** | • Secure sand-boxed execution (Python & C++)<br>• Per-test-case verdicts<br>• Time / memory limits |
| **AI Review** | • One-click, on-demand feedback via **GPT-4o**<br>• Actionable suggestions only when the user requests |
| **User Experience** | • Submission history & verdict breakdown<br>• Profile page with solved counts by difficulty<br>• Global leaderboard |
| **Admin** | • JSON-based test-case authoring (`problem_testcases/problem_<id>.json`)<br>• Django Admin for problems & users |
| **Dev Ops** | • Single-command local start-up with `docker-compose`<br>• AWS EC2/RDS deployment guide<br>• CI-ready Docker images |

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone & cd
git clone https://github.com/<your-github-user>/Nova_Judge.git
cd Nova_Judge/onlinejudge

# 2. Configure environment variables
cp .env.example .env               # edit values as needed

# 3. Build & run
docker-compose up --build -d

# 4. Initialise DB
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
