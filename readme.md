Task Manager System

Introduction

This is a simple task management system built using Flask and MySQL. It allows users to add, edit, delete, and view tasks with ease. The project demonstrates full-stack development skills by integrating a dynamic frontend with a backend API and a relational database.

Features

Add Tasks: Users can create new tasks by providing a title, summary, description, due date, and priority.

Edit Tasks: Users can update existing tasks, including title, details, and deadlines.

Delete Tasks: Remove tasks from the system.

View Tasks: Displays all tasks dynamically, including their details such as priority and due date.

Technology Stack

Frontend: HTML, CSS, JavaScript (Dynamic interactions via Fetch API)

Backend: Flask (Python)

Database: MySQL

How to Run the Project

Prerequisites

Python 3.x

MySQL installed and running

pip for managing Python dependencies

Installation Steps

Clone this repository:

git clone https://github.com/your-username/pythonproduct.git
cd pythonproduct

Install required Python packages:

pip install -r requirements.txt

Set up the MySQL database:

Log into your MySQL server and create a database:

CREATE DATABASE task_manager;

Update the db connection settings in app.py with your MySQL credentials.

Run the Flask application:

python app.py

Open your browser and navigate to:

http://127.0.0.1:5000

Directory Structure

pythonproduct/
|-- app.py              # Main Flask application
|-- index.html          # Frontend HTML file
|-- requirements.txt    # Python dependencies

Future Improvements

Add user authentication for task management.

Implement task filtering and sorting by priority or due date.

Deploy the application to a cloud service like Render or Heroku.

License

This project is licensed under the MIT License. Feel free to use and modify it.