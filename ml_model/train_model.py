import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from feature_extraction import extract_features

def main():
    print("Loading dataset from archive...")
    # Load dataset
    df = pd.read_csv('archive/malicious_phish.csv')
    
    # Map labels: 'benign' -> 0, everything else (phishing, malware, defacement) -> 1
    df['label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)
    
    # Sample the dataset to 20,000 rows to make training faster
    df = df.sample(n=20000, random_state=42)
    
    print("Extracting features (This might take a moment)...")
    # Extract features for each URL
    features_list = df['url'].apply(extract_features).tolist()
    
    # Convert list of dicts to DataFrame
    X = pd.DataFrame(features_list)
    y = df['label']
    
    print(f"Dataset shape: {X.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    # Train model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy * 100:.2f}%")
    
    print("Saving model to random_forest_model.pkl...")
    # Save model
    joblib.dump(clf, 'random_forest_model.pkl')
    print("Training complete and model saved.")

if __name__ == '__main__':
    main()
