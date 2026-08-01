import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
from feature_extraction import extract_features

def main():
    print("=" * 60)
    print("CyberShield - ML Model Training (v3.0)")
    print("30 Advanced Features | Full Dataset | Target: 99% Accuracy")
    print("=" * 60)

    print("\n[1/6] Loading full dataset from archive...")
    df = pd.read_csv('archive/malicious_phish.csv')
    print(f"  Total rows loaded: {len(df)}")

    # Map labels: benign -> 0, everything else -> 1
    df['label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)
    print(f"  Benign (Safe) URLs  : {len(df[df['label'] == 0])}")
    print(f"  Malicious URLs      : {len(df[df['label'] == 1])}")

    print("\n[2/6] Creating balanced dataset (100,000 URLs)...")
    # Use 100k balanced dataset for best accuracy
    benign    = df[df['label'] == 0].sample(n=50000, random_state=42)
    malicious = df[df['label'] == 1].sample(n=50000, random_state=42)
    df_balanced = pd.concat([benign, malicious]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"  Final dataset size  : {len(df_balanced)} (50k benign + 50k malicious)")

    print("\n[3/6] Extracting 30 advanced features (please wait ~3 minutes)...")
    features_list = df_balanced['url'].apply(extract_features).tolist()
    X = pd.DataFrame(features_list)
    y = df_balanced['label']
    print(f"  Feature matrix shape: {X.shape}")
    print(f"  Features used       : {list(X.columns)}")

    print("\n[4/6] Splitting data (80% train / 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"  Training samples    : {len(X_train)}")
    print(f"  Testing samples     : {len(X_test)}")

    print("\n[5/6] Training Random Forest Classifier (300 trees)...")
    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n  *** Model Accuracy : {accuracy * 100:.2f}% ***")
    print("\n  Detailed Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe (0)', 'Phishing (1)']))

    print("  Feature Importance Ranking (Top 15):")
    importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': clf.feature_importances_
    }).sort_values('Importance', ascending=False).head(15)
    for _, row in importance.iterrows():
        bar = '#' * int(row['Importance'] * 60)
        print(f"    {row['Feature']:28s} {row['Importance']:.4f}  {bar}")

    print("\n[6/6] Saving model to random_forest_model.pkl...")
    joblib.dump(clf, 'random_forest_model.pkl')
    print("  Model saved successfully!")
    print("=" * 60)
    print(f"TRAINING COMPLETE! Accuracy: {accuracy * 100:.2f}%")
    print("=" * 60)

if __name__ == '__main__':
    main()
