# streamlit_tennis.py

import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ----------------------------
# 1. Database Connection
# ----------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='sports',   # Replace with your database name
            user='root',            # Replace with your MySQL username
            password='1234'             # Replace with your password
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# ----------------------------
# 2. Helper Functions
# ----------------------------
def run_query(query):
    conn = get_connection()
    if conn:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return pd.DataFrame()

# ----------------------------
# 3. Streamlit App Layout
# ----------------------------
st.set_page_config(page_title="Tennis Analytics Dashboard", layout="wide")
st.title("🎾 Tennis Analytics Dashboard")

# ----------------------------
# Homepage Dashboard
# ----------------------------
st.header("🏠 Key Statistics")

# Total Competitors
total_competitors = run_query("SELECT COUNT(*) AS total FROM Competitors")
st.metric("Total Competitors", int(total_competitors['total'][0]))

# Total Competitions
total_competitions = run_query("SELECT COUNT(*) AS total FROM Competitions")
st.metric("Total Competitions", int(total_competitions['total'][0]))

# Highest Points
highest_points = run_query("SELECT MAX(points) AS highest FROM Competitor_Rankings")
st.metric("Highest Points Scored", int(highest_points['highest'][0]))

# ----------------------------
# Competitor Search & Filter
# ----------------------------
st.header("🔎 Competitor Search & Filter")

search_name = st.text_input("Search by Competitor Name")
rank_range = st.slider("Rank Range", 1, 100, (1, 10))
points_threshold = st.number_input("Minimum Points", min_value=0, value=0)

query = f"""
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
WHERE comp.name LIKE '%{search_name}%'
AND cr.rank_position BETWEEN {rank_range[0]} AND {rank_range[1]}
AND cr.points >= {points_threshold}
ORDER BY cr.rank_position
LIMIT 100
"""
competitor_df = run_query(query)
st.dataframe(competitor_df)

# ----------------------------
# Competitor Details Viewer
# ----------------------------
st.header("📋 Competitor Details Viewer")
selected_competitor = st.selectbox("Select Competitor", competitor_df['competitor_name'].tolist() if not competitor_df.empty else [])

if selected_competitor:
    details_query = f"""
    SELECT comp.name AS competitor_name, cr.rank_position, cr.points
    FROM Competitor_Rankings cr
    JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
    WHERE comp.name = '{selected_competitor}'
    """
    details_df = run_query(details_query)
    st.table(details_df)

# ----------------------------
# Leaderboards
# ----------------------------
st.header("🏆 Leaderboards")

st.subheader("Top 10 Ranked Competitors")
top_ranked = run_query("""
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
ORDER BY cr.rank_position
LIMIT 10
""")
st.table(top_ranked)

st.subheader("Top 10 Highest Points Competitors")
top_points = run_query("""
SELECT comp.name AS competitor_name, cr.rank_position, cr.points
FROM Competitor_Rankings cr
JOIN Competitors comp ON cr.competitor_id = comp.competitor_id
ORDER BY cr.points DESC
LIMIT 10
""")
st.table(top_points)
