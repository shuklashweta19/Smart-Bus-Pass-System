🚌 Smart Bus Pass Issuing System

A web-based application built using Flask + MySQL that allows users to apply for a bus pass online. This project simplifies the traditional bus pass issuing process by digitizing form submission, route handling, and pass generation.

📌 Features
📝 Online Bus Pass Application Form
👤 User Data Storage (Name, Age, Contact, etc.)
🛣️ Route Management (Source → Destination)
🎫 Automatic Pass Generation
📅 Auto Issue & Expiry Date (30 days validity)
✅ Success Confirmation Page
🎨 Clean and Responsive UI (HTML + CSS)
🛠️ Tech Stack
Frontend: HTML, CSS
Backend: Flask (Python)
Database: MySQL
📂 Project Structure
bus-pass-system/
│── app.py
│── templates/
│   ├── form.html
│   └── success.html
│── static/
│   └── style.css
│── README.md
⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/your-username/bus-pass-system.git
cd bus-pass-system
2️⃣ Install Dependencies
pip install flask mysql-connector-python
3️⃣ Setup MySQL Database

Create database:

CREATE DATABASE bus_pass_;
USE bus_pass_;

Create tables:

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15),
    email VARCHAR(100),
    user_type VARCHAR(50)
);

CREATE TABLE Routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    destination VARCHAR(100),
    distance INT,
    fare INT
);

CREATE TABLE Passes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    route_id INT,
    issue_date DATE,
    expiry_date DATE,
    pass_type VARCHAR(20),
    status VARCHAR(20)
);
4️⃣ Run the Application
python app.py

Open browser:

http://127.0.0.1:5000/
🚀 How It Works
User fills the bus pass application form
Data is stored in the Users table
Route details are stored in Routes table
Pass is generated and stored in Passes table
User sees a success confirmation page
🌱 Future Enhancements
🔐 User Login & Authentication
💳 Online Payment Integration
📍 Distance & Fare Calculation
📊 Admin Dashboard
📱 Mobile Responsive Improvements
📥 Download Bus Pass (PDF)
🎯 SDG Alignment

This project supports Sustainable Development Goal 12 (Responsible Consumption & Production) by:

Reducing paperwork
Digitizing public transport services
Improving efficiency in resource usage
👩‍💻 Author

Shweta Shukla
📍 Mumbai, India

⭐ Contribute

Feel free to fork this repository and contribute improvements!
