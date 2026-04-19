<div align="center">
  <br />
  <h1>🏢 CMS PRO — Complaint Management System</h1>
  <p>
    <strong>A premium, enterprise-grade complaint tracking system with cinematic UI, built with Django.</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
    <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js" />
    <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License" />
  </p>
</div>

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [User Roles & Permissions](#-user-roles--permissions)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Contributing](#-contributing)

---

## 🎯 About the Project

**CMS PRO** is a next-generation complaint management system designed for modern enterprises. It features a cinematic dark-theme UI with glassmorphism effects, real-time complaint tracking, interactive star ratings, SLA monitoring, and powerful admin analytics — all wrapped in a premium user experience.

### 🌟 What Makes It Unique?
- **Cinematic Landing Page** — Animated hero section with floating orbs, gradient text, and scroll-reveal effects
- **Dark Glassmorphism UI** — Premium card designs with blur effects and glow borders
- **SLA Overdue System** — Auto-detects complaints open for 3+ days with pulsing red alerts
- **Star Rating System** — Interactive 5-star feedback widget for resolved complaints
- **Re-open Tickets** — Users can re-open unsatisfactory resolutions with tracked count
- **CSV & PDF Export** — Admin can download all complaint data as CSV or a professional PDF report with one click

---

## ✨ Key Features

### 🏠 Public Homepage
- Cinematic hero section with animated gradient text
- Live stats counter animation (complaints tracked, resolved, users, rating)
- Feature showcase cards with hover effects
- Scroll-reveal animations & floating orb background

### 🔐 Authentication & Roles
- Role-based login system (Admin / Manager / User)
- Custom registration with role selection
- Split-screen cinematic login page

### 📊 Dashboard
- **5 Stat Cards** — Total, Awaiting, In Progress, Resolved, SLA Overdue
- **Admin Charts** — Bar chart (department distribution) + Doughnut chart (status breakdown)
- **Admin Bonus Cards** — Avg. Satisfaction rating & Resolution rate
- **Activity Log Table** — Recent complaints with overdue badges
- **Notification Bell** — Dynamic overdue count badge with pulse animation

### 📋 Complaint Management
- Create complaints with **file attachments** (images, PDFs, docs)
- Categorized by department (IT, HR, Facility, Other)
- Real-time status tracking: `Open` → `In Progress` → `Resolved`
- **SLA Overdue Badge** — Red pulsing badge on 3+ day old unresolved complaints
- **Re-open Count** — Yellow badge showing how many times a ticket was reopened

### ⭐ Rating & Feedback
- Interactive 5-star rating widget with hover animations
- Text feedback field for detailed comments
- Shown only to complaint creator after resolution
- Admin sees average satisfaction score on dashboard

### 🔁 Re-open Tickets
- Users can re-open resolved complaints if unsatisfied
- Confirmation dialog before re-opening
- Auto-creates a remark in the activity timeline
- Reopen count tracked and displayed on cards

### 📤 CSV & PDF Export (Admin)
- One-click export of all complaint data to CSV or PDF
- Professional PDF report includes: Ref ID, Title, Category, Status, Assigned To, Created At, and Rating
- Timestamped filenames for easy tracking


### 🔔 Notification System
- Bell icon in navbar shows overdue complaint count
- Pulsing red badge animation when overdue > 0
- Visible across all pages

### 📎 File Attachments
- Upload files when creating complaints
- Supports: JPG, PNG, PDF, DOC, XLSX, TXT
- Download link on complaint detail page

### ⏱️ SLA Monitoring
- 3-day SLA threshold (configurable in model)
- Auto-calculated `is_overdue` and `days_open` properties
- Red glow on overdue complaint cards
- Overdue stat card on dashboard

---

## 💻 Tech Stack

| Category | Technology |
| --- | --- |
| **Backend** | Python 3.x, Django 6.0 |
| **Frontend** | HTML5, CSS3, JavaScript, Django Templates |
| **UI Framework** | Bootstrap 5, Font Awesome 6 |
| **Charts** | Chart.js |
| **Typography** | Google Fonts (Inter, Plus Jakarta Sans) |
| **Database** | SQLite3 |
| **Design** | Glassmorphism, Dark Theme, CSS Animations |

---

## 👥 User Roles & Permissions

### 👑 Admin
- Full system oversight with analytics dashboard
- Assign/reassign complaints to managers
- View bar & doughnut charts for department/status breakdown
- See average satisfaction rating and resolution rate
- Export all complaints to CSV
- Email notifications on assignment

### 💼 Manager
- View complaints assigned to them
- Update status (Open → In Progress → Resolved)
- Add official remarks with status change
- Email notifications to users on updates

### 👤 User
- Submit complaints with file attachments
- Track real-time status of their complaints
- Rate resolved complaints (1-5 stars + feedback)
- Re-open unsatisfactory resolutions
- View activity timeline with all remarks

---

## 📁 Project Structure

```
complaint-system/
├── core/                    # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── complaints/              # Main app
│   ├── models.py            # User, Complaint, ComplaintRemark, ComplaintRating
│   ├── views.py             # Homepage, Dashboard, CRUD, Export CSV
│   ├── forms.py             # ComplaintForm, RatingForm
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin registrations
├── templates/
│   ├── homepage.html        # Public landing page
│   ├── base.html            # Layout with sidebar & navbar
│   ├── complaints/
│   │   ├── dashboard.html   # Stats, charts, activity log
│   │   ├── complaint_list.html
│   │   ├── complaint_detail.html
│   │   └── complaint_form.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/
│   ├── css/style.css        # Premium dark theme CSS
│   └── img/                 # Logo, avatars, auth hero
├── media/                   # Uploaded attachments
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git installed

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
   Open your browser and navigate to `http://127.0.0.1:8000/`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/SELVAKUMAR-ANALYST/complaint-system/issues).

---

<div align="center">
  <p>Built with ❤️ by <strong>Selvakumar S</strong></p>
  <p>
    <a href="https://github.com/SELVAKUMAR-ANALYST">
      <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
    </a>
  </p>
</div>
