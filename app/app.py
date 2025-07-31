import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("app/sample_data.csv", parse_dates=["Date"])

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df["Date"].min().date())
end_date = st.sidebar.date_input("End Date", df["Date"].max().date())

# Filter by date
df_filtered = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# Title
st.title("💸 FinTech Dashboard")

# Summary Cards
total_credit = df_filtered[df_filtered["Type"] == "Credit"]["Amount"].sum()
total_debit = df_filtered[df_filtered["Type"] == "Debit"]["Amount"].sum()
balance = total_credit - total_debit

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Credit", f"₹{total_credit:,.2f}")
col2.metric("🧾 Total Debit", f"₹{total_debit:,.2f}")
col3.metric("📊 Balance", f"₹{balance:,.2f}", delta=f"{'+' if balance >= 0 else '-'}₹{abs(balance):,.2f}")

# Expense Breakdown
st.subheader("📂 Expenses by Category")
debit_df = df_filtered[df_filtered["Type"] == "Debit"]
if not debit_df.empty:
    fig = px.pie(debit_df, names="Category", values="Amount", title="Expenses by Category")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No debit transactions in selected date range.")

# Transaction Table
st.subheader("📋 All Transactions")
st.dataframe(df_filtered.sort_values("Date", ascending=False), use_container_width=True)
