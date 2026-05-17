import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Step 1: Load the dataset
print("=" * 50)
print("STEP 1: Loading dataset...")
print("=" * 50)

# Go up one level to find the datasets folder
csv_path = os.path.join('..', 'datasets', 'Crop_recommendation.csv')
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

# Features (X) - soil parameters and weather
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]

# Target (y) - crop label
y = df['label']

# Encode crop names to numbers (for ML model)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"✅ Features shape: {X.shape}")
print(f"✅ Unique crops: {len(label_encoder.classes_)}")
print(f"✅ Crops: {list(label_encoder.classes_)}")

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
    n_estimators=100,  # Number of trees
    max_depth=10,      # Maximum depth of each tree
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

# Step 6: Save the model and label encoder
print("\n" + "=" * 50)
print("STEP 6: Saving model and encoder...")
print("=" * 50)

# Save the trained model
model_path = os.path.join('api', 'crop_model.pkl')
joblib.dump(model, model_path)

# Save the label encoder (to convert numbers back to crop names)
encoder_path = os.path.join('api', 'crop_label_encoder.pkl')
joblib.dump(label_encoder, encoder_path)

print(f"✅ Model saved to: {model_path}")
print(f"✅ Encoder saved to: {encoder_path}")

# Step 7: Test prediction with sample data
print("\n" + "=" * 50)
print("STEP 7: Testing a sample prediction...")
print("=" * 50)

# Sample soil data: N=90, P=42, K=43, temp=20, humidity=82, ph=6.5, rainfall=200
sample_data = [[90, 42, 43, 20.0, 82.0, 6.5, 200.0]]
sample_prediction = model.predict(sample_data)
sample_crop = label_encoder.inverse_transform(sample_prediction)

print(f"✅ Sample input: N=90, P=42, K=43, temp=20°C, humidity=82%, pH=6.5, rainfall=200mm")
print(f"✅ Predicted crop: {sample_crop[0]}")

print("\n" + "=" * 50)
print("🎉 MODEL TRAINING COMPLETE! 🎉")
print("=" * 50)