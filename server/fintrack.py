import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import atexit
from datetime import datetime, timedelta

transdbpath = "transactions.db"
usersdbpath = "users.db"

import os
print("Current working directory:", os.getcwd())

def returnParameters(data):
    words = data.split(" ")
    return words[0], datetime.strptime(words[0], "%m/%d/%Y"), words[1], int(words[2])

conn = sqlite3.connect(transdbpath)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Amount INTEGER NOT NULL,
    Type TEXT NOT NULL
)''')

# cursor.execute("DELETE FROM transactions")

conn.commit()

options = [
    "Housing",
    "Transportation",
    "Food",
    "Clothes",
    "Healthcare",
    "PersonalCare",
    "Education",
    "DebtPayments",
    "SavingsInvestments",
    "Entertainment",
    "GiftsDonations",
    "Misc"
]

# cursor.execute("INSERT INTO transactions (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("10/17/2024",15,0,0,0,0,0,0,0,0,0,0,0))

# cursor.execute("UPDATE employees SET Age = 30 WHERE Name = 'Charlie'")

conn.commit()

cursor.execute("SELECT * FROM transactions")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenditures (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Housing INTEGER NOT NULL,
    Transportation INTEGER NOT NULL,
    Food INTEGER NOT NULL,
    Clothes INTEGER NOT NULL,
    Healthcare INTEGER NOT NULL,
    PersonalCare INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    DebtPayments INTEGER NOT NULL,
    SavingsInvestments INTEGER NOT NULL,
    Entertainment INTEGER NOT NULL,
    GiftsDonations INTEGER NOT NULL,
    Misc INTEGER NOT NULL,
    Total INTEGER NOT NULL
)''')

# cursor.execute("DELETE FROM expenditures")

# Commit the changes
conn.commit()


# cursor.execute("INSERT INTO expenditures (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("10/17/2024",15,0,0,0,0,0,0,0,0,0,0,0,0))


conn.commit()

cursor.execute("SELECT * FROM expenditures")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()


cursor.execute('''CREATE TABLE IF NOT EXISTS weeklyexpenditures (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Housing INTEGER NOT NULL,
    Transportation INTEGER NOT NULL,
    Food INTEGER NOT NULL,
    Clothes INTEGER NOT NULL,
    Healthcare INTEGER NOT NULL,
    PersonalCare INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    DebtPayments INTEGER NOT NULL,
    SavingsInvestments INTEGER NOT NULL,
    Entertainment INTEGER NOT NULL,
    GiftsDonations INTEGER NOT NULL,
    Misc INTEGER NOT NULL,    
    Total INTEGER NOT NULL
)''')

# cursor.execute("DELETE FROM weeklyexpenditures")

conn.commit()


new_row_id1 = 1 # forget how used this should revisit

conn.commit()

cursor.execute("SELECT * FROM weeklyexpenditures")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()

conn.close()

uconn = sqlite3.connect('users.db')
ucursor = uconn.cursor()
# Read SQL table into DataFrame
#df = pd.read_sql_query("SELECT * FROM table_name", conn)
ucursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Salary INTEGER NOT NULL
)
''')

ucursor.execute("DELETE FROM users")

# Commit the changes
uconn.commit()

ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Andre', 80000)")
ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Pepper', 120000)")
ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Johnson', 75000)")

uconn.commit()

ucursor.execute("SELECT * FROM users")

# Fetch all results
rows = ucursor.fetchall()

# Print the results
for row in rows:
    print(row)

uconn.close()

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains


@app.route('/expenditures', methods=['POST'])
def updateExpenditures():

   # print("POST /expenditures was called")

    global new_row_id1

    data = request.get_json()


    # print(data)
        
    type = data['option']

    
    amount = int(data['amount'])


    date = data['date']

    date_object = datetime.strptime(date, "%m/%d/%Y")

    conn = sqlite3.connect(transdbpath)
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM expenditures WHERE Date = ?", (date,))
    exists = cursor.fetchone()[0] > 0
    if exists:
        cursor.execute(f"UPDATE expenditures SET {type} = {type} + ? WHERE Date = ?", (amount, date))
        cursor.execute(f"UPDATE expenditures SET Total = Total + ? WHERE Date = ?", (amount, date))
    else:
        # Insert a new row if the date does not exist

        cursor.execute('''INSERT INTO expenditures (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc, Total
        ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
        (date,))
      
        cursor.execute(f"UPDATE expenditures SET {type} = {type} + ? WHERE Date = ?", (amount, date)) # error
   
        cursor.execute(f"UPDATE expenditures SET Total = Total + ? WHERE Date = ?", (amount, date))
      
        cursor.execute("SELECT last_insert_rowid()")
 
        new_row_id1 = cursor.fetchone()[0]
       # print(f"The last inserted row ID is: {new_row_id1}")

    conn.commit()

    cursor.execute("SELECT * FROM expenditures")

    # Fetch all results
    rows = cursor.fetchall()

    # Print the results
    #for row in rows:
      #print(row)

    #print("new row id" + str(new_row_id1))
    #print("flag close")
    conn.close()
    return jsonify({'week1': 'test'})




@app.route('/weekly_expenditures', methods=['POST'])
def updateWeeklyExpenditures():

    data = request.get_json()
    
    print("weekly exp data")
    print(data)
        
    type = data['option']
    amount = int(data['amount'])
    date = data['date']

    date_object = datetime.strptime(date, "%m/%d/%Y")

    conn = sqlite3.connect(transdbpath)
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    cursor.execute(f'SELECT COUNT(*) FROM weeklyexpenditures')
    row_count = cursor.fetchone()[0]  # Get the first element of the result

    #Check if the table is empty
    if row_count == 0:
        #print(f'The table weeklyexps is empty.')
        cursor.execute("INSERT INTO weeklyexpenditures (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date,0,0,0,0,0,0,0,0,0,0,0,0,0))
    else:
        print("nothing")
       # print(f'The table weeklyexps has {row_count} rows.')


    cursor.execute("SELECT Date FROM weeklyexpenditures ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchone()
    lastdate = result[0]
    lastdateobj = datetime.strptime(lastdate, "%m/%d/%Y")

    date_difference = date_object - lastdateobj
    days = date_difference.days

    cursor.execute("SELECT COUNT(*) From expenditures WHERE Date = ?",(date,))
    exists = cursor.fetchone()[0] > 0
    #print(days)

    if days > 6:
        new_date = lastdateobj + timedelta(days=7)

        new_date_str = new_date.strftime("%m/%d/%Y")

        cursor.execute('''INSERT INTO weeklyexpenditures (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc, Total
        ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
        (new_date_str,))

        cursor.execute(f"UPDATE weeklyexpenditures SET {type} = {type} + ? WHERE Date = ?", (amount, new_date_str))
        cursor.execute(f"UPDATE weeklyexpenditures SET Total = Total + ? WHERE Date = ?", (amount, new_date_str))
        cursor.execute("SELECT last_insert_rowid()") 
    else:
        cursor.execute(f"UPDATE weeklyexpenditures SET {type} = {type} + ? WHERE Date = ?", (amount, lastdate))
        cursor.execute(f"UPDATE weeklyexpenditures SET Total = Total + ? WHERE Date = ?", (amount, lastdate))
    

    conn.commit()

    cursor.execute("SELECT * FROM weeklyexpenditures")

    # Fetch all results
    rows = cursor.fetchall()

  # Print the results
    #for row in rows:
      #print(row)

    print()

    conn.close()
    return jsonify({'week1': 'test'})


@app.route('/transactions', methods=['POST']) # post trans
def updateTransactions():

    print("POST /transactions was called")

    data = request.get_json()
        
    type = data['option']
    amount = int(data['amount'])
    date = data['date']

    conn = sqlite3.connect(transdbpath)

    cursor = conn.cursor()

    cursor.execute('''INSERT INTO transactions (Date, Amount, Type) VALUES (?, ?, ?)''', (date, amount, type))

    conn.commit()

    cursor.execute("SELECT * FROM transactions")

    # Fetch all results
    rows = cursor.fetchall()

  # Print the results
    for row in rows:
      print(row)

    conn.close()

    my_dict = {'week1': 1}
    my_dict2 = {'week1': [1, 2, 3, 4, 5]}
    
    return jsonify({'week1': 'test'})


@app.route('/expenditures', methods=['GET'])
def sendExpenditures():

    # print("GET /expenditures was called")

    conn = sqlite3.connect(transdbpath)
    conn.row_factory = sqlite3.Row # test this new cursor avoid <sqlite3.Row object at 0x0000022A108C2DD0> error
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM expenditures")
    rows = cursor.fetchall()
    result_dict = [dict(row) for row in rows]


   # print("Test of sql table to py dict: ")
    #print(result_dict)
    #print("End test of st to pd")
    #print()
    conn.close()

    return jsonify(result_dict)


@app.route('/weekly_expenditures', methods=['GET']) # get weekly
def sendWeeklyExpenditures():
     
    conn = sqlite3.connect(transdbpath)
    conn.row_factory = sqlite3.Row # test this new cursor avoid <sqlite3.Row object at 0x0000022A108C2DD0> error
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM weeklyexpenditures")
    rows = cursor.fetchall()
    result_dict = [dict(row) for row in rows]


    #print("Test of sql table to py dict: ")
    #print(result_dict)
    #print("End test of st to pd")
    #print()
    conn.close()

    return jsonify(result_dict)


@app.route('/transactions', methods=['GET']) # get trans
def sendTransactions():
    print("GET /transactions was called")

    conn = sqlite3.connect(transdbpath)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    result_dict = [dict(row) for row in rows]

    print(result_dict)

    conn.close()
    return jsonify(result_dict)
    #return jsonify({'week1': 'test'}) # this works
   

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
    app.run(debug=True)

# data = {'Date': ['2024-10-01', '2024-10-02', '2024-10-03'],
#         'Description': ['Salary', 'Groceries', 'Subscription'],
#         'Amount': [3000, -150, -10]}


# df = pd.DataFrame(data)
# print(df)

# df.to_sql('table_name', conn, if_exists='replace', index=False)




# Displaying the DataFrame
