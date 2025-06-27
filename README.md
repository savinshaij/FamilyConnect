<h1 align="center">
  👨‍👩‍👧‍👦 FamilyConnect - Social Platform for Families
</h1>

<p align="center">
  <b>Private, secure, and engaging platform to connect and celebrate family moments together</b><br/>
  <i>Built with Django, SQLite, Tailwind CSS, and a focus on bonding & belonging</i>
</p>

---

<div align="center">

![Backend](https://img.shields.io/badge/Backend-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Auth](https://img.shields.io/badge/Auth-Secure_Email_Verification-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)

</div>

---

## 🌟 Features

- 🏠 **Family Groups**
  - Create & join family groups with approval-based membership
  - Group admins control access and manage requests

- 📝 **Posts & Sharing**
  - Public, private, and group-specific posts
  - Memory uploads including images, videos, and documents

- 📅 **Events**
  - Add and manage family events like birthdays and anniversaries
  - Calendar view and notifications

- 📂 **Documents**
  - Secure Aadhaar and family document uploads per group
  - Access-controlled storage

- 💸 **Monthly Membership**
  - Track monthly family group fees
  - Role-based permissions for payment tracking

---

## 🛠️ Tech Stack

| Layer       | Tech                        |
|-------------|-----------------------------|
| Backend     | Django                      |
| Database    | SQLite (default Django DB)  |
| Frontend    | Tailwind CSS                |
| Auth        | Django Allauth + Email OTP  |
| Media       | Cloudinary (optional)       |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip or pipenv
- Git

### Installation

```bash
# Clone the project
git clone https://github.com/savinshaij/FamilyConnect.git
cd FamilyConnect

# Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables in .env
cp .env.example .env

# Apply migrations & create superuser
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
