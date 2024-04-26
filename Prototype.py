import streamlit as st
import hashlib
import base64
import plotly.express as px
import os
import cv2
import numpy as np
import sqlite3
df = px.data.iris()

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/free-vector/hand-painted-watercolor-abstract-watercolor-background_23-2149018547.jpg?w=2000&t=st=1713079659~exp=1713080259~hmac=6c4e228f9e8fcdef477731c0b009a1ceac25a1d379d95470d1634f63db4b1acb");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{

background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def create_table():
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Function to insert a new user account into the database
def insert_user(username, password):
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)", (username, hashlib.sha256(password.encode()).hexdigest()))
    conn.commit()
    conn.close()

# Function to check if a username exists in the database
def username_exists(username):
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to validate login credentials
def validate_login(username, password):
    conn = sqlite3.connect('user_accounts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashlib.sha256(password.encode()).hexdigest()))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to create a SQLite database and table for storing user details
def create_details_table():
    conn = sqlite3.connect('user_details.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_details
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, name TEXT)''')
    conn.commit()
    conn.close()

# Function to insert or update user details in the database
def insert_user_details(username, name):
    conn = sqlite3.connect('user_details.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_details (username, name) VALUES (?, ?)", (username, name))
    conn.commit()
    conn.close()

# Function to retrieve user details from the database
def get_user_details(username):
    conn = sqlite3.connect('user_details.db')
    c = conn.cursor()
    c.execute("SELECT name FROM user_details WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Main function to run the application
def main():
    create_table()
    create_details_table()

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.name = ""

    if not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if validate_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.name = get_user_details(username)
                st.success("Logged in as {}".format(username))
                st.write("Please enter Login again to continue")
            else:
                st.error("Invalid username or password")
        
        st.title("Sign Up Page")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if username_exists(new_username):
                st.error("Username already exists. Please choose a different one.")
            else:
                insert_user(new_username, new_password)
                st.success("Account created successfully!")
                st.write("Now you can go back to the login page and log in with your new account.")
    else:
        st.title("Welcome to the Dashboard")
        st.write("Welcome back!")

        # Provide option to update name
        new_name = st.text_input("Enter your name:", st.session_state.name or "")
        if st.button("Save 1"):
            insert_user_details(st.session_state.username, new_name)
            st.write("Your name has been saved.")

        # Display restricted content only for logged-in users
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home","Info","About","Ethical Guidelines","Community","NewSights"])

        if page == "Home":
            st.title("Newsights")
            st.text("This is a tool developed by the NewSights Ai team")
            st.image("https://manoshanti.com/wp-content/uploads/2023/06/11-1.png")
            st.write("Schizophrenia is a severe mental disorder characterized by distorted thoughts, perceptions, emotions, and behaviors. It affects approximately 20 million people worldwide, making it one of the most prevalent and disabling mental illnesses globally. Despite its relatively low prevalence compared to other mental health conditions, schizophrenia imposes a significant burden on individuals, families, and society as a whole.")
            st.write("Schizophrenia, a severe mental disorder characterized by distorted thinking, hallucinations, and social withdrawal, poses significant challenges for individuals and families across India. Despite being a global phenomenon, the prevalence and impact of schizophrenia in India are compounded by various factors, including cultural beliefs, limited access to mental health services, and pervasive stigma. In India, where mental health remains a taboo subject, individuals living with schizophrenia often face discrimination and social isolation, exacerbating their already considerable burden. Families caring for loved ones with schizophrenia grapple with emotional distress and financial strain, as they navigate a healthcare system ill-equipped to provide adequate support. Although the Indian government has made strides in addressing mental health through initiatives like the National Mental Health Programme (NMHP) and the Mental Healthcare Act, 2017, challenges persist in translating policy into effective action, particularly at the grassroots level. Furthermore, the stigma associated with speaking out about a mental illness is high. Mental illnesses are thought by many famillies, still, are caused by the fault of the person experiencing it.")

        elif page == "Info":
            st.title("Info Page")
            st.write("Welcome to the Info Page.")
            st.write("Understanding Schizophrenia:")
            st.markdown("**What is Schizophrenia?**") 
            "Schizophrenia is a chronic and severe mental disorder that affects how a person thinks, feels, and behaves. It is characterized by disruptions in thought processes, perceptions, emotions, and behavior."

            st.markdown("**Statistics about Schizophrenia**")

            st.markdown("**Prevalence**")
            "Schizophrenia affects approximately 20 million people worldwide. It is a relatively common mental health condition that can have profound effects on individuals and their families."

            st.markdown("**Age of Onset**")
            "Schizophrenia typically emerges in late adolescence or early adulthood, although it can occur at any age. The onset of symptoms may be gradual or sudden, and early detection and intervention are crucial for effective management."
            st.markdown("**Global Impact**")
            "Schizophrenia is one of the leading causes of disability worldwide. It affects individuals across all socioeconomic and cultural backgrounds, leading to significant social, occupational, and personal impairment."

            st.markdown("**Mortality Rate**")
            "Individuals with schizophrenia have a significantly higher mortality rate compared to the general population. This increased mortality is primarily due to factors such as suicide, which occurs at a much higher rate among individuals with schizophrenia, as well as comorbid medical conditions such as cardiovascular disease."

            st.markdown("**Treatment Gap**")
            "Despite advances in mental health care, there remains a significant treatment gap for schizophrenia. Many individuals with schizophrenia do not receive adequate care or support, leading to poorer outcomes and increased risk of relapse and hospitalization."
        elif page == "About": 
            st.title("About")
            st.write("Here you will find information about the Model and App")
        elif page =="Community":
            st.title("Community")
            st.write("Here you can share, the data curated by you to improve and contribute to this model")
        elif page =="NewSights":
            st.title("NewSights")
            
            hi_boy = st.text_input("Enter your Age:", st.session_state.name or "")
            if st.button("Save 2/5"):
                eegrergerg = insert_user_details(st.session_state.username, hi_boy)
                
            hi_bos = st.text_input("Please give any preexisting conditions you may have, ex diabetes:", st.session_state.name or "")
            if st.button("Save 3/5"):
                ergergerg = insert_user_details(st.session_state.username, hi_bos)
           
            hi_bol = st.text_input("Symptoms that you may have experienced before:", st.session_state.name or "")
            if st.button("Save 4/5"):
                bybybybybybybybyb = insert_user_details(st.session_state.username, hi_bol)
            
            hi_bot = st.text_input("Please enter the number of familly members that you know of who have this condition:", st.session_state.name or "")
            if st.button("Save 5/5"):
                owowowowowowo = insert_user_details(st.session_state.username, hi_bot)
                st.write("**Thank you**! Your information has been saved in your account")
            

        else:
            st.title("Ethical Guidelines")
            st.write("We follow strict ethical guidelines. In the following, you will find the regulations we adhere by")

if __name__ == "__main__":
    main()