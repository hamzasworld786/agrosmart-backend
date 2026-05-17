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
print("DATASET INFO")
print("=" * 50)
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nData types:")
print(df.dtypes)

# DEFINE FEATURES AND TARGET
# Adjust these based on your actual column names
# Most common pattern:
feature_columns = ['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Phosphorus', 'Potassium']
target_column = 'Fertilizer Name'

# Check if columns exist, if not, print available ones
missing_cols = []
for col in feature_columns:
    if col not in df.columns:
        missing_cols.append(col)

if missing_cols:
    print(f"\n⚠️ Missing columns: {missing_cols}")
    print(f"Available columns: {df.columns.tolist()}")
    print("\nPlease update feature_columns list with correct names from above")
else:
    print(f"\n✅ All feature columns found: {feature_columns}")
    
    # Prepare data
    X = df[feature_columns]
    y = df[target_column]
    
    # Encode categorical columns
    categorical_cols = ['Soil Type', 'Crop Type']
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        # Save encoder
        joblib.dump(le, os.path.join('api', f'fertilizer_encoder_{col.replace(" ", "_")}.pkl'))
    
    # Encode target
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save model and encoders
    joblib.dump(model, os.path.join('api', 'fertilizer_model_v2.pkl'))
    joblib.dump(le_target, os.path.join('api', 'fertilizer_target_encoder_v2.pkl'))
    joblib.dump(feature_columns, os.path.join('api', 'fertilizer_features_v2.pkl'))
    
    print("\n🎉 Training complete! Model saved as fertilizer_model_v2.pkl")