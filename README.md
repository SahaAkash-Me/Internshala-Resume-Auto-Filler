# 🤖 Internshala Resume Auto-Filler

An automation script built with **Python + Playwright** that automatically fills your [Internshala](https://internshala.com) resume — saving hours of manual data entry.

---

## ✨ What It Does

| Section | Status |
|---|---|
| Career Objective | ✅ Auto-filled |
| Work Experience (Amazon + Wipro) | ✅ Auto-filled with bullet points |
| Academic Projects | ✅ Auto-filled |
| Skills | ✅ Auto-added via dropdown |
| Accomplishments | ✅ Auto-filled |
| GitHub Portfolio | ✅ Heading + Description added |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Playwright** — browser automation
- **Chromium** — headless/headed browser

---

## ⚙️ Setup & Installation

**Step 1 — Install dependencies:**
```bash
pip install playwright
playwright install chromium
```

**Step 2 — Add your credentials:**

Open `internshala_resume_filler.py` and update:
```python
EMAIL    = "your_email@gmail.com"
PASSWORD = "your_password"
```

**Step 3 — Run the script:**
```bash
python internshala_resume_filler.py
```

---

## 🚀 How It Works

1. Opens a **real Chromium browser** window (so you can watch it work)
2. Logs into your Internshala account
3. **Pauses** for any CAPTCHA or OTP — you solve it manually, then press Enter
4. Navigates to your resume page
5. Fills each section one by one automatically
6. Clicks **Save / Update** after each section

---

## 📁 Project Structure

```
internshala-resume-filler/
│
├── internshala_resume_filler.py   # Main automation script
└── README.md                      # This file
```

---

## ⚠️ Important Notes

- **Never share** your credentials publicly — keep your password private
- Internshala may update their page layout over time — selectors may need updating if the site changes
- Script runs in **headed mode** (visible browser) so you can monitor progress

---

## 👤 Author

**Akash Saha**
- 📧 sahaakash6@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/akash-saha-b54310382)
- 🐙 [GitHub](https://github.com/SahaAkash-Me)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).


Completion : docs/Completion_Update.png
