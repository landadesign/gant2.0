import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.dates import DateFormatter
import jpholiday
from datetime import datetime, timedelta

# Load Japanese font (if available)
jp_font_path = next((f for f in fm.findSystemFonts() if "Osaka" in f), None)
jp_font = fm.FontProperties(fname=jp_font_path) if jp_font_path else fm.FontProperties()

def get_working_days_duration(start_date, days):
    current_date = start_date
    working_days = 0
    while working_days < days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5 and not jpholiday.is_holiday(current_date):
            working_days += 1
    return current_date

# Streamlit UI
st.title("Gantt Chart Generator")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:", df.head())

        # Parse dates
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(10, 6))

        for i, task in enumerate(df.itertuples()):
            ax.barh(task.Task, (task.End_Date - task.Start_Date).days, left=task.Start_Date, color="skyblue")

        # Format plot
        ax.set_xlabel("Date", fontproperties=jp_font)
        ax.set_ylabel("Tasks", fontproperties=jp_font)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45, fontproperties=jp_font)
        plt.yticks(fontproperties=jp_font)
        ax.grid(True)

        # Show chart
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Example CSV download template
example_csv = "Task,Start Date,End Date\nTask 1,2025-01-01,2025-01-05\nTask 2,2025-01-02,2025-01-06"
st.download_button("Download Example CSV Template", data=example_csv, file_name="example_gantt_chart.csv")
