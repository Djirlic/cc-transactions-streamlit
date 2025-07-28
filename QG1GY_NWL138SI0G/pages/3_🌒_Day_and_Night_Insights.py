import altair as alt
import streamlit as st
import pandas as pd
import snowflake.snowpark as sp
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("💳 Fraud Overview by Daytime")

df = session.table("CC_TRANSACTIONS_DB.DBT_MDJIRLIC.MART_TRANSACTIONS_DAY_VS_NIGHT").to_pandas()

st.subheader("💰 Total Transaction Volume")
transaction_volume = alt.Chart(df).mark_bar().encode(
    x=alt.X("IS_NIGHT_TRANSACTION", title="Is Night"),
    y=alt.Y("TOTAL_AMOUNT", title="Transaction Volume"),
    color=alt.Color("IS_NIGHT_TRANSACTION", legend=None)
).properties(
    width=600,
    height=400
)
st.altair_chart(transaction_volume)

st.subheader("📈 Fraud Rate")
fraud_rate = alt.Chart(df).mark_bar().encode(
    x=alt.X("IS_NIGHT_TRANSACTION", title="Is Night"),
    y=alt.Y("FRAUD_RATE", title="Fraud Rate", axis=alt.Axis(format='%')),
    color=alt.Color("IS_NIGHT_TRANSACTION", legend=None)
).properties(
    width=600,
    height=400
)
st.altair_chart(fraud_rate)

st.subheader("💸 Fraud Amount")
fraud_amount = alt.Chart(df).mark_bar().encode(
    x=alt.X("IS_NIGHT_TRANSACTION", title="Is Night"),
    y=alt.Y("FRAUD_AMOUNT", title="Fraud Amount in USD"),
    color=alt.Color("IS_NIGHT_TRANSACTION", legend=None)
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
    color=alt.Color(field="IS_NIGHT_TRANSACTION", type="nominal"),
    tooltip=[
        alt.Tooltip("IS_NIGHT_TRANSACTION", title="Is Night"),
        alt.Tooltip("FRAUD_AMOUNT", title="Fraud Amount ($)", format=","),
        alt.Tooltip("FRAUD_SHARE", title="Share", format=".1%")
    ]
).properties(
    width=400,
    height=400,
    title="Fraud Amount Share per Night (true) and Day (false)"
)

st.altair_chart(chart)

st.subheader("📀 Data")
st.dataframe(df)