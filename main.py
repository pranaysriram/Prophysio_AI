import streamlit as st

# Ensure this is the first Streamlit command
st.set_page_config(page_title="ProPhysio AI", layout="wide", page_icon="⚕️")

import pandas as pd
import joblib
import time
import os
import openai
from dotenv import load_dotenv

# Load Environment Variables for API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this is set in a .env file

# Ensure API Key is Set
if not API_KEY:
    st.error("🔑 OpenAI API key is missing! Set it in a .env file.")
else:
    openai.api_key = API_KEY

# Title Section
st.title("🏃 ProPhysio AI: Injury Prediction & Diet Chatbot")

# Load Injury Prediction Model
try:
    model = joblib.load('adaboost_model1.pkl')
except Exception as e:
    st.error(f"❌ Failed to load injury prediction model: {e}")
    model = None

# Sidebar for User Input
with st.sidebar:
    st.header("⚙️ User Information")
    
    Player_Age = st.number_input('Enter Age', min_value=0, value=24)
    Player_Weight = st.number_input('Enter Weight (kg)', min_value=0.0, value=66.25)
    Player_Height = st.number_input('Enter Height (cm)', min_value=0.0, value=175.73)
    Previous_Injuries = st.selectbox('Previous Injuries?', [0, 1])  
    
    # New Type of Injury Input
    if Previous_Injuries == 1:
        Injury_Type = st.text_input('Specify Type of Injury', placeholder='e.g., Ankle Sprain, ACL Tear')
    else:
        Injury_Type = "None"
    
    Training_Intensity = st.slider('Training Intensity (1-10)', min_value=0.1, max_value=10.0, value=0.46)
    Recovery_Time = st.number_input('Recovery Time (days)', min_value=0, value=5)

    BMI_Classification = st.selectbox('BMI Classification', ['Normal', 'Obesity I', 'Obesity II', 'Overweight', 'Underweight'])
    
    Diet_Type = st.radio("Diet Preference:", ["Veg", "Non-Veg"])

# Convert BMI to One-Hot Encoding
bmi_dict = {
    'Normal': (1, 0, 0, 0, 0),
    'Obesity I': (0, 1, 0, 0, 0),
    'Obesity II': (0, 0, 1, 0, 0),
    'Overweight': (0, 0, 0, 1, 0),
    'Underweight': (0, 0, 0, 0, 1)
}

BMI_Classification_Normal, BMI_Classification_Obesity_I, BMI_Classification_Obesity_II, BMI_Classification_Overweight, BMI_Classification_Underweight = bmi_dict[BMI_Classification]

# Injury Treatment Section
if Injury_Type != "None":
    st.subheader("🏥 Recommended Treatment for Injury")
    
    def get_injury_treatment(injury):
        prompt = f"You are a physiotherapist. Provide a treatment plan and rehabilitation exercises for {injury}."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": "You are a helpful physiotherapist."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {e}"

    treatment_plan = get_injury_treatment(Injury_Type)
    st.info(treatment_plan)

# Injury Prediction Section
st.subheader("🧟 Injury Risk Prediction")

input_data = pd.DataFrame({
    'Player_Age': [Player_Age],
    'Player_Weight': [Player_Weight],
    'Player_Height': [Player_Height],
    'Previous_Injuries': [Previous_Injuries],
    'Training_Intensity': [Training_Intensity],
    'Recovery_Time': [Recovery_Time],
    'BMI_Classification_Normal': [BMI_Classification_Normal],
    'BMI_Classification_Obesity I': [BMI_Classification_Obesity_I],
    'BMI_Classification_Obesity II': [BMI_Classification_Obesity_II],
    'BMI_Classification_Overweight': [BMI_Classification_Overweight],
    'BMI_Classification_Underweight': [BMI_Classification_Underweight]
})

injury_risk = None  

if st.button("⚡ Predict Injury using Adaboost Model"):
    if model:
        with st.spinner("Analyzing..."):
            time.sleep(2)
            prediction = model.predict(input_data)

        if prediction == 1:
            st.error("🚨 High Risk of Severe Injury!\n\nAccuracy of Adaboost Model: 63%")
            injury_risk = 3  
        else:
            st.success("✅ Athlete is Fit!\n\nAccuracy of Adaboost Model: 63%")
            injury_risk = 1  
    else:
        st.error("❌ Injury prediction model is not available!")

# AI-Powered Diet Chatbot
st.subheader("🥗 AI-Powered Personalized Diet Plan")

if injury_risk is not None:
    diet_chatbot = get_injury_treatment  # Using the same OpenAI model
    user_input = f"Athlete with {BMI_Classification} classification, injury risk level {injury_risk}, previous injury: {Injury_Type}, prefers {Diet_Type} diet."
    diet_plan = get_injury_treatment(user_input)
    st.info(diet_plan)
else:
    st.warning("⚠️ Please predict the injury risk first before generating a diet plan.")
