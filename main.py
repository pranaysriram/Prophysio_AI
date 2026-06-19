import streamlit as st

# Streamlit Config
st.set_page_config(
    page_title="ProPhysio AI",
    layout="wide",
    page_icon="⚕️"
)

import pandas as pd
import joblib
import time
import os
from groq import Groq
from dotenv import load_dotenv

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🔑 GROQ API key is missing! Add it to your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ==========================
# Session State
# ==========================
if "injury_risk" not in st.session_state:
    st.session_state.injury_risk = None

# ==========================
# AI Helper Function
# ==========================
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert sports physiotherapist "
                        "and sports nutritionist."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {e}"

# ==========================
# App Title
# ==========================
st.title("🏃 ProPhysio AI")
st.subheader("Smart Injury Prediction & Personalized Recovery Assistant")

# ==========================
# Load ML Model
# ==========================
try:
    model = joblib.load("adaboost_model1.pkl")
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    model = None

# ==========================
# Sidebar Inputs
# ==========================
with st.sidebar:
    st.header("⚙️ Athlete Information")

    Player_Age = st.number_input(
        "Age",
        min_value=0,
        value=24
    )

    Player_Weight = st.number_input(
        "Weight (kg)",
        min_value=0.0,
        value=66.25
    )

    Player_Height = st.number_input(
        "Height (cm)",
        min_value=0.0,
        value=175.73
    )

    Previous_Injuries = st.selectbox(
        "Previous Injuries?",
        [0, 1]
    )

    if Previous_Injuries == 1:
        Injury_Type = st.text_input(
            "Specify Injury",
            placeholder="e.g., ACL Tear, Ankle Sprain"
        )
    else:
        Injury_Type = "None"

    Training_Intensity = st.slider(
        "Training Intensity",
        min_value=0.1,
        max_value=10.0,
        value=5.0
    )

    Recovery_Time = st.number_input(
        "Recovery Time (days)",
        min_value=0,
        value=5
    )

    BMI_Classification = st.selectbox(
        "BMI Classification",
        [
            "Normal",
            "Obesity I",
            "Obesity II",
            "Overweight",
            "Underweight"
        ]
    )

    Diet_Type = st.radio(
        "Diet Preference",
        ["Veg", "Non-Veg"]
    )

# ==========================
# BMI One-Hot Encoding
# ==========================
bmi_dict = {
    "Normal": (1, 0, 0, 0, 0),
    "Obesity I": (0, 1, 0, 0, 0),
    "Obesity II": (0, 0, 1, 0, 0),
    "Overweight": (0, 0, 0, 1, 0),
    "Underweight": (0, 0, 0, 0, 1),
}

(
    BMI_Classification_Normal,
    BMI_Classification_Obesity_I,
    BMI_Classification_Obesity_II,
    BMI_Classification_Overweight,
    BMI_Classification_Underweight,
) = bmi_dict[BMI_Classification]

# ==========================
# Injury Treatment Section
# ==========================
if Injury_Type != "None":

    st.subheader("🏥 AI Injury Treatment Recommendation")

    treatment_prompt = f"""
    Provide:
    1. Injury Overview
    2. Immediate Treatment
    3. Rehabilitation Exercises
    4. Recovery Timeline
    5. Prevention Tips

    Injury: {Injury_Type}
    """

    treatment_plan = get_ai_response(treatment_prompt)

    st.info(treatment_plan)

# ==========================
# Injury Prediction
# ==========================
st.subheader("🧠 Injury Risk Prediction")

input_data = pd.DataFrame({
    "Player_Age": [Player_Age],
    "Player_Weight": [Player_Weight],
    "Player_Height": [Player_Height],
    "Previous_Injuries": [Previous_Injuries],
    "Training_Intensity": [Training_Intensity],
    "Recovery_Time": [Recovery_Time],
    "BMI_Classification_Normal": [BMI_Classification_Normal],
    "BMI_Classification_Obesity I": [BMI_Classification_Obesity_I],
    "BMI_Classification_Obesity II": [BMI_Classification_Obesity_II],
    "BMI_Classification_Overweight": [BMI_Classification_Overweight],
    "BMI_Classification_Underweight": [BMI_Classification_Underweight]
})

if st.button("⚡ Predict Injury Risk"):

    if model is not None:

        with st.spinner("Analyzing athlete data..."):
            time.sleep(2)

            prediction = model.predict(input_data)

        if prediction[0] == 1:

            st.session_state.injury_risk = 3

            st.error(
                "🚨 High Risk of Injury\n\n"
                "Model Accuracy: 63%"
            )

        else:

            st.session_state.injury_risk = 1

            st.success(
                "✅ Athlete Appears Fit\n\n"
                "Model Accuracy: 63%"
            )

    else:
        st.error("❌ Model unavailable.")

# ==========================
# Diet Plan Section
# ==========================
st.subheader("🥗 Personalized AI Diet Plan")

if st.session_state.injury_risk is not None:

    diet_prompt = f"""
    Create a personalized athlete diet plan.

    BMI Category: {BMI_Classification}
    Injury Risk Level: {st.session_state.injury_risk}
    Previous Injury: {Injury_Type}
    Diet Preference: {Diet_Type}

    Include:
    - Breakfast
    - Lunch
    - Dinner
    - Snacks
    - Protein Recommendation
    - Hydration Advice
    - Recovery Nutrition Tips
    """

    diet_plan = get_ai_response(diet_prompt)

    st.info(diet_plan)

else:
    st.warning(
        "⚠️ Predict injury risk first to generate a diet plan."
    )
