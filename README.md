# 🏃 ProPhysio AI: Injury Prediction & Diet Chatbot

ProPhysio AI is an AI-powered healthcare application designed to assist athletes in injury prevention, recovery, and nutrition planning. The system leverages Machine Learning and Generative AI to predict injury risks, provide personalized physiotherapy recommendations, and generate customized diet plans.

## 🚀 Features

### 🩺 Injury Risk Prediction
- Predicts the likelihood of severe injuries using an AdaBoost Machine Learning model.
- Considers factors such as:
  - Age
  - Weight
  - Height
  - Previous Injuries
  - Training Intensity
  - Recovery Time
  - BMI Classification

### 🏥 Physiotherapy Assistance
- Generates personalized treatment plans.
- Recommends rehabilitation exercises based on the injury type.
- Provides recovery guidance using OpenAI-powered AI assistance.

### 🥗 Personalized Diet Planning
- Creates customized diet plans for athletes.
- Supports:
  - Vegetarian Diet Plans
  - Non-Vegetarian Diet Plans
- Tailors recommendations according to BMI classification and injury risk level.

### 💻 Interactive Dashboard
- User-friendly web interface built with Streamlit.
- Real-time injury assessment and AI-generated recommendations.

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Machine Learning
- Scikit-learn
- AdaBoost Classifier
- Joblib

### Data Processing
- Pandas

### AI Integration
- OpenAI API

### Environment Management
- Python-dotenv

---

## 📂 Project Structure

```text
ProPhysio-AI/
│
├── app.py
├── adaboost_model1.pkl
├── requirements.txt
├── .env
├── README.md
│
└── assets/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ProPhysio-AI.git
cd ProPhysio-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 📊 Machine Learning Model

The injury prediction system uses an AdaBoost Classifier trained on athlete-related health and performance data.

### Input Features

- Player Age
- Player Weight
- Player Height
- Previous Injuries
- Training Intensity
- Recovery Time
- BMI Classification

### Output

- High Risk of Severe Injury
- Athlete is Fit

---

## 🤖 AI-Powered Assistance

The application integrates OpenAI models to:

- Generate rehabilitation plans
- Suggest physiotherapy exercises
- Create personalized diet plans
- Provide recovery recommendations

---

## 🎯 Use Cases

- Athlete Injury Prevention
- Sports Rehabilitation
- Fitness Monitoring
- Personalized Nutrition Planning
- Healthcare Assistance

---

## 🔮 Future Enhancements

- Wearable Sensor Integration
- Real-Time Injury Monitoring
- Injury Severity Classification
- Exercise Demonstration Videos
- Mobile Application Development
- Progress Tracking Dashboard
- Advanced Predictive Analytics

---

## 👨‍💻 Author

**Sriram Pranay Kumar**

B.Tech – Artificial Intelligence & Machine Learning

Passionate about AI, Machine Learning, Healthcare Technology, and Sports Analytics.

---

## 📄 License

This project is licensed under the MIT License.
