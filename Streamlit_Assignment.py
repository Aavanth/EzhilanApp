import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Dropdown for Category
selected_category = st.selectbox("Select a Category", df["Category"].unique())

# Multi-select for Sub_Category in the selected Category
sub_categories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub_Categories", sub_categories)

# Filter data based on selected Category and Sub_Category
filtered_df = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_sub_categories))]

# Line chart of sales for selected items
sales_by_sub_category = filtered_df.groupby("Sub_Category").sum()["Sales"]
st.line_chart(sales_by_sub_category)

# Metrics for selected items
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
overall_avg_profit_margin = (total_profit / total_sales) * 100

# Calculate overall average profit margin
overall_avg_profit_margin_all = (df["Profit"].sum() / df["Sales"].sum()) * 100

# Display metrics
st.metric("Total Sales", total_sales)
st.metric("Total Profit", total_profit)
st.metric("Overall Profit Margin (%)", overall_avg_profit_margin, delta=overall_avg_profit_margin - overall_avg_profit_margin_all)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")