import streamlit as st
import numpy as np
import joblib

# Load models
models = {
    "Logistic Regression": joblib.load("models/models_logistic_regression_model.pkl"),
    "Decision Tree": joblib.load("models/models_decision_tree_model.pkl")
}

st.title("📋 Farmer Credit Profile & Scoring")
st.markdown("Fill in the farmer’s information to check their **creditworthiness** and see **how different models rate them.**")

# Model selector
selected_model = st.selectbox("🔍 Select Prediction Model", list(models.keys()))

# Education mapping
education_mapping = {
    'NONE': 0, 'NURSERY': 0,
    'QUARANIC/INTEGRATED QUARANIC': 1, 'OTHER RELIGIOUS': 1,
    'PRIMARY': 2, 'ADULT EDUCATION': 2,
    'JUNIOR SECONDARY': 3, 'MODERN SCHOOL': 3, 'LOWER/UPPER 6': 3,
    'SENIOR SECONDARY': 4, 'SECONDARY VOCATIONAL/TECHNICAL/COMMERCIAL': 4,
    'TEACHER TRAINING': 5, 'TERTIARY VOCATIONAL/TECHNICAL/COMMERCIAL': 5,
    'POLYTECHNIC/PROF': 6, 'NATIONAL CERTIFICATE OF EDUCATION (NCE)': 6,
    '1st DEGREE': 6, 'HIGHER DEGREE (POST-GRADUATE)': 7,
    'OTHER': 8
}

sector_map = {"Urban": 0, "Rural": 1}

# Input form
with st.form("farmer_form"):
    age = st.slider("Age", 18, 60, 30)
    years = st.slider("Years in Community", 0, 40, 5)
    education = st.selectbox("Level of Education", list(education_mapping.keys()))
    phone = st.radio("Has Access to Phone?", ["Yes", "No"])
    sector = st.selectbox("Urban or Rural Sector", ["Rural", "Urban"])
    women_access = st.radio("Has Access to Women's Support?", ["Yes", "No"])
    submit = st.form_submit_button("🔍 Predict Creditworthiness")

if submit:
    # Encode inputs
    education_encoded = education_mapping.get(education, 8)
    phone_encoded = 1 if phone == "Yes" else 0
    sector_encoded = sector_map[sector]
    women_encoded = 1 if women_access == "Yes" else 0

    # Combine input into array
    X = np.array([[age, years, education_encoded, phone_encoded, sector_encoded, women_encoded]])
    model = models[selected_model]
    prediction = model.predict(X)[0]

    # Prediction result
    st.subheader("🧾 Prediction Result")
    if prediction == 1:
        st.success("✅ This farmer is likely to get a loan!")
    else:
        st.error("⚠️ This farmer is considered high risk.")

    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0][1]
        st.info(f"📊 Confidence Score (probability of approval): **{prob:.2f}**")

    # Tips section
    st.markdown("---")
    st.markdown("### 🔑 Tips to Improve Credit Score")
    st.markdown("""
    - Stay longer in your community  
    - Complete at least secondary education  
    - Maintain phone access for communication  
    - Join cooperative or women-focused support groups  
    """)

st.markdown("---")
st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Team Numerixa</strong></div>", unsafe_allow_html=True)
