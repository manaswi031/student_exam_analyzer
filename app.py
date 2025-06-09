import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Student Exam Result Analyzer", layout="wide")

# Title of the app
st.title("📊 Student Exam Result Analyzer")

# Upload CSV
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# Load Data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample data.")
    df = pd.read_csv("sample_results.csv")

# Calculate percentage score
df["% Score"] = (df["Marks Obtained"] / df["Max Marks"]) * 100

# Show summary metrics
st.subheader("📌 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", df["Student ID"].nunique())
col2.metric("Average Score", f"{df['% Score'].mean():.2f}%")
col3.metric("Pass % (>=35%)", f"{(df['% Score'] >= 35).mean() * 100:.2f}%")

# Subject Filter
st.subheader("🔍 Filter by Subject")
subjects = ["All"] + sorted(df["Subject"].unique())
selected_subject = st.selectbox("Select Subject", subjects)

if selected_subject != "All":
    df = df[df["Subject"] == selected_subject]

# Highlight logic
def highlight_rows(row):
    if row["% Score"] < 35:
        return ["background-color: #ffcccc"] * len(row)
    elif row["% Score"] >= 90:
        return ["background-color: #ccffcc"] * len(row)
    else:
        return [""] * len(row)

# Show full data table
st.subheader("📋 Full Result Table")
st.dataframe(df.style.apply(highlight_rows, axis=1), use_container_width=True)

# Top 10 performers
st.subheader("🏅 Top 10 Performers")
top10 = df.sort_values(by="% Score", ascending=False).head(10)
st.dataframe(top10.style.apply(highlight_rows, axis=1), use_container_width=True)

# CSV Download
st.subheader("⬇️ Export Filtered Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_results.csv",
    mime="text/csv"
)

# Optional charts
with st.expander("📈 Visualizations"):
    st.bar_chart(df["% Score"])
    st.write("Subject Distribution:")
    st.dataframe(df["Subject"].value_counts())
