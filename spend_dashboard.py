import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spend Simulator", layout="wide")

st.title("💼 Interactive Spend Scenario Tool")

uploaded_file = st.file_uploader("📁 Upload your procurement CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df["Unit.Price"] = pd.to_numeric(df["Unit.Price"], errors="coerce")
    df["Quantity.Ordered"] = pd.to_numeric(df["Quantity.Ordered"], errors="coerce")
    df["Ordered.Date"] = pd.to_datetime(df["Ordered.Date"], errors="coerce")
    df.dropna(subset=["Unit.Price", "Quantity.Ordered", "Ordered.Date"], inplace=True)
    df["Total.Spending"] = df["Unit.Price"] * df["Quantity.Ordered"]

    vendor_list = df["Vendor.Name"].dropna().unique().tolist()

    st.sidebar.header("🎛️ Custom Inputs")
    selected_vendor = st.sidebar.selectbox("Choose Vendor", vendor_list)
    custom_unit_price = st.sidebar.number_input("Enter Unit Price", min_value=0.0, value=10.0)
    custom_quantity = st.sidebar.number_input("Enter Quantity", min_value=1, value=5)

    st.metric("💰 Your Custom Spend", f"${custom_unit_price * custom_quantity:,.2f}")

    vendor_df = df[df["Vendor.Name"] == selected_vendor]
    monthly = vendor_df.groupby(vendor_df["Ordered.Date"].dt.to_period("M"))["Total.Spending"].sum().reset_index()
    monthly["Ordered.Date"] = monthly["Ordered.Date"].dt.to_timestamp()

    fig = px.line(monthly, x="Ordered.Date", y="Total.Spending", title=f"📈 Monthly Spend – {selected_vendor}")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Raw Data"):
        st.dataframe(vendor_df)
