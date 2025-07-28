import altair as alt
import streamlit as st
import pandas as pd
import snowflake.snowpark as sp
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("📍 Fraud Overview by Merchant Location")

exclude_unknown_on = st.toggle("Exclude transactions with unknown merchant location")
df = session.table("CC_TRANSACTIONS_DB.DBT_MDJIRLIC.MART_TRANSACTIONS_BY_MERCHANT_STATE").to_pandas()
heatmap_df = session.table("CC_TRANSACTIONS_DB.DBT_MDJIRLIC_MART.MART_TRANSACTIONS_WITH_MERCHANT_COORDINATES").to_pandas()

if exclude_unknown_on:
    df = df[df["IS_MERCHANT_LOCATION_VALID"] == True]

st.subheader("💰 Total Transaction Volume")
transaction_volume = alt.Chart(df).mark_bar().encode(
    x=alt.X("MERCHANT_STATE", title="State"),
    y=alt.Y("TOTAL_AMOUNT", title="Transaction Volume"),
    color=alt.Color("MERCHANT_STATE", legend=None)
).properties(
    width=600,
    height=400
)
st.altair_chart(transaction_volume)

st.subheader("📈 Fraud Rate")
fraud_rate = alt.Chart(df).mark_bar().encode(
    x=alt.X("MERCHANT_STATE", title="State"),
    y=alt.Y(
        "FRAUD_RATE_EXCL_UNKNOWN" if exclude_unknown_on else "FRAUD_RATE", 
        title="Fraud Rate", 
        axis=alt.Axis(format='%')
    ),
    color=alt.Color("MERCHANT_STATE", legend=None)
).properties(
    width=600,
    height=400
)
st.altair_chart(fraud_rate)

st.subheader("💸 Fraud Amount")
fraud_amount = alt.Chart(df).mark_bar().encode(
    x=alt.X("MERCHANT_STATE", title="State"),
    y=alt.Y("FRAUD_AMOUNT", title="Fraud Amount in USD"),
    color=alt.Color("MERCHANT_STATE", legend=None)
).properties(
    width=600,
    height=400
)
st.altair_chart(fraud_amount)

st.subheader("📊 Fraud Amount Share")
df["FRAUD_SHARE"] = df["FRAUD_AMOUNT"] / df["FRAUD_AMOUNT"].sum()

# Altair pie chart (using theta)
chart = alt.Chart(df).mark_arc().encode(
    theta=alt.Theta(field="FRAUD_SHARE", type="quantitative"),
    color=alt.Color(field="MERCHANT_STATE", type="nominal"),
    tooltip=[
        alt.Tooltip("MERCHANT_STATE", title="State"),
        alt.Tooltip("FRAUD_AMOUNT", title="Fraud Amount ($)", format=","),
        alt.Tooltip("FRAUD_SHARE", title="Share", format=".1%")
    ]
).properties(
    width=400,
    height=400,
    title="Fraud Amount Share per U.S. State"
)

st.subheader("🗺️ Fraud map")
heatmap_df = heatmap_df[heatmap_df["IS_FRAUD"] == True]
map_df = heatmap_df.rename(columns={
    "MERCHANT_LATITUDE": "latitude",
    "MERCHANT_LONGITUDE": "longitude"
})
st.map(map_df)

st.altair_chart(chart)

st.subheader("📀 Data")
st.dataframe(df)
st.dataframe(heatmap_df)