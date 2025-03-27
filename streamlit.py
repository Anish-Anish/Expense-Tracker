import streamlit as st
import pandas as pd
from dbversion import store_records, fetch_records,store_df_to_table2, fetch_records_table2, fetch_filtered_data,get_years_list, get_months_list, linechart, barchart, barchart_year_category, barchart_category
import requests
import matplotlib.pyplot as plt


st.title("Upload Excel")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
if uploaded_file is None:
    st.warning("No file uploaded")

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    if st.button("Upload"):
        store_records(df)
        st.success("Records successfully stored in the database!")


if st.button("View Expenses"):
    df = fetch_records()
    json_data={"data":df.to_dict(orient="records")}

    response=requests.post(
        "http://127.0.0.1:5001/view_data",
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
        st.warning("No file uploaded")

# ------------------------------------------------tabel 2-----------------------------------------------------

df = pd.read_excel(uploaded_file)
df_with_date = store_df_to_table2(df)
df_for_ref = fetch_records_table2()

# ----------------------------------------------side-bar------------------------------------------------------

st.sidebar.header("Filters")

years_list = get_years_list()

year = st.sidebar.selectbox("Select Year", years_list, index=None, placeholder="Choose a year")

months_list = get_months_list(year)

month = st.sidebar.selectbox("Select Month", months_list, index=None, placeholder="Choose a month")

categories = ['Travel', "Investment", "Utilities", "Entertainment", "Food", "Shopping"]

category = st.sidebar.selectbox("Select Category", categories, index=None, placeholder="Choose a category")

if st.sidebar.button("View Details"):

    df = fetch_filtered_data(year,month, category)

    if not df.empty:
        if not year and not month and not category:
            st.warning("You did not select any specification so displaying all expenses")
            st.table(df)
        elif year and month and category:
            st.table(df)
        elif not year and not month and category:
            df4=barchart_category(category)
            fig, ax = plt.subplots()
            st.table(df)
            ax.bar(df4['Year'], df4['Amount'])

            ax.set_xticks(years_list)
            st.pyplot(fig)

        elif not month and not category:

            st.title("Yearly Expenses")
            df1=linechart(year)
            st.table(df)
            fig, ax = plt.subplots()
            ax.plot(df1['Month'], df1['Amount'], marker='o')
            st.pyplot(fig)

        elif year and category :
            df3 = barchart_year_category(year,category)
            fig, ax = plt.subplots()
            st.table(df)
            ax.bar(df3['Month'], df3['Amount'])
            ax.set_xticks(range(1,13))
            st.pyplot(fig)

        elif year and month:
            df2=barchart(year,month)
            fig, ax = plt.subplots()
            st.table(df)
            ax.bar(df2['Category'], df2['Amount'])
            ax.set_xticklabels(df2['Category'],rotation=45)
            st.pyplot(fig)
    else:
        st.warning("You do not have any transactions")

