# Web-Based Tracker

A task and project management tracker with recurring task logic, PDF report downloads, and calendar UI.

---

## ✅ Local Wi-Fi Deployment

1. Install Python and pip
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run locally:
   ```bash
   python app.py
   ```
4. Access from other devices:
   ```
   http://<your-local-IP>:5000
   ```

---

## 🚀 Deploy to Render.com

1. Push code to GitHub
2. Create a Web Service on Render
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `gunicorn app:app`
5. Add Env Variables:
   - `DATABASE_URL=sqlite:///tracker.db`
   - `SECRET_KEY=your-secret-key`

---

## ✨ Features

- Role-based login
- Daily/Weekly recurring tasks
- Task calendar (Evo)
- PDF reports
- SQLite (upgradeable to PostgreSQL)
