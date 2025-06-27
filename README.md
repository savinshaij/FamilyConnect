<h1 align="center">
  💼 AttendEase - Modern HRMS for Smart Workplaces
</h1>

<p align="center">
  <b>A feature-rich HR Management System to track attendance, manage leaves, and ensure smooth handovers</b><br/>
  <i>Built with MERN stack, Tailwind CSS, and Framer Motion</i>
</p>

---

<div align="center">

![Tech](https://img.shields.io/badge/Stack-MERN-blueviolet?style=for-the-badge&logo=javascript)
![Frontend](https://img.shields.io/badge/Frontend-Next.js-black?style=for-the-badge&logo=next.js)
![Backend](https://img.shields.io/badge/Backend-Express.js-darkgreen?style=for-the-badge&logo=express)
![Database](https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb)
![CSS](https://img.shields.io/badge/CSS-Tailwind-blue?style=for-the-badge&logo=tailwindcss)
![Motion](https://img.shields.io/badge/Animations-Framer%20Motion-pink?style=for-the-badge&logo=framer)

</div>

---

## ✨ Key Features

- 👥 Role-Based Access (Admin, Manager, Employee)
- 🗓️ Leave Request & Approval (Sick, Casual, Earned, Half-day, Hourly)
- 📊 Attendance Monitoring (Daily, Weekly, Monthly)
- 🔁 Duty Handover & Work Substitution
- 🧮 Leave Balancing & Auto-Deduction
- 📈 Dynamic Reports & Dashboards

---

## 🔧 Tech Stack

| Layer       | Technology                    |
|------------|-------------------------------|
| Frontend    | `Next.js`, `Tailwind CSS`, `Framer Motion` |
| Backend     | `Node.js`, `Express.js`       |
| Database    | `MongoDB` (NoSQL)             |
| Auth        | `JWT`, `bcrypt`, Role-based   |
| Dev Tools   | `VS Code`, `Postman`, `Mongo Compass` |

---

## 🧠 Modules Breakdown

| Module                         | Estimated Time |
|--------------------------------|----------------|
| 👤 User Management              | 15 hours       |
| 📝 Leave Management             | 25 hours       |
| ⏱️ Attendance Tracking          | 20 hours       |
| 🔄 Work Substitution & Handover| 15 hours       |
| 📊 Reports & Analytics          | 15 hours       |
| 🧑‍💼 Admin Dashboard            | 15 hours       |
| **🧮 Total**                    | **105 hours**  |

---

## 🗃️ Database Example Schema

```js
// Employee Model
{
  employeeId: "EMP101",
  name: "Alice Thomas",
  department: "IT",
  email: "alice@example.com",
  password: "<hashed>",
  role: "employee",
  leaveBalance: {
    sick: 6,
    casual: 4,
    earned: 10,
  }
}

// Leave Request
{
  leaveId: "LV2025-002",
  employeeId: "EMP101",
  leaveType: "Sick",
  from: "2025-06-25",
  to: "2025-06-27",
  status: "Pending",
  substituteEmployeeId: "EMP110"
}
