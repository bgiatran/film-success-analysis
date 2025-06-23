import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import sys

# Load movie dataset
df = pd.read_csv("data/movies.csv")

# Extract release month from release_date
df["release_month"] = pd.to_datetime(df["release_date"], errors='coerce').dt.month

# Drop rows with missing critical values
df = df.dropna(subset=["budget", "release_month", "revenue"])

# Try different profitability thresholds
thresholds = [2.0, 1.5, 1.0, 0.8]
success = False

for t in thresholds:
    df["is_hit"] = df["revenue"] > (t * df["budget"])
    class_counts = df["is_hit"].value_counts()

    if len(class_counts) >= 2:
        print(f"Using threshold: revenue > {t} * budget")
        success = True
        break
    else:
        print(f"Only one class at threshold {t}: {class_counts.to_dict()}")

if not success:
    print("No valid threshold produced both hit and non-hit examples.")
    sys.exit(1)

# Features and target
feature_cols = ["budget", "release_month"]
X = df[feature_cols]
y = df["is_hit"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize using StandardScaler with column names preserved
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols, index=X_train.index)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Save model and scaler
os.makedirs("ml", exist_ok=True)
joblib.dump({
    "model": model,
    "scaler": scaler,
    "feature_names": feature_cols
}, "ml/hit_predictor.pkl")

print("Model and scaler saved to ml/hit_predictor.pkl")