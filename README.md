TaskFlow Pro: A Visual Productivity Ecosystem
Author: [Ayush Gite]
Video Demo: [https://youtu.be/KkInPSB5rZY?si=yi4yKp-Gel7g4ont]
Project Overview
TaskFlow Pro is a full-stack web application designed to bridge the gap between simple text-based "to-do lists" and complex project management tools. Developed as my final project for CS50x 2025, the application provides a centralized workspace where users can securely manage tasks, assign priority levels, and visualize their schedule through a dynamic calendar interface.

The core philosophy behind TaskFlow Pro is that productivity is not just about what needs to be done, but when and how urgently it needs to happen. By combining a relational database (SQLite) with a modern frontend (Bootstrap) and a powerful JavaScript API (FullCalendar), I created a tool that helps users reduce cognitive load and focus on execution.

Design Choices and Philosophy
1. The Decision to use the MVC Pattern
During the development process, I followed the Model-View-Controller (MVC) architecture.

The Model: My SQLite database (tasks.db) serves as the single source of truth.

The View: My HTML templates, styled with CSS and enhanced by Jinja2, handle the presentation.

The Controller: app.py acts as the brain, processing user input and deciding what data to show.

I chose this structure because it made debugging significantly easier. When a task wasn't appearing, I knew exactly where to look: was it not being saved in the Model, or was it not being rendered in the View?

2. User Authentication and Security
Security was a top priority. I implemented a registration and login system using Werkzeug’s password hashing.

Why Hashing? I learned that storing plain-text passwords is a major security risk. By using generate_password_hash, even if the database is compromised, user credentials remain secure.

Session Management: I used flask-session to keep users logged in. This prevents "Session Hijacking" and ensures that the user_id is stored securely on the server side rather than in an editable cookie on the user's browser.

3. The "Priority" Logic
One of the unique design choices I made was the visual prioritization system. In static/styles.css, I created classes for High, Medium, and Low priorities.

Implementation: Using Jinja2, the app dynamically assigns a class to each task based on the database value: class="priority-{{ task.priority }}".

The Impact: This creates a thick, color-coded border on the left side of each task. High priority is red, Medium is yellow, and Low is green. This allows for "instant scanning"—a user knows exactly what to work on first without reading a single word.

4. Integration of FullCalendar API
The most challenging part of this project was the calendar. I didn't want a static image; I wanted a living calendar.

The Problem: JavaScript cannot naturally "read" a Python SQL list.

The Solution: I used Jinja2 to loop through my Python tasks variable and generate JavaScript objects inside the <script> tag of index.html. This taught me how data can travel from a Server (Python) to a Database (SQL) and finally to a Client-side script (JavaScript).

File Structure Breakdown
Backend Core
app.py: Contains the routing logic. It handles the "GET" requests to show pages and the "POST" requests to modify data. I included specific logic in the index route to sort tasks so that "Pending" items always stay at the top.

helpers.py: Contains the login_required decorator. This is a crucial security feature that wraps around my routes to ensure unauthorized users cannot access the dashboard by simply typing the URL.

Data Layer
tasks.db: A relational SQLite database. I designed the schema with two tables: users and tasks. I used a Foreign Key (user_id) to link them, which is a fundamental concept I learned in the SQL unit of CS50.

Frontend Interface
templates/layout.html: The "Mother" template. It contains the navigation bar and the links to the Bootstrap CDN. By using Template Inheritance, I kept my code "DRY" (Don't Repeat Yourself).

templates/index.html: The main dashboard. It uses a Bootstrap grid system (rows and columns) to split the screen between the task list and the calendar.

static/styles.css: Beyond basic colors, I implemented "Glassmorphism" (subtle shadows and blurred backgrounds) to give the app a 2025 "SaaS" (Software as a Service) feel.

Technical Challenges & Lessons Learned
The biggest hurdle was Date Formatting. HTML date pickers provide dates as strings (YYYY-MM-DD), but sometimes different libraries expect different formats. I had to learn how to manipulate these strings in Python to ensure they were stored correctly in SQL and then read correctly by the FullCalendar JavaScript.

Another challenge was Responsive Design. I wanted the app to be shareable (as I hosted it via Codespaces). I used Bootstrap’s "Mobile-First" classes so that the split-screen layout stacks vertically on a smartphone but stays side-by-side on a laptop.

How to Install and Run
Clone the repository or download the files.

In your terminal, navigate to the folder and install the dependencies: pip install -r requirements.txt

Initialize the database by running the schema.

Start the Flask server: flask run

Open the local address provided by the terminal.

Conclusion
TaskFlow Pro is more than just a CS50 project; it is a culmination of everything I learned about web development, from database integrity to front-end user experience. It taught me that building a successful app requires a balance of secure back-end logic and intuitive front-end design.
