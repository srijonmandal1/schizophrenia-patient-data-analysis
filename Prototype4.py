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
from streamlit import session_state


patients_info = {
    "Emily": {
        "Age": 35,
        "Gender": "Female",
        "Location": "Austin, TX",
        "Medical History": "History of depression",
        "Doctor Notes": "(Date: Mar 10, 2024) Patient Emily, a 35-year-old female, presents with a stable mental health condition. No significant medical history was reported. Patient displays consistent adherence to treatment regimen and demonstrates positive response to therapy. Regular check-ups are advised to monitor progress and ensure continued stability.",
        "Medical Tests Performed": "CT",
        "Family Members with Condition": 1
    },
    "Ander": {
        "Age": 42,
        "Gender": "Male",
        "Location": "San Jose, CA",
        "Medical History": "History of Disorganized speech",
        "Doctor Notes": "(Date: Mar 19, 2024) Patient Ander, a 42-year-old male, has a history of depression. Current treatment regimen includes antidepressant medication and regular psychotherapy sessions. Patient's condition is stable with noticeable improvement in mood and overall well-being. Continued medication and therapy are recommended to maintain stability and prevent relapse.",
        "Medical Tests Performed": "MRI",
        "Family Members with Condition": 2
    },
    "Jack": {
        "Age": 28,
        "Gender": "Male",
        "Location": "Seatle, WA",
        "Medical History": "No significant medical history",
        "Doctor Notes": "(Date: April 5, 2024) Patient Jack, a 28-year-old male, presents as a new case. No significant medical history reported. Further evaluation is required to assess symptoms and formulate an appropriate treatment plan. Patient will undergo comprehensive assessment to determine diagnosis and develop tailored intervention strategies.",
        "Medical Tests Performed": "None",
        "Family Members with Condition": 0
    },
    "Prab": {
        "Age": 50,
        "Gender": "Male",
        "Location": "Bangalore, India",
        "Medical History": "Diabetes, hypertension",
        "Doctor Notes":"(Date: April 21, 2024) Patient Prab, a 50-year-old male, has a medical history of diabetes and hypertension. Both conditions are well-managed with appropriate medication and lifestyle modifications. Despite comorbidities, patient demonstrates good mental health with no significant psychiatric symptoms reported. Regular monitoring of both physical and mental health parameters is recommended to ensure optimal overall well-being.",
        "Medical Tests Performed": "None",
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
        #st.session_state.selected_page = "Home"

    if not st.session_state.logged_in:
        
        image_url = "https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.3&permmsgid=msg-a:r170675093240963886&th=18f2832283a38e48&view=att&disp=safe&realattid=f_lvkhfytl2"
        #col1, col2 = st.columns([1, 3])
        col1, col2 = st.columns(2)  
        with col1:
            st.image(image_url, width=500)

        with col2:
            #st.title("Login Page")
            # Using Markdown syntax to center align the title
            st.markdown("<h1 style='text-align: center;'>Log in</h1>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            # Using columns to create a layout with two columns
            col1, col2 = st.columns(2)

            # Adding buttons to the columns
            with col1:
                button1 = st.button("Log in")

            with col2:
                button2 = st.button("Sign up")

            if button1:
                if validate_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.name = get_user_details(username)
                    st.success("Logged in as {}".format(username))
                    st.write("Please enter Login again to continue")
                else:
                    st.error("Invalid username or password")
            if button2:
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
        # Page selection

        # Page selection
        #selected_page = st.sidebar.radio("Go to:", ("Home", "Info","Analyze","Ethical Guidelines", "New Patient"), key="sidebar_radio_" + st.session_state.selected_page)

        selected_page = st.sidebar.radio("Go to:", ("Home", "Info","Analyze","Ethical Guidelines", "New Patient"))

        # Store the selected page in session state
        st.session_state.selected_page = selected_page
      
        #page = st.sidebar.radio("Go to", ["Home","Info","Analyze","Ethical Guidelines","New Patient"], key="sidebar_radio_" + st.session_state.get("page", "Home"))
        # Store the selected page in session state
        #st.session_state.page = page

        if selected_page == "Home":
            display_home()
        elif selected_page == "Info":
            display_info()
        elif selected_page == "Analyze": 
            display_analyze()
        elif selected_page =="Ethical Guidelines":
            display_ethical_guidelines()
        #else:
        elif selected_page =="New Patient":
           add_patient()
           
            
def insert_patient_info(name, age, gender, location, history, tests, family_members):
    conn = sqlite3.connect('patients.db')  # Replace 'patients.db' with your database file path
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, gender, location, history, tests, family_members) VALUES (?, ?, ?, ?)", (name, age, gender, location, history, tests, family_members))
    conn.commit()
    conn.close()


def display_home():
    #st.title("Newsights")
    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r3397015451568297743&th=18f28604691af4e8&view=att&disp=safe&realattid=f_lvkj8rx90", width=700)
    st.write("Welcome back!")
    st.text("This is a tool developed by the NewSights AI team for Microsoft ICJ 2024")
    # Using columns to create a layout with two columns
    col1, col2 = st.columns(2)

    # Adding buttons to the columns
    with col1:
        st.write("")
        st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.3&permmsgid=msg-a:r170675093240963886&th=18f2832283a38e48&view=att&disp=safe&realattid=f_lvkhfytl2", width = 500)

    with col2:
        st.write("")
        st.write("")
        st.markdown("**What is Schizophrenia?**") 
        st.write("Schizophrenia is a complex and chronic mental health disorder marked by symptoms such as delusions, hallucinations, disorganized thinking and impaired social functioning, often co-occurs with depression, anxiety disorders, and substance abuse. ")
        st.write("The symptoms not only significantly impact individual’s functioning of daily life, but also pose a risk of harm to others.")
        st.write("Early intervention, comprehensive treatment approaches, and support from healthcare professionals, family, and community resources are essential in addressing the needs of individuals living with schizophrenia.")
        st.write("Please find more information in the information page.")
        #st.write("Schizophrenia is a severe mental disorder characterized by distorted thoughts, perceptions, emotions, and behaviors. It affects approximately 20 million people worldwide, making it one of the most prevalent and disabling mental illnesses globally. Despite its relatively low prevalence compared to other mental health conditions, schizophrenia imposes a significant burden on individuals, families, and society as a whole.")
        #st.write("Schizophrenia, a severe mental disorder characterized by distorted thinking, hallucinations, and social withdrawal, poses significant challenges for individuals and families across India. Despite being a global phenomenon, the prevalence and impact of schizophrenia in India are compounded by various factors, including cultural beliefs, limited access to mental health services, and pervasive stigma. In India, where mental health remains a taboo subject, individuals living with schizophrenia often face discrimination and social isolation, exacerbating their already considerable burden. Families caring for loved ones with schizophrenia grapple with emotional distress and financial strain, as they navigate a healthcare system ill-equipped to provide adequate support. Although the Indian government has made strides in addressing mental health through initiatives like the National Mental Health Programme (NMHP) and the Mental Healthcare Act, 2017, challenges persist in translating policy into effective action, particularly at the grassroots level. Furthermore, the stigma associated with speaking out about a mental illness is high. Mental illnesses are thought by many famillies, still, are caused by the fault of the person experiencing it.")
    
    st.write("")
    st.markdown("**Current Schizophrenia Statistics:**") 
    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.2&permmsgid=msg-a:r-8228753530922092587&th=18f28bfb5975492b&view=att&disp=safe&realattid=f_lvkmylrp1", width=500)


    if st.button("Add Patient"):
        #print("Add Patient button clicked")  # Print statement for debugging
        st.session_state.selected_page = "New Patient"  # Update session state to navigate to "New Patient" page
        #st.query_params["selected_page"] = "New Patient"  # Update URL query parameters to navigate to "New Patient" page



    # Define the list of patients
    patients = ["Ander", "Emily", "Jack", "Prab"]

    # Set the default selected patient
    default_index = patients.index("Ander")

    # Create the selectbox with the default selected patient
    selected_patient = st.selectbox("Select an existing patient:", patients, index=default_index, key="patient_selectbox")
    if selected_patient:
        st.subheader(f"Patient Information for {selected_patient}")

        # Store the selected patient in session state
        st.session_state.selected_patient = selected_patient

        # Using columns to create a layout with two columns
        col1, col2 = st.columns(2)

        # Adding buttons to the columns
        with col1:
            patient_info = patients_info[selected_patient]
            for field, value in patient_info.items():
                st.write(f"**{field}:** {value}")
            
        with col2:
            st.markdown("**Newsights Analysis:**") 
            st.write("")
            st.image("/Users/joydeepjana/Documents/Image 4-30-24 at 1.55 PM.jpeg", width = 350)

        
        # Using columns to create a layout with two columns
        col1, col2 = st.columns(2)

        # Adding buttons to the columns
        with col1:
            button1 = st.button("Update Profile")

        with col2:
            button2 = st.button("Add Medical Record")
        if button1:
            updated_info = {}  # Dictionary to store updated information
            for field, value in patient_info.items():
                updated_value = st.text_input(f"Update {field}", value, key=f"{selected_patient}_{field}")
                updated_info[field] = updated_value
            # Update patient_info dictionary with updated information
            patients_info[selected_patient].update(updated_info)
            st.success("Information updated successfully!")
        elif button2:
            st.session_state.selected_page = "Analyze"

def display_info():
    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r3397015451568297743&th=18f28604691af4e8&view=att&disp=safe&realattid=f_lvkj8rx90", width=700)
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

def display_analyze():

    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r3397015451568297743&th=18f28604691af4e8&view=att&disp=safe&realattid=f_lvkj8rx90", width=700)
    #st.title("The Model")
    #st.write("Here you will find information about the Model and App")
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
    # Access the selected patient from session state
    selected_patient = st.session_state.selected_patient
    st.title("Newsights Patient Analysis")

# Markdown for choosing input type
    input_type = st.radio("Choose Input Type:", ('Text', 'Speech', 'Video'))
    st.markdown(f"### You Selected {input_type} Input")


# Upload file based on input type
    if input_type == 'Text':
            file = upload_file('Text')
            # Analyze uploaded file
            if st.button("Analyze"):
                analyze_file(file)
            if st.checkbox("Graph Analysis"):
                st.image("/Users/joydeepjana/Documents/Image 5-2-24 at 9.32 PM.jpeg", width=700)
            if st.checkbox("Summary and keypoints"):
                st.write("This person's life has been a journey filled with struggles and triumphs as they navigate the complexities of living with schizophrenia. From a young age, they experienced feelings of isolation and misunderstanding, grappling with intrusive thoughts and overwhelming sensations that made daily tasks challenging.As they entered adulthood, the symptoms of schizophrenia became more pronounced, with hallucinations, delusions, and disorganized thinking dominating their reality. Despite the fear and stigma surrounding mental illness, they found the courage to seek help, supported by their loved ones.Treatment brought some relief, but also came with its own set of challenges, including medication side effects and the constant fear of relapse. Despite these obstacles, they found moments of peace and clarity amidst the chaos, often through creativity and self-expression.Their journey with schizophrenia is marked by resilience and determination, as they continue to strive for stability and wellness. They have learned to cherish the small victories and find hope in the face of adversity, knowing that they are more than their illness and that they have the strength to overcome whatever challenges lie ahead.")
    elif input_type == 'Speech':
            file = upload_file('Speech')
            if st.button("Analyze"):
                analyze_file(file)
            if st.checkbox("Graph Analysis"):
                st.image("/Users/joydeepjana/Documents/Image 5-2-24 at 9.09 PM.jpeg", width=700)
            if st.checkbox("Summary and keypoints"):
                st.write("This person's life has been a journey filled with struggles and triumphs as they navigate the complexities of living with schizophrenia. From a young age, they experienced feelings of isolation and misunderstanding, grappling with intrusive thoughts and overwhelming sensations that made daily tasks challenging.As they entered adulthood, the symptoms of schizophrenia became more pronounced, with hallucinations, delusions, and disorganized thinking dominating their reality. Despite the fear and stigma surrounding mental illness, they found the courage to seek help, supported by their loved ones.Treatment brought some relief, but also came with its own set of challenges, including medication side effects and the constant fear of relapse. Despite these obstacles, they found moments of peace and clarity amidst the chaos, often through creativity and self-expression.Their journey with schizophrenia is marked by resilience and determination, as they continue to strive for stability and wellness. They have learned to cherish the small victories and find hope in the face of adversity, knowing that they are more than their illness and that they have the strength to overcome whatever challenges lie ahead.")

    elif input_type == 'Video':
            file = upload_file('Video')
            if st.button("Analyze"):
                analyze_file(file)
            if st.checkbox("Graph Analysis"):
                st.image("/Users/joydeepjana/Documents/Image 5-2-24 at 9.09 PM.jpeg", width=700)
            if st.checkbox("Summary and keypoints"):
                st.write("This person's life has been a journey filled with struggles and triumphs as they navigate the complexities of living with schizophrenia. From a young age, they experienced feelings of isolation and misunderstanding, grappling with intrusive thoughts and overwhelming sensations that made daily tasks challenging.As they entered adulthood, the symptoms of schizophrenia became more pronounced, with hallucinations, delusions, and disorganized thinking dominating their reality. Despite the fear and stigma surrounding mental illness, they found the courage to seek help, supported by their loved ones.Treatment brought some relief, but also came with its own set of challenges, including medication side effects and the constant fear of relapse. Despite these obstacles, they found moments of peace and clarity amidst the chaos, often through creativity and self-expression.Their journey with schizophrenia is marked by resilience and determination, as they continue to strive for stability and wellness. They have learned to cherish the small victories and find hope in the face of adversity, knowing that they are more than their illness and that they have the strength to overcome whatever challenges lie ahead.")




# Produce graph
    #if st.checkbox("Produce Graph"):
            #produce_graph()
            #st.set_option('deprecation.showPyplotGlobalUse', False)

    #if st.checkbox("Voice modulation"):
            #produce_line_graph()
            #st.set_option('deprecation.showPyplotGlobalUse', False)

    #if st.checkbox("Summary and keypoints"):
            
            #st.write("This person's life has been a journey filled with struggles and triumphs as they navigate the complexities of living with schizophrenia. From a young age, they experienced feelings of isolation and misunderstanding, grappling with intrusive thoughts and overwhelming sensations that made daily tasks challenging.As they entered adulthood, the symptoms of schizophrenia became more pronounced, with hallucinations, delusions, and disorganized thinking dominating their reality. Despite the fear and stigma surrounding mental illness, they found the courage to seek help, supported by their loved ones.Treatment brought some relief, but also came with its own set of challenges, including medication side effects and the constant fear of relapse. Despite these obstacles, they found moments of peace and clarity amidst the chaos, often through creativity and self-expression.Their journey with schizophrenia is marked by resilience and determination, as they continue to strive for stability and wellness. They have learned to cherish the small victories and find hope in the face of adversity, knowing that they are more than their illness and that they have the strength to overcome whatever challenges lie ahead.")


def display_ethical_guidelines():
    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r3397015451568297743&th=18f28604691af4e8&view=att&disp=safe&realattid=f_lvkj8rx90", width=700)
    st.title("Ethical Guidelines")
    st.write("We follow strict ethical guidelines. In the following, you will find the regulations we adhere by")
    st.write("We follow strict ethical guidelines. In the following, you will find the regulations we adhere by: Ethical Guidelines for apps dealing with user information, particularly concerning schizophrenia, should prioritize the well-being, privacy, and autonomy of individuals while promoting trust, transparency, and responsible data usage. Here are some key principles:Informed Consent:obtain explicit and informed consent from users before collecting any personal information, including health-related data such as schizophrenia symptoms or treatment history.Privacy Protection: Implement robust security measures to safeguard users' data against unauthorized access, breaches, or misuse. Anonymize or pseudonymize sensitive information whenever possible to minimize the risk of re-identification.Data Minimization: Collect only the minimum amount of information necessary for the app's intended purpose. Avoid unnecessary data collection, especially concerning sensitive health information like schizophrenia.Transparency: Provide clear and accessible information about the app's data collection practices, including what types of data are collected, how they are used, and with whom they may be shared. Ensure transparency about any third-party services or partners involved in data processing.User Control: Empower users with control over their data by offering options to review, update, or delete their information. Allow users to customize their privacy settings and consent preferences.Purpose Limitation: Use user data only for the specific purposes disclosed to users and refrain from repurposing or sharing data for unrelated activities without obtaining additional consent.Data Accuracy: Take measures to ensure the accuracy and reliability of the information collected, especially when dealing with health-related data like schizophrenia symptoms or treatment outcomes.Ethical Use of AI: If the app incorporates artificial intelligence or machine learning algorithms, ensure that these technologies are used ethically and responsibly. Avoid reinforcing biases or stigmatizing behaviors related to schizophrenia.Avoid Stigmatization: Design app interfaces, content, and communications in a way that avoids stigmatizing language or imagery associated with mental health conditions, including schizophrenia. Promote a supportive and non-judgmental environment for users seeking help or information.Professional Guidance: If the app provides diagnostic or therapeutic support for schizophrenia, collaborate with mental health professionals to ensure the accuracy, safety, and ethicality of the app's content and functionalities.Accessibility: Ensure that the app is accessible to users with diverse needs, including those with schizophrenia or other mental health conditions. Provide options for customization, readability, and usability to accommodate different preferences and abilitiesContinuous Evaluation: Regularly assess and evaluate the app's compliance with ethical guidelines, user feedback, and emerging best practices in data privacy and mental health support. Commit to ongoing improvement and transparency in addressing ethical concerns.By adhering to these ethical guidelines, apps dealing with user information, especially those related to schizophrenia, can foster trust, promote user well-being, and contribute positively to mental health care and support.")



def add_patient():
    st.image("https://mail.google.com/mail/u/0?ui=2&ik=3a37770afa&attid=0.1&permmsgid=msg-a:r3397015451568297743&th=18f28604691af4e8&view=att&disp=safe&realattid=f_lvkj8rx90", width=700)
    st.title("Add Patient")
    new_patient_name = st.text_input("Enter the name of the new patient:")
    new_patient_age = st.number_input("Enter the age of the new patient:", min_value=0, max_value=150)
    new_patient_gender = st.text_input("Enter the gender of the new patient:")
    new_patient_location = st.text_input("Enter the location of the new patient:")
    new_patient_history = st.text_area("Enter the medical history of the new patient:")
    new_patient_tests = st.text_input("Enter the medical tests performed of the new patient:")
    new_patient_family_members = st.number_input("Enter the number of family members with the condition:", min_value=0, max_value=100)
# Connect to SQLite database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('patients.db')

# Create a cursor object to execute SQL commands
    cur = conn.cursor()

# Create the patients table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS patients (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               age INTEGER,
               gender TEXT,
               location TEXT,
               history TEXT,
               tests TEXT,
               family_members INTEGER
               )''')

# Commit changes
    conn.commit()

# Close the cursor and connection
    cur.close()
    conn.close()

    if st.button("Save"):
        # Save the new patient's information to the database or storage
        insert_patient_info(new_patient_name, new_patient_age, new_patient_gender, new_patient_location, new_patient_history, new_patient_tests, new_patient_family_members)
        st.success("New patient information saved successfully!")
def insert_patient(conn, name, age, gender, location, history, tests, family_members):
    """Insert a new patient into the patients table."""
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO patients (name, age, gender, location, history, tests, family_members)
                      VALUES (?, ?, ?, ?)''', (name, age, gender, location, history, tests, family_members))
    conn.commit()
    cursor.close()

def get_patient_by_name(conn, name):
    """Retrieve patient information by name."""
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM patients WHERE name = ?''', (name,))
    patient_info = cursor.fetchone()
    cursor.close()
    return patient_info

# Connect to SQLite database
conn = sqlite3.connect('example.db')


if __name__ == "__main__":
    main()
