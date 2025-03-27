import sqlite3
import pandas as pd
from main import category_matcher

DB_FILE = "transactions.db"
DB_FILE2=("table2.db")

def delete_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
            DROP TABLE IF EXISTS transactions;
         """)
    conn.commit()
    conn.close()

def create_table():
    delete_table()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            Date DATE,
            Transaction_Id TEXT,
            Transaction_Name TEXT,
            Amount INTEGER
        )
    """)
    conn.commit()
    conn.close()

def store_records(df):
    conn = sqlite3.connect(DB_FILE)
    create_table()
    df.to_sql("transactions", conn, if_exists="append", index=False)
    conn.close()

def fetch_records():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df



# ----------------------------------------------table-2------------------------------------------

def del_table2():
    conn = sqlite3.connect(DB_FILE2)
    cursor = conn.cursor()
    cursor.execute("""
          DROP TABLE IF EXISTS table2;
       """)
    conn.commit()
    conn.close()

def create_table2():
    del_table2()
    conn = sqlite3.connect(DB_FILE2)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS table2 (
            Year INT,
            Month INT,
            Category TEXT,
            Amount INTEGER
        )
    """)
    conn.commit()
    conn.close()

def store_df_to_table2(df):
    create_table2()
    conn = sqlite3.connect(DB_FILE2)

    df1=category_matcher(df)

    print("our df1",df1)
    df1['Date'] = pd.to_datetime(df['Date'])
    df1["Month"] = df1["Date"].dt.month
    df1["Year"] = df1["Date"].dt.year

    grouped_df1=df1[['Year','Month','Category','Amount']]

    grouped_df1.to_sql("table2", conn, if_exists="append", index=False)
    return grouped_df1
    conn.close()

def fetch_records_table2():
    conn = sqlite3.connect(DB_FILE2)
    df = pd.read_sql("SELECT * FROM table2 ", conn)
    conn.close()
    return df


# ----------------------------------------drop-down-filtered-data---------------------------------


def fetch_filtered_data(year, month, category):
    conn = sqlite3.connect(DB_FILE2)

    query = "select Year, Month, Category, sum(Amount) as Amount from table2 where 1=1 "
    params = []

    if year:
        query= query+ "and Year = ?"
        params.append(year)

    if month:
        query = query + "and Month = ?"
        params.append(month)

    if category:
        query= query+ " and Category = ? "
        params.append(category)

    query+= "GROUP BY Year,Month,Category ORDER BY Year,Month"


    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# -----------------------------------------get-years-list-----------------------------------------------


def get_years_list():
    conn = sqlite3.connect(DB_FILE2)
    query="select DISTINCT year from Table2"
    li = pd.read_sql_query(query, conn)
    conn.close()
    return li["Year"].to_list()

# ----------------------------------------get-months-list-------------------------------------------------

def get_months_list(y):

    conn = sqlite3.connect(DB_FILE2)
    query = "select DISTINCT Month from Table2 where 1=1 and Year = ?"
    li = pd.read_sql_query(query, conn,params=[y])
    conn.close()
    return li

# -------------------------------------------line chart------------------------------------------------

def linechart(year):

    conn = sqlite3.connect(DB_FILE2)

    query = "select Month,sum(Amount) as Amount from table2 where 1=1"
    params = []

    if year:
        query = query + " and Year = ?"
        params.append(year)

    query += "group by Month"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# -------------------------------------------year and month bar chart--------------------------------------------------

def barchart(year,month):

    conn = sqlite3.connect(DB_FILE2)

    query = "select category, sum(Amount) as Amount from table2 where 1=1"
    params = []

    if year:
        query = query + " and Year = ?"
        params.append(year)

    if month:
        query = query + " and Month = ?"
        params.append(month)

    query += "GROUP BY Month,Category "

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()
    return df

# ----------------------------------------year and category--------------------------------------------------

def barchart_year_category(year, category):
    conn = sqlite3.connect(DB_FILE2)

    query = "select Month, sum(Amount) as Amount from table2 where 1=1"
    params = []

    if year:
        query = query + " and Year = ?"
        params.append(year)

    if category:
        query = query + " and Category = ?"

        params.append(category)

    query += "GROUP BY Month,Category "

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()
    return df

# ---------------------------------------- category--------------------------------------------------
def barchart_category( category):
    conn = sqlite3.connect(DB_FILE2)

    query = "select Year, sum(Amount) as Amount from table2 where 1=1"
    params = []

    if category:
        query = query + " and Category = ?"

        params.append(category)

    query += "GROUP BY Year,Category "

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()
    return df