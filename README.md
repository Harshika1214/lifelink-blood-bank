# 🩸 LifeLink - Blood Bank Management System

A modern web-based Blood Bank Management System built with Django and Python to manage blood donors, donations, blood inventory, and blood requests through a centralized platform.

---

## 📌 Project Overview

LifeLink is a Django-based web application designed to organize and simplify the management of blood bank operations.

The system provides separate workflows for users and administrators. Users can register, create their donor profile, record blood donations, submit blood requests, and track their request history.

Administrators can manage donor information, donations, blood inventory, and blood requests through Django's built-in administration panel.

The project focuses on implementing real-world backend concepts such as authentication, database relationships, form validation, business rules, transactions, CRUD operations, and inventory management.

---

## 🎯 Objectives

The main objectives of LifeLink are to:

- Maintain organized donor information.
- Record and track blood donations.
- Maintain blood group inventory.
- Allow users to submit blood requests.
- Allow users to track their request status.
- Provide administrators with centralized management.
- Apply validation and business rules to important operations.
- Provide a simple and responsive user interface.

---

# ✨ Features

## 👤 User Authentication

LifeLink provides a complete authentication workflow.

### Available functionality

- User registration
- User login
- User logout
- Password change
- Password reset workflow
- Session-based authentication
- Protected pages for authenticated users

Django's built-in authentication system is used to handle user accounts and password security.

---

# 🧑‍🩸 Donor Management

Registered users can create and manage their donor profiles.

### Donor information includes

- Full name
- Blood group
- Age
- Gender
- Phone number
- Address
- City
- Donor status
- Last donation date

Users can update their donor information whenever required.

---

# 🩸 Blood Donation Management

Registered donors can record blood donations through the application.

### Donation information includes

- Blood group
- Number of units
- Donation date
- Donation status
- Additional notes

The system automatically connects the donation with the authenticated donor.

### Donation Eligibility

LifeLink applies a 90-day gap between donations.

The system checks the donor's last donation date before allowing another donation.

```text
Previous Donation
       |
       v
Add 90 Days
       |
       v
Next Eligible Donation Date
       |
       v
Check Current Date
       |
       +---- Eligible
       |
       +---- Not Eligible

This prevents a donor from recording another donation before the required interval.
🏥 Blood Inventory Management
LifeLink maintains blood inventory for all supported blood groups.
Supported Blood Groups
- A+
- A-
- B+
- B-
- AB+
- AB-
- O+
- O-
The inventory stores the number of available blood units for each blood group.
Inventory Status
The system categorizes inventory based on available units:
Available
Low Stock
Critical

This helps administrators identify blood groups that require attention.
Automatic Inventory Update
When a completed donation is recorded, the donated units are automatically added to the corresponding blood group inventory.
Donation Completed
       |
       v
Find Blood Group
       |
       v
Update Inventory
       |
       v
Increase Available Units

🚑 Blood Request Management
Users can submit blood requests when blood is required for a patient.
Request information includes
- Patient name
- Blood group
- Units required
- Hospital name
- Hospital city
- Priority
- Required date
- Contact phone
- Reason for request
Request Priorities
- Normal
- Urgent
- Emergency
Request Statuses
- Pending
- Approved
- Fulfilled
- Rejected
Users can view and track their submitted requests.
Pending requests can also be cancelled by the requester.
📊 User Dashboard
The dashboard provides users with a centralized overview of their activity.
It can display:
- Donor profile information
- Donation history
- Number of donations
- Blood request history
- Number of blood requests
- Current request statuses
This gives users a quick overview of their blood donation and request activities.
🔎 Blood Inventory Search
The inventory page allows users to search for a specific blood group.
For example:
Search: O+

The application filters the inventory and displays the corresponding blood group information.
🛠️ Admin Panel
LifeLink uses Django's built-in Admin Panel for administrative management.
Administrators can manage:
Donor Profiles
- View donors
- Search donors
- Filter donors
- Update donor information
- Check donor status
Blood Inventory
- View blood groups
- Update available units
- Set minimum stock levels
- Monitor inventory status
Donations
- View donation records
- Search donations
- Filter donations
- Update donation status
- Review donation dates
Blood Requests
- View requests
- Search requests
- Filter requests
- Update request status
- Review request priority
- Review required dates
🏗️ Technology Stack
Backend
- Python 3
- Django 5
Frontend
- HTML5
- CSS3
- JavaScript
- Django Templates
Database
- SQLite
Development Tools
- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment
🧠 Django Concepts Used
This project demonstrates practical usage of several Django concepts.
Models
Database structure is created using Django Models.
Main models include:
DonorProfile
Donation
BloodInventory
BloodRequest

Forms
Django ModelForms and UserCreationForm are used for:
- Registration
- Donor profile management
- Blood donations
- Blood requests
Views
Django views handle:
- Authentication
- Dashboard
- Donor profile
- Donations
- Blood requests
- Inventory
- Password management
URL Routing
Django URL patterns connect browser requests with the appropriate views.
Templates
Django Templates are used to generate the application's user interface.
Django ORM
The Django ORM is used to create, retrieve, update, and delete database records without writing raw SQL for normal application operations.
Transactions
Database transactions are used during important operations such as completed blood donations and inventory updates.
🗄️ Database Relationships
The project uses relationships between Django models.
The main relationship structure is:
User
 |
 | One-to-One
 v
DonorProfile
 |
 | One-to-Many
 v
Donation

A user can also create multiple blood requests:
User
 |
 | One-to-Many
 v
BloodRequest

Blood inventory is maintained separately for each blood group.
🔄 Application Workflow
Donor Workflow
Register
   |
   v
Login
   |
   v
Create Donor Profile
   |
   v
Check Eligibility
   |
   v
Donate Blood
   |
   v
Donation Recorded
   |
   v
Inventory Updated

Blood Request Workflow
Login
   |
   v
Request Blood
   |
   v
Submit Request
   |
   v
Pending
   |
   v
Admin Reviews
   |
   +------> Approved
   |
   +------> Rejected
   |
   v
Fulfilled

🛡️ Validation
The application performs server-side validation for important user inputs.
Donor Age
Donor age must be between:
18 - 65 years

Donation Units
Donation units must be between:
1 - 5 units

Blood Request Units
Blood requests can contain:
1 - 20 units

Donation Eligibility
The system checks the 90-day interval before allowing another donation.
🔐 Security
The application uses Django's built-in security features, including:
- Password hashing
- CSRF protection
- Session authentication
- Login-required views
- Django password validation
- ORM-based database operations
- Django authentication middleware
Sensitive files such as:
.env
db.sqlite3
venv/
__pycache__/

are excluded from Git using .gitignore.
Production credentials and secret configuration should be supplied through environment variables rather than committed to GitHub.
📁 Project Structure
lifelink-blood-bank/
│
├── bloodbank/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   │
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── blood_extras.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── donate.html
│   ├── request_blood.html
│   ├── my_requests.html
│   ├── inventory.html
│   ├── change_password.html
│   │
│   └── registration/
│       ├── password_reset_form.html
│       ├── password_reset_done.html
│       ├── password_reset_confirm.html
│       ├── password_reset_complete.html
│       ├── password_reset_email.html
│       └── password_reset_subject.txt
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt

⚙️ Installation and Setup
1. Clone the Repository
git clone https://github.com/Harshika1214/lifelink-blood-bank.git

Move into the project directory:
cd lifelink-blood-bank

2. Create a Virtual Environment
On Windows:
python -m venv venv

Activate it:
venv\Scripts\activate

3. Install Dependencies
Install the project dependencies:
pip install -r requirements.txt

4. Apply Database Migrations
python manage.py migrate

5. Create an Admin Account
python manage.py createsuperuser

Enter the requested username, email, and password.
6. Start the Development Server
python manage.py runserver

Open the application in your browser:
http://127.0.0.1:8000/

🔑 Admin Panel
The Django administration panel is available at:
http://127.0.0.1:8000/admin/

Use the superuser credentials created with:
python manage.py createsuperuser

🖼️ Screenshots
Screenshots of the application will be added to this section.
Home Page
Add project screenshot here.
User Dashboard
Add project screenshot here.
Donor Profile
Add project screenshot here.
Blood Donation
Add project screenshot here.
Blood Inventory
Add project screenshot here.
Blood Request
Add project screenshot here.
Request Tracking
Add project screenshot here.
Admin Panel
Add project screenshot here.
🧪 Testing
The project can be tested using Django's built-in testing framework.
Run:
python manage.py test

Automated tests can cover:
- Authentication
- Donor registration
- Donation eligibility
- Inventory updates
- Blood requests
- Request cancellation
- Form validation
🚀 Future Improvements
Possible future improvements include:
- Real SMTP email notifications
- Blood request email alerts
- Donor search by blood group and location
- Hospital accounts
- Blood compatibility matching
- Blood expiry tracking
- Automatic inventory deduction after request fulfillment
- REST API
- PostgreSQL support
- Docker support
- Automated CI/CD
- Cloud deployment
- Advanced analytics dashboard
- Donation certificates
- Improved notification system
📚 Learning Outcomes
This project demonstrates practical knowledge of:
- Python
- Django
- Django Models
- Django ORM
- Database relationships
- CRUD operations
- Django Forms
- Form validation
- User authentication
- Session management
- URL routing
- Template rendering
- Transactions
- Django Admin
- Business logic
- Git
- GitHub
- Web application architecture
👩‍💻 Author
Harshika Matharia
GitHub:
https://github.com/Harshika1214
📄 License
This project is currently intended for educational and portfolio purposes