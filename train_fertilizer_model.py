import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Step 1: Load the dataset
print("=" * 50)
print("STEP 1: Loading Fertilizer dataset...")
print("=" * 50)

csv_path = os.path.join('..', 'datasets', 'Fertilizer Prediction.csv')
df = pd.read_csv(csv_path)

print(f"✅ Dataset loaded successfully!")
print(f"   Total rows: {len(df)}")
print(f"   Columns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

# Step 2: Prepare the data
print("\n" + "=" * 50)
print("STEP 2: Preparing data for training...")
print("=" * 50)

# The dataset typically has columns: Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Phosphorus, Potassium, Fertilizer Name
# Let me check the actual column names
print(f"\nActual column names: {df.columns.tolist()}")

# Based on standard Fertilizer Prediction dataset, features are usually:
# Temperature, Humidity, Moisture, Soil_Type, Crop_Type, Nitrogen, Phosphorus, Potassium
# Target is: Fertilizer_Name

# Let me auto-detect columns
feature_cols = []
target_col = None

for col in df.columns:
    if col.lower() == 'fertilizer name' or col.lower() == 'fertilizer_name':
        target_col = col
    elif col.lower() not in ['fertilizer name', 'fertilizer_name']:
        feature_cols.append(col)

print(f"\n✅ Feature columns: {feature_cols}")
print(f"✅ Target column: {target_col}")

X = df[feature_cols]
y = df[target_col]

# Encode categorical features and target
label_encoders = {}

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
label_encoders['target'] = le_target

# Encode categorical feature columns (like Soil_Type, Crop_Type)
for col in feature_cols:
    if df[col].dtype == 'object':  # Categorical column
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

print(f"\n✅ Features shape: {X.shape}")
print(f"✅ Unique fertilizers: {len(le_target.classes_)}")
print(f"✅ Fertilizers: {list(le_target.classes_)}")

# Step 3: Split into training and testing
print("\n" + "=" * 50)
print("STEP 3: Splitting data (80% train, 20% test)...")
print("=" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

print(f"✅ Training samples: {len(X_train)}")
print(f"✅ Testing samples: {len(X_test)}")

# Step 4: Train the model
print("\n" + "=" * 50)
print("STEP 4: Training Random Forest model...")
print("=" * 50)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

print(f"✅ Model training complete!")

# Step 5: Check accuracy
print("\n" + "=" * 50)
print("STEP 5: Testing model accuracy...")
print("=" * 50)

train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print(f"✅ Training accuracy: {train_accuracy * 100:.2f}%")
print(f"✅ Testing accuracy: {test_accuracy * 100:.2f}%")

# Step 6: Save the model and encoders
print("\n" + "=" * 50)
print("STEP 6: Saving model and encoders...")
print("=" * 50)

# Save the trained model
model_path = os.path.join('api', 'fertilizer_model.pkl')
joblib.dump(model, model_path)

# Save the target encoder
encoder_path = os.path.join('api', 'fertilizer_label_encoder.pkl')
joblib.dump(le_target, encoder_path)

# Save the feature encoders for categorical columns
feature_encoders_path = os.path.join('api', 'fertilizer_feature_encoders.pkl')
joblib.dump(label_encoders, feature_encoders_path)

print(f"✅ Model saved to: {model_path}")
print(f"✅ Encoder saved to: {encoder_path}")

# Step 7: Test prediction with sample data
print("\n" + "=" * 50)
print("STEP 7: Testing a sample prediction...")
print("=" * 50)

# Create sample input based on actual feature columns
sample_input = {}
for col in feature_cols:
    if df[col].dtype == 'object':
        sample_input[col] = df[col].iloc[0]  # Use first value
    else:
        sample_input[col] = df[col].iloc[0]

print(f"✅ Sample input: {sample_input}")

print("\n" + "=" * 50)
print("🎉 FERTILIZER MODEL TRAINING COMPLETE! 🎉")
print("=" * 50)