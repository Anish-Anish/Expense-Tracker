import streamlit as st
import pandas as pd
from dbversion import (
    store_records, fetch_records, store_df_to_table2, fetch_records_table2,
    fetch_filtered_data, get_years_list, get_months_list, linechart,
    barchart, barchart_year_category, barchart_category
)
import requests
import matplotlib.pyplot as plt


BACKEND_URL = "https://expense-tracker-5-vk1n.onrender.com"

st.title("Upload Excel")


uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if st.button("Upload"):
        store_records(df)
        st.success("Records successfully stored in the database!")
else:
    st.warning("No file uploaded yet. Please upload an Excel file.")


if st.button("View Expenses"):
    df = fetch_records()

    if df.empty:
        st.warning("No expense records found. Please upload data first.")
    else:
        json_data = {"data": df.to_dict(orient="records")}
        response = requests.post(
            f"{BACKEND_URL}/view_data",
            json=json_data,
            proxies={"http": None, "https": None}
        )

        if response.status_code == 200:
            result = response.json()
            df1 = pd.DataFrame(result["total_data"])
            st.subheader("Expense by Category")
            st.dataframe(df1)
            fig, ax = plt.subplots()
            ax.pie(df1["Amount"], labels=df1["Category"], autopct="%1.1f%%", startangle=90)
            st.pyplot(fig)
        else:
            st.error("Failed to retrieve data from the backend.")


if uploaded_file:
    df_with_date = store_df_to_table2(df)
    df_for_ref = fetch_records_table2()


st.sidebar.header("Filters")
years_list = get_years_list()
year = st.sidebar.selectbox("Select Year", years_list, index=None, placeholder="Choose a year")

months_list = get_months_list(year)
month = st.sidebar.selectbox("Select Month", months_list, index=None, placeholder="Choose a month")

categories = ['Travel', "Investment", "Utilities", "Entertainment", "Food", "Shopping"]
category = st.sidebar.selectbox("Select Category", categories, index=None, placeholder="Choose a category")


if st.sidebar.button("View Details"):
    df = fetch_filtered_data(year, month, category)

    if df.empty:
        st.warning("You do not have any transactions.")
    else:
        st.table(df)

        if not year and not month and not category:
            st.warning("No specific filters applied. Showing all expenses.")

        elif not year and not month and category:
            df4 = barchart_category(category)
            fig, ax = plt.subplots()
            ax.bar(df4['Year'], df4['Amount'])
            ax.set_xticks(years_list)
            st.pyplot(fig)

        elif not month and not category:
            st.title("Yearly Expenses")
            df1 = linechart(year)
            fig, ax = plt.subplots()
            ax.plot(df1['Month'], df1['Amount'], marker='o')
            st.pyplot(fig)

        elif year and category:
            df3 = barchart_year_category(year, category)
            fig, ax = plt.subplots()
            ax.bar(df3['Month'], df3['Amount'])
            ax.set_xticks(range(1, 13))
            st.pyplot(fig)

        elif year and month:
            df2 = barchart(year, month)
            fig, ax = plt.subplots()
            ax.bar(df2['Category'], df2['Amount'])
            ax.set_xticklabels(df2['Category'], rotation=45)
            st.pyplot(fig)
