import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

  # 👈 required for app.py to import and call it
st.title("📊 Lender Dashboard - Farmer Credit Risk")

# Load models
models = {
    "Logistic Regression": joblib.load("models/models_logistic_regression_model.pkl"),
    "Decision Tree": joblib.load("models/models_decision_tree_model.pkl")
}

# Education mapping
education_mapping = {
    'NONE': 0,
    'NURSERY': 0,
    'QUARANIC/INTEGRATED QUARANIC': 1,
    'OTHER RELIGIOUS': 1,
    'PRIMARY': 2,
    'ADULT EDUCATION': 2,
    'JUNIOR SECONDARY': 3,
    'MODERN SCHOOL': 3,
    'LOWER/UPPER 6': 3,
    'SENIOR SECONDARY': 4,
    'SECONDARY VOCATIONAL/TECHNICAL/COMMERCIAL': 4,
    'TEACHER TRAINING': 5,
    'TERTIARY VOCATIONAL/TECHNICAL/COMMERCIAL': 5,
    'POLYTECHNIC/PROF': 6,
    'NATIONAL CERTIFICATE OF EDUCATION (NCE)': 6,
    '1st DEGREE': 6,
    'HIGHER DEGREE (POST-GRADUATE)': 7,
    'OTHER': 8
}
sector_map = {"Urban": 0, "Rural": 1}

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Farmer Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ✅ Show columns found (for debugging)
    st.write("📋 Columns in uploaded CSV:", df.columns.tolist())

    # ✅ Check for required columns
    required_columns = [
        'age', 'years_lived_in_community', 'level_of_education',
        'phone_access', 'sector', 'women_access'
    ]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"❌ Missing required column(s): {', '.join(missing)}")
    else:
        st.markdown("### 🔍 Select Model for Prediction")
        selected_model = st.selectbox("Choose a model", list(models.keys()))

        # Preprocess
        df['education_encoded'] = df['level_of_education'].map(education_mapping).fillna(8).astype(int)
        df['phone_access'] = df['phone_access'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)
        df['sector_encoded'] = df['sector'].map(sector_map).fillna(0).astype(int)
        df['women_access'] = df['women_access'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)

        features = df[['age', 'years_lived_in_community', 'education_encoded',
                       'phone_access', 'sector_encoded', 'women_access']]

        model = models[selected_model]
        df['credit_prediction'] = model.predict(features)
        if hasattr(model, "predict_proba"):
            df['confidence_score'] = model.predict_proba(features)[:, 1]

        # Rename for clarity
        df.rename(columns={'credit_prediction': 'Loan Approved (1=Yes)', 'confidence_score': 'Confidence Score'}, inplace=True)

        # Show table
        st.markdown("### 📋 Prediction Table")
        st.dataframe(df[['age', 'level_of_education', 'sector', 'Loan Approved (1=Yes)', 'Confidence Score']])

        # Summary Chart
        st.markdown("### 📊 Risk Summary")
        fig = px.histogram(df, x='Loan Approved (1=Yes)', color='Loan Approved (1=Yes)',
                           title="Loan Approval Distribution", nbins=2, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        # Download option
        st.download_button("💾 Download Results as CSV", df.to_csv(index=False), "credit_predictions.csv", "text/csv")
