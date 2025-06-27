# 👨‍👩‍👧‍👦 FamilyConnect - A Private Social Network for Families

![FamilyConnect Banner](https://placehold.co/1200x400/3b82f6/ffffff?text=FamilyConnect+-+Private+Social+Media+for+Families)

**FamilyConnect** is a Django-powered platform built to bring families closer by enabling private group communication, event sharing, document uploads, and secure group management. It's not just a social network—it's a digital family space. ❤️

---

## ✨ Key Features

### 🏠 Family Groups
- Create or join family groups using a unique **Group ID**
- Admin approval required for new member requests
- Family-based content sharing and visibility

### 📬 Membership System
- Secure join requests with admin-only approvals
- Member roles: **Admin**, **Member**
- Notifications for membership actions

### 📸 Posts & Memories
- Share **public**, **private**, or **group-only** posts
- Upload photos, videos, and text memories
- React and comment within the family circle

### 📅 Events & Celebrations
- Share upcoming family events like birthdays, anniversaries, reunions
- RSVP and reminders for event participation

### 📂 Secure Document Sharing
- Upload & store important family docs (e.g., **Aadhaar, Certificates**)
- Role-based access to documents

### 💸 Membership Fees
- Optional monthly **membership fee system**
- Track payments for each member
- Admin reports for due and paid members

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| **Backend**   | Django, Django Rest Framework |
| **Frontend**  | Django Templates, Bootstrap 5 |
| **Database**  | PostgreSQL / SQLite (for dev) |
| **Auth**      | Django Auth (Custom User Model) |
| **Storage**   | FileSystem / Cloud (S3-ready) |

---

## 🚀 Getting Started

### 🧰 Prerequisites
- Python 3.10+
- pip / venv
- PostgreSQL (optional, for production)

### ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/familyconnect.git
cd familyconnect

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup DB
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
