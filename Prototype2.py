import streamlit as st
import hashlib
import base64
import plotly.express as px
import os
import cv2
import numpy as np
import sqlite3
import matplotlib as plt
import pandas as pd
import matplotlib.pyplot as plt

patients_info = {
    "Emily": {
        "Age": 35,
        "Medical History": "No significant medical history",
        "Doctor Notes": "Patient Emily, a 35-year-old female, presents with a stable mental health condition. No significant medical history was reported. Patient displays consistent adherence to treatment regimen and demonstrates positive response to therapy. Regular check-ups are advised to monitor progress and ensure continued stability.",
        "Family Members with Condition": 1
    },
    "Ander": {
        "Age": 42,
        "Medical History": "History of depression",
        "Doctor Notes": "Patient Ander, a 42-year-old male, has a history of depression. Current treatment regimen includes antidepressant medication and regular psychotherapy sessions. Patient's condition is stable with noticeable improvement in mood and overall well-being. Continued medication and therapy are recommended to maintain stability and prevent relapse.",
        "Family Members with Condition": 2
    },
    "Jack": {
        "Age": 28,
        "Medical History": "No significant medical history",
        "Doctor Notes": "Patient Jack, a 28-year-old male, presents as a new case. No significant medical history reported. Further evaluation is required to assess symptoms and formulate an appropriate treatment plan. Patient will undergo comprehensive assessment to determine diagnosis and develop tailored intervention strategies.",
        "Family Members with Condition": 0
    },
    "Prab": {
        "Age": 50,
        "Medical History": "Diabetes, hypertension",
        "Doctor Notes":"Patient Prab, a 50-year-old male, has a medical history of diabetes and hypertension. Both conditions are well-managed with appropriate medication and lifestyle modifications. Despite comorbidities, patient demonstrates good mental health with no significant psychiatric symptoms reported. Regular monitoring of both physical and mental health parameters is recommended to ensure optimal overall well-being.",
        "Family Members with Condition": 3
    }
}
df = px.data.iris()

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("")
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
        
       
        image_url = "https://mail.google.com/mail/u/0/?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r-2831946639571680047&th=18f2385a0a6670e6&view=fimg&realattid=f_lvj6r5sk0&disp=thd&attbid=ANGjdJ-v6nVAMb4hgcmA3R1y1anClqAykUwOrTKjy4zeYKjQ8-0r0PlvTlsYtGkyo20IK-aNpuPl7udhnl9uo1pfbaCuuwt5-lQL2nh1zts31XWwocMkqckuFt9DrKE&ats=2524608000000&sz=w3554-h2422"
        col1, col2 = st.columns([1, 3])  
        with col1:
            st.image(image_url, use_column_width=True)

        with col2:
            st.title("Login Page")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Log in"):
                if validate_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.name = get_user_details(username)
                    st.success("Logged in as {}".format(username))
                    st.write("Please enter Login again to continue")
                else:
                    st.error("Invalid username or password")
            if st.button("Sign up"):
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
        

        # Display restricted content only for logged-in users
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home","Info","Analyze","Ethical Guidelines","New Patient"])

        if page == "Home":
            st.title("Newsights")
            st.write("Welcome back!")
            st.text("This is a tool developed by the NewSights Ai team")
            st.image("https://mail.google.com/mail/u/0/?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r-2831946639571680047&th=18f2385a0a6670e6&view=fimg&realattid=f_lvj6r5sk0&disp=thd&attbid=ANGjdJ-v6nVAMb4hgcmA3R1y1anClqAykUwOrTKjy4zeYKjQ8-0r0PlvTlsYtGkyo20IK-aNpuPl7udhnl9uo1pfbaCuuwt5-lQL2nh1zts31XWwocMkqckuFt9DrKE&ats=2524608000000&sz=w3554-h5000")
            st.write("Schizophrenia is a severe mental disorder characterized by distorted thoughts, perceptions, emotions, and behaviors. It affects approximately 20 million people worldwide, making it one of the most prevalent and disabling mental illnesses globally. Despite its relatively low prevalence compared to other mental health conditions, schizophrenia imposes a significant burden on individuals, families, and society as a whole.")
            st.write("Schizophrenia, a severe mental disorder characterized by distorted thinking, hallucinations, and social withdrawal, poses significant challenges for individuals and families across India. Despite being a global phenomenon, the prevalence and impact of schizophrenia in India are compounded by various factors, including cultural beliefs, limited access to mental health services, and pervasive stigma. In India, where mental health remains a taboo subject, individuals living with schizophrenia often face discrimination and social isolation, exacerbating their already considerable burden. Families caring for loved ones with schizophrenia grapple with emotional distress and financial strain, as they navigate a healthcare system ill-equipped to provide adequate support. Although the Indian government has made strides in addressing mental health through initiatives like the National Mental Health Programme (NMHP) and the Mental Healthcare Act, 2017, challenges persist in translating policy into effective action, particularly at the grassroots level. Furthermore, the stigma associated with speaking out about a mental illness is high. Mental illnesses are thought by many famillies, still, are caused by the fault of the person experiencing it.")
            selected_patient = st.selectbox("Select a patient:", ["Emily", "Ander", "Jack", "Prab"])
            if selected_patient:
                st.subheader(f"Patient Information for {selected_patient}")
                patient_info = patients_info[selected_patient]
                for field, value in patient_info.items():
                    st.write(f"**{field}:** {value}")
                if st.button("Update"):
                    updated_info = {}  # Dictionary to store updated information
                    for field, value in patient_info.items():
                        updated_value = st.text_input(f"Update {field}", value, key=f"{selected_patient}_{field}")
                        updated_info[field] = updated_value
    # Update patient_info dictionary with updated information
                    patients_info[selected_patient].update(updated_info)
                    st.success("Information updated successfully!")
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
        elif page == "Analyze": 
            st.title("The Model")
            st.write("Here you will find information about the Model and App")
            def upload_file(file_type):
                file = st.file_uploader(f"Upload {file_type} File", type=['txt', 'csv', 'mp4'])
                if file:
                    st.success(f"{file_type} File Uploaded Successfully!")
                    return file
                else:
                    st.warning(f"Please Upload a {file_type} File.")
            def analyze_file(file):

    # Placeholder for analysis
                st.write("Placeholder for analysis of uploaded file.")
    # If it's a CSV file, display a sample dataframe
                if isinstance(file, pd.DataFrame):
                    st.write("Sample Data:")
                    st.write(file.head())
            def produce_graph():
    # Sample data for demonstration
                data = {'Category': ['Happy', 'Sad', 'Angry', 'Depressed'],
            'Values': [10, 20, 15, 25]}
                df = pd.DataFrame(data)
    
    # Plotting
                plt.bar(df['Category'], df['Values'])
                plt.xlabel('Emotion')
                plt.ylabel('Values')
                plt.title('Analysis')
                st.pyplot()
            def produce_line_graph():
    # Sample data for demonstration
                data = {'Category': ['0.5min', '1m', '1.5m', '2min'],
            'Values': [10, 20, 15, 25]}
                df = pd.DataFrame(data)
    
    # Plotting
                plt.plot(df['Category'], df['Values'])
                plt.xlabel('Time')
                plt.ylabel('Values')
                plt.title(' Line Graph')
                st.pyplot()
    # Title
            st.title("Newsights Patient Analysis")
    
    # Markdown for choosing input type
            input_type = st.radio("Choose Input Type:", ('Text', 'Speech', 'Video'))
            st.markdown(f"### You Selected {input_type} Input")
    
    # Upload file based on input type
            if input_type == 'Text':
                    file = upload_file('Text')
            elif input_type == 'Speech':
                    file = upload_file('Speech')
            elif input_type == 'Video':
                    file = upload_file('Video')
    
    # Analyze uploaded file
            if st.button("Analyze"):
                    analyze_file(file)
    
    # Produce graph
            if st.checkbox("Produce Graph"):
                    produce_graph()
                    st.set_option('deprecation.showPyplotGlobalUse', False)

            if st.checkbox("Voice modulation"):
                    produce_line_graph()
                    st.set_option('deprecation.showPyplotGlobalUse', False)
            if st.checkbox("Summary and keypoints"):
                    
                    st.write("This person's life has been a journey filled with struggles and triumphs as they navigate the complexities of living with schizophrenia. From a young age, they experienced feelings of isolation and misunderstanding, grappling with intrusive thoughts and overwhelming sensations that made daily tasks challenging.As they entered adulthood, the symptoms of schizophrenia became more pronounced, with hallucinations, delusions, and disorganized thinking dominating their reality. Despite the fear and stigma surrounding mental illness, they found the courage to seek help, supported by their loved ones.Treatment brought some relief, but also came with its own set of challenges, including medication side effects and the constant fear of relapse. Despite these obstacles, they found moments of peace and clarity amidst the chaos, often through creativity and self-expression.Their journey with schizophrenia is marked by resilience and determination, as they continue to strive for stability and wellness. They have learned to cherish the small victories and find hope in the face of adversity, knowing that they are more than their illness and that they have the strength to overcome whatever challenges lie ahead.")
