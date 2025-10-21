🎾 Tennis Analytics Dashboard
Project Overview

This project is a comprehensive Tennis Analytics solution that extracts, stores, analyzes, and visualizes tennis competition data using the SportRadar API, MySQL, and Streamlit. The platform allows users to explore competitions, venues, and competitor rankings through an interactive web dashboard.

Features
1. Homepage Dashboard

Displays key statistics:

Total number of competitors

Total competitions

Highest points scored by a competitor

2. Competitor Search & Filter

Search competitors by name

Filter competitors by:

Rank range

Points threshold

3. Competitor Details Viewer

Displays detailed information for selected competitors:

Rank

Points

Competitions played

4. Leaderboards

Top-ranked competitors

Competitors with highest points

5. Venue & Competitions Analysis (Optional)

List all venues with capacities and surface types

Analyze competitions by categories and types

Project Structure
tennis_analytics/
│
├─ sports.sql               # SQL script to create database and tables
├─ apidata.py               # Python script to fetch data from SportRadar API
├─ tennis_dashboard.py      # Streamlit interactive dashboard
├─ README.md                # Project documentation
└─ requirements.txt         # Python dependencies

Setup Instructions
1. Database Setup

Open MySQL Workbench or command line.

Run the SQL script to create tables:

source path/to/sports.sql;


Ensure you have a database named tennis_db (or modify the script accordingly).

2. Fetch Data from SportRadar API

Install required Python packages:

pip install mysql-connector-python pandas requests


Run the API script:

python apidata.py


This populates the MySQL database with competitions, venues, and competitor rankings.

3. Run the Streamlit Dashboard

Install Streamlit:

pip install streamlit


Run the dashboard:

python -m streamlit run tennis_dashboard.py


Make sure your Python script is not named streamlit.py.

Dependencies

Python 3.8+

MySQL 8.0+

Python libraries:

streamlit

pandas

mysql-connector-python

requests

Usage

Open the dashboard in your browser (http://localhost:8501)

Explore key statistics on the homepage

Search for competitors and view details

Check leaderboards for top-ranked players

Future Enhancements

Add country-wise analysis (requires country column in Competitors table)

Include rank movement trends

Add interactive charts for competitions and venue analysis

Export dashboard reports to Excel or PDF

Author

Prathmesh Potdar
