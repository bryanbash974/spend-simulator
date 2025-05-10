import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spend Dashboard", layout="wide")

st.title("Spend Intelligence Dashboard – Powered by Clarity")

# Load data automatically (no upload needed)
df = pd.read_csv("PrisonSampled2024.csv")

# Clean data
df["Unit.Price"] = pd.to_numeric(df["Unit.Price"], errors="coerce")
df["Quantity.Ordered"] = pd.to_numeric(df["Quantity.Ordered"], errors="coerce")
df["Ordered.Date"] = pd.to_datetime(df["Ordered.Date"], errors="coerce")
df.dropna(subset=["Unit.Price", "Quantity.Ordered", "Ordered.Date"], inplace=True)
df["Total.Spending"] = df["Unit.Price"] * df["Quantity.Ordered"]

# Get list of unique vendors
vendor_list = sorted(df["Vendor.Name"].dropna().unique().tolist())

# Sidebar controls
st.sidebar.header("Choose Your Scenario")
selected_vendor = st.sidebar.selectbox("Vendor:", vendor_list)
custom_unit_price = st.sidebar.number_input("Custom Unit Price ($)", min_value=0.0, value=10.0)
custom_quantity = st.sidebar.number_input("Custom Quantity", min_value=1, value=5)

# Calculate custom spend
custom_total = custom_unit_price * custom_quantity

# Main dashboard content
st.subheader(f"Monthly Spend for {selected_vendor}")
vendor_df = df[df["Vendor.Name"] == selected_vendor]

monthly = vendor_df.groupby(vendor_df["Ordered.Date"].dt.to_period("M"))["Total.Spending"].sum().reset_index()
monthly["Ordered.Date"] = monthly["Ordered.Date"].dt.to_timestamp()

fig = px.line(
    monthly, 
    x="Ordered.Date", 
    y="Total.Spending", 
    title="Spending Over Time",
    labels={"Ordered.Date": "Date", "Total.Spending": "Total Spending ($)"}
)

st.plotly_chart(fig, use_container_width=True)

# Show calculated result
st.metric(label="Your Custom Spend Estimate", value=f"${custom_total:,.2f}")

# Optional data preview
with st.expander("See Raw Data"):
    st.dataframe(vendor_df)
