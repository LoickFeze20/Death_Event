from streamlit import *
import streamlit as st
import pickle 
import time
import base64 

with open("class.pkl", "rb") as file:
    model = pickle.load(file)

# Configuration de la page
st.set_page_config(page_title="Death_Event", layout="wide",page_icon="💹")

# Chargement du CSS externe
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Charger l'image
with open("cardie.jpg", "rb") as file:
    img_data = file.read()
img_base64 = base64.b64encode(img_data).decode()

st.sidebar.markdown(
    f"""
    <img class="sidebar-img" src="data:image/jpeg;base64,{img_base64}">
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h2 style='text-align: center;'>Heart Attack</h2>", unsafe_allow_html=True)

# Liste des pages disponibles
pages = ["HOME🏠", "LEARN MORE📚", "CLASSIFICATION💹"]

# Initialisation des états de session
if "current_page" not in st.session_state:
    st.session_state.current_page = pages[0]

if "previous_page" not in st.session_state:
    st.session_state.previous_page = None

# Sélection de page via radio button
selected = st.sidebar.radio("📁 Sélectionnez une page :", pages, index=pages.index(st.session_state.current_page), key="page_radio")

# Gestion de navigation
def go_to(page_name):
    st.session_state.previous_page = st.session_state.current_page
    st.session_state.current_page = page_name

# Changement de page
if selected != st.session_state.current_page:
    go_to(selected)

# Affichage conditionnel selon la sélection
if st.session_state.current_page == "HOME🏠":
    # En-tête HTML
    st.markdown("""
    <div class="header-container">
        <div class="header-title"> WELCOME TO THE MACHINE 
        LEARNING PLATFORM DEDICATED TO CLASSIFICATION📊</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="text">
        Welcome to the machine learning platform dedicated 
        to classification allowing you to predict whether a
        subject (sick) can die or survive according to their 
        health and personal parameters. Go to the Sidebar to:
    </div>
    """, unsafe_allow_html=True) 
    st.markdown("""
    <div class="texte">
        🟩 Proceed to classification to make the prediction⏳or
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="texte">
        🟩 Learn more about classification or machine learning 📚
    </div>
    """, unsafe_allow_html=True)
    
elif st.session_state.current_page == "LEARN MORE📚":
    st.markdown("""
    <div class="header-container">
        <div class="header-title"> Everything you need to know about Machine Learning
        and classification</div>
    </div>
    """, unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Machine Learning")
        st.image("img1.jpg", caption="Process", width=300) 
        st.markdown("Machine learning is a branch of artificial intelligence that focuses on building systems that can learn from data and improve their performance over time without being explicitly programmed. It allows computers to automatically identify patterns and make decisions or predictions based on input data. Machine learning is used in a wide range of applications, such as recommendation systems, speech recognition, and autonomous vehicles.")
    with col2:
        st.subheader("Classification")
        st.image("img.jpg", caption="Procces", width=300) 
        st.markdown("Classification is a type of supervised machine learning task where the goal is to assign a label or category to input data based on a training set of labeled examples. The algorithm learns from this training data to classify new, unseen data correctly. For example, a classification model can determine whether an email is spam or not, or predict the type of disease based on medical records. Common classification algorithms include logistic regression, decision trees, support vector machines, and neural networks.")
    
elif st.session_state.current_page == "CLASSIFICATION💹":
    st.markdown("""
    <div class="header-container">
        <div class="header-title"> CLASSIFICATION TABLE 💹</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('Fill in the information below to predict the Death Event')
    
    with st.form(key='Details'):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("Personal Information")
            age = st.number_input("Age",step=1.0)
            sex = st.selectbox("Sex",['Yes' , 'No'])
            smoking = st.selectbox("Smoking",['Yes' , 'No'])
            kpi1, kpi2 = st.columns(2)
            ejection_fraction = kpi1.number_input("Ejection Fraction",step=1)
            creatinine_phosphokinase = kpi2.number_input("creatinine Phosphokinase",step=1)
        with col2:
            st.subheader("Diseases")
            diabetes = st.selectbox("Diabetes",['Yes' , 'No'])
            anaemia = st.selectbox("Anaemia",['Yes' , 'No'])
            high_blood_pressure = st.selectbox("High Blood Pressure",['Yes' , 'No'])
            Time = st.number_input("Time",step=1)
        with col3:
            st.subheader("Serums")
            serum_creatinine = st.number_input("Serum Creatinine",step=0.1)
            serum_sodium = st.number_input("Serum Sodium",step=1)
            platelets = st.number_input("Platelets",step=1.0)
        
        #Encodage
        sex_encode = 1 if sex == 'male' else 0   
        smoker_encode = 1 if smoking == 'yes' else 0
        diabetes_encode = 1 if diabetes == 'yes' else 0
        anaemia_encode = 1 if anaemia == 'yes' else 0
        high_blood_pressure_encode = 1 if anaemia == 'yes' else 0
        
        input_data = [[age,anaemia_encode,creatinine_phosphokinase,diabetes_encode,
                    ejection_fraction,high_blood_pressure_encode,platelets,serum_creatinine,
                    serum_sodium,sex_encode,smoker_encode,Time]] 
        
        st_state = st.form_submit_button('**Predict Patient**')
        if st_state:
            with st.spinner('calcul en cours..'):
                prediction = model.predict(input_data)[0]
                time.sleep(1)
            st.success('Prediction terminée')
            st.markdown(f"The risk of dying is:**{prediction}**")
            if prediction == 1:
                st.error("The patient is at high risk of death")
            else:
                st.success("The patient is at low risk of death")
                
# Affichage du bouton retour en haut de la page principale
#           

st.markdown(f'<div class="page"><b>{st.session_state.current_page}</b></div>', unsafe_allow_html=True)
