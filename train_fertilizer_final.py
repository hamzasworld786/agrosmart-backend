import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
csv_path = os.path.join('..', 'datasets', 'Fertilizer Prediction.csv')
df = pd.read_csv(csv_path)

print("=" * 50)
print("TRAINING FERTILIZER MODEL WITH YOUR EXACT COLUMNS")
print("=" * 50)

# YOUR EXACT COLUMN NAMES (from the output)
feature_columns = ['Temparature', 'Humidity ', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']
target_column = 'Fertilizer Name'

print(f"Features: {feature_columns}")
print(f"Target: {target_column}")

# Prepare data
X = df[feature_columns].copy()  # Use .copy() to avoid warnings
y = df[target_column]

# Encode categorical columns
categorical_cols = ['Soil Type', 'Crop Type']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X.loc[:, col] = le.fit_transform(X[col])  # Use .loc to avoid warning
    encoders[col] = le
    joblib.dump(le, os.path.join('api', f'fertilizer_encoder_{col.replace(" ", "_")}.pkl'))
    print(f"✅ Encoded {col}")

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print(f"\n✅ Training Accuracy: {train_acc * 100:.2f}%")
print(f"✅ Testing Accuracy: {test_acc * 100:.2f}%")

# Save model and encoders
joblib.dump(model, os.path.join('api', 'fertilizer_model_final.pkl'))
joblib.dump(le_target, os.path.join('api', 'fertilizer_target_encoder_final.pkl'))
joblib.dump(feature_columns, os.path.join('api', 'fertilizer_features_final.pkl'))
joblib.dump(categorical_cols, os.path.join('api', 'fertilizer_categorical_cols_final.pkl'))

print("\n🎉 Model saved as fertilizer_model_final.pkl")
print("\n📋 To test the model, use this curl command:")
print('curl -X POST http://127.0.0.1:8000/api/fertilizer/ -H "Content-Type: application/json" -d "{\"Temparature\":26,\"Humidity \":52,\"Moisture\":38,\"Soil Type\":\"Sandy\",\"Crop Type\":\"Maize\",\"Nitrogen\":37,\"Potassium\":0,\"Phosphorous\":0}"')