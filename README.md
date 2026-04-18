<div align="center">
  <br />
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/1200px-Django_logo.svg.png" alt="Django Logo" width="200">
  <br />
  <h1>🏢 Complaint Management System</h1>
  <p>
    <strong>A robust, role-based organizational complaint tracking system built with Django.</strong>
  </p>
  <p>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
    <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" /></a>
    <a href="https://getbootstrap.com/"><img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" /></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License" /></a>
  </p>
</div>

<hr />

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [User Roles & Permissions](#-user-roles--permissions)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 About the Project
The **Complaint Management System** is a streamlined web application designed to help organizations track, manage, and resolve internal complaints efficiently. With a hierarchical role-based access system, it ensures that issues raised by employees are categorized, assigned to the right managers, and addressed systematically.

## ✨ Key Features
- 🔐 **Role-Based Authentication:** Distinct dashboards and permissions for Admins, Managers, and Users.
- 🗂️ **Categorized Complaints:** Route issues by department (e.g., IT, HR, Facility Management).
- 📊 **Real-time Status Tracking:** Monitor tickets from `Open` to `In Progress` and `Resolved`.
- 💬 **Interactive Remarks:** Allow continuous communication on complaints via remarks.
- 🖼️ **User Profiles:** Support for custom profile pictures (Avatars).
- 📱 **Responsive UI:** Fully responsive interface built with Bootstrap 5.

## 💻 Tech Stack
| Category | Technology |
| --- | --- |
| **Backend** | Python, Django 5.0+ |
| **Frontend** | HTML5, CSS3, Django Templates, Bootstrap 5 |
| **Database** | SQLite3 (Configurable for PostgreSQL) |
| **Utilities** | Pillow (Image Processing), django-environ |

## 👥 User Roles & Permissions

### 👑 Admin
- Complete oversight of the system.
- Manage users (Assign roles, activate/deactivate accounts).
- Reassign complaints to different managers.

### 💼 Manager
- View complaints assigned specifically to them.
- Change the status of tickets (e.g., mark as Resolved).
- Add official remarks to update the user.

### 👤 User
- Submit new complaints to specific departments.
- View the real-time status of their own complaints.
- Reply with remarks for further clarification.

## 📸 Screenshots
*(Add screenshots of your application here)*
> **Pro Tip:** Include screenshots of the Dashboard, Complaint Submission Form, and the Remarks section.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites
- Python 3.8 or higher installed on your system.
- Git installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SELVAKUMAR-ANALYST/complaint-system.git
   cd complaint-system
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Admin Account):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/SELVAKUMAR-ANALYST/complaint-system/issues).

## 📄 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

<div align="center">
  <i>Created by Selvakumar S</i>
</div>
