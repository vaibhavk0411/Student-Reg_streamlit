import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn=sqlite3.connect("mydb.db")
    return conn


def createTable():
    with connectdb() as conn:
        cur= conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS student(name text, password text, roll int primary key, branch text)")
        conn.commit()

def addRecord(data):
    with connectdb() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO student(name,password, roll,branch)VALUES(?, ?, ?, ?)",data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already Registered")

def display():
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM STUDENT")
        result= cur.fetchall()
        return result


def signup():
    st.title("Registerationn Page")
    name= st.text_input("Enter Name")
    password= st.text_input("Enter Password", type='password')
    repassword= st.text_input("Retype your Password", type='password')
    roll=st.number_input("Enter Roll Number", format="%0.0f")
    branch=st.selectbox("Enter Branch",options=["CSE","AIML","MECHANICAL"])

    if st.button("SignIn"):
        if password != repassword:
            st.warning("Password Mismatch")
        else:
            addRecord((name,password,roll,branch))
            st.success("Student Registered !!!!")

#checking if roll no exists or not

def check_roll(roll):
    with connectdb() as conn:
        #it creates a cursor object that allows us to execute sql queries
        cur = conn.cursor()
        cur.execute("SELECT * FROM STUDENT WHERE roll=?", (roll,))
        #here we have placed ? to prevent sql injection 
        # here (roll,) is a tuple that contains the value that will be passed into the query
        return cur.fetchone()

def reset_password(roll,new_password):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE student SET password=? WHERE roll=?", (new_password, roll))
        conn.commit()

def reset_passwordpage():
    st.title("Reset Password")
    roll = st.number_input("Enter Roll Number", format="%0.0f")
    verified = check_roll(roll)  
    if st.button("Verify Roll Number"):
        if verified:
            st.success("Roll Number Found! Enter New Password Below.")
        else:
            st.error("Roll Number not found!")

    if verified:
        new_password = st.text_input("Enter New Password", type='password')
        repassword = st.text_input("Retype New Password", type='password')

        if st.button("Reset Password"):
            if new_password == repassword:
                reset_password(roll, new_password)
                st.success("Password reset successful!")
            else:
                st.error("Passwords do not match!")

def display_br(branch=None):
    with connectdb() as conn:
        cur = conn.cursor()
        if branch and branch != "All":
            cur.execute("SELECT * FROM student WHERE branch = ?", (branch,))
        else:
            cur.execute("SELECT * FROM student")
        return cur.fetchall()

def search_student(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE roll = ?", (roll,))
        return cur.fetchone()

def delete_student(roll):
    with connectdb() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE roll = ?", (roll,))
        conn.commit()
        st.success("Student record deleted successfully!")

def display_students():
    st.title("Student Records")
    branch_filter = st.selectbox("Filter by Branch", ["All", "CSE", "AIML", "MECHANICAL"])
    search_roll = st.text_input("Search by Roll Number")

    if search_roll:
        student = search_student(search_roll)
        if student:
            st.write("### Student Details")
            st.table([student])
            if st.button("Delete Student Record"):
                delete_student(search_roll)
        else:
            st.error("No student found with this Roll Number")
    else:
        students = display_br(branch_filter)
        st.write("### Student List")
        st.table(students)

createTable()
with st.sidebar:
    selected = option_menu("My App", ['Signup', 'Display All Records', 'Reset Password'])

if selected == 'Signup':
    signup()
elif selected == 'Reset Password':
    reset_passwordpage()
else:
    display_students()
    