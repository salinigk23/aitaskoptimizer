import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

st.set_page_config(page_title="Team Mood Tracker", layout="wide")
st.title("👥 Team Mood Tracker")
password = st.text_input("Enter dashboard password", type="password")
if password != "securepass123":
    st.error("Unauthorized access. Please enter the correct password.")
    st.stop()

def load_logs():
    conn = sqlite3.connect("logs.db")
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = load_logs()

if df.empty:
    st.warning("No mood data logged yet.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    st.sidebar.markdown("## Filter")
    user = st.sidebar.selectbox("Select user", ["All"] + sorted(df["user_id"].dropna().unique()))
    if user != "All":
        df = df[df["user_id"] == user]
        st.subheader(f"📈 Mood trends for: {user}")
    else:
        st.subheader("📈 Team-wide Mood Overview")

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="timestamp:T",
        y="emotion:N",
        color="user_id:N",
        tooltip=["timestamp", "user_id", "emotion"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(df[["timestamp", "user_id", "emotion", "recommended_tasks"]])