# 💰 TrackWise

> A lightweight personal expense manager with multi-user support, built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## ✨ Features

- 🔐 **Multi-user system** — each user has their own private data
- 🔑 **Secure login** — passwords hashed with SHA-256
- ➕ **Add expenses** with amount, category, and description
- 🗑 **Delete** one or multiple expenses at once
- 📊 **Monthly reports** — breakdown by category per month
- 🎨 **Modern dark UI** built with Tkinter

---

## 📸 Screenshot

> _Add a screenshot of your app here_

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- No external libraries needed (uses built-in `tkinter` and `json`)

### Run the app

```bash
git clone https://github.com/YOUR_USERNAME/TrackWise.git
cd TrackWise
python expense_manager.py
```

---

## 📁 Project Structure

```
TrackWise/
│
├── expense_manager.py     # Main application
├── users.json             # Stores user credentials (auto-created)
├── expenses_<user>.json   # Per-user expense data (auto-created)
└── README.md
```

---

## 🛠 Built With

- **Python** — core language
- **Tkinter** — GUI framework
- **JSON** — lightweight data storage
- **hashlib** — password security (SHA-256)

---

## 📌 Roadmap

- [ ] Export expenses to CSV
- [ ] Charts and graphs (matplotlib)
- [ ] Budget limit alerts
- [ ] Dark/Light theme toggle

---

## 👤 Author

**Farnam Asgarzadeh**  
High school student | Python developer  
📍 Isfahan, Iran

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
