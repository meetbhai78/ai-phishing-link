"""
CyberShield - ML Model Comprehensive Evaluation Script
Calculates: Accuracy, Precision, Recall, F1-Score, Confusion Matrix, Specificity, ROC-AUC
"""
import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)

# Ensure ml_model path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from feature_extraction import extract_features

def main():
    print("=" * 60)
    print("[EVAL] CYBERSHIELD ML MODEL EVALUATION (v3.0 - Random Forest)")
    print("=" * 60)

    model_path = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
    dataset_path = os.path.join(os.path.dirname(__file__), 'archive', 'malicious_phish.csv')

    print(f"Loading Model from: {model_path}")
    clf = joblib.load(model_path)
    print("Model loaded successfully!")

    print(f"Loading Dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Standardize labels
    if 'type' in df.columns:
        df['label'] = df['type'].apply(lambda x: 0 if str(x).lower() == 'benign' else 1)
    elif 'status' in df.columns:
        df['label'] = df['status'].apply(lambda x: 0 if str(x).lower() == 'legitimate' else 1)
    elif 'Result' in df.columns:
        df['label'] = df['Result'].apply(lambda x: 0 if x == -1 or x == 0 else 1)
    elif 'label' not in df.columns and 'phishing' in df.columns:
        df['label'] = df['phishing'].astype(int)

    # Sample 5,000 URLs for fast evaluation
    sample_df = df.sample(n=min(5000, len(df)), random_state=42).reset_index(drop=True)
    print(f"Evaluating on {len(sample_df)} test samples ({len(sample_df[sample_df['label']==0])} Safe, {len(sample_df[sample_df['label']==1])} Phishing)...")

    features_list = sample_df['url'].apply(extract_features).tolist()
    X_test = pd.DataFrame(features_list)
    y_test = sample_df['label']

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE METRICS:")
    print("=" * 60)
    print(f"  * Accuracy            : {acc * 100:.2f}%")
    print(f"  * Precision           : {prec * 100:.2f}%")
    print(f"  * Recall (Sensitivity): {rec * 100:.2f}%")
    print(f"  * Specificity         : {specificity * 100:.2f}%")
    print(f"  * F1-Score            : {f1 * 100:.2f}%")
    print(f"  * ROC-AUC Score       : {auc:.4f}")
    print("=" * 60)

    print("\nCONFUSION MATRIX:")
    print(f"  +---------------------+---------------------+")
    print(f"  | True Negative (TN)  | False Positive (FP) |")
    print(f"  | {tn:<19} | {fp:<19} |")
    print(f"  +---------------------+---------------------+")
    print(f"  | False Negative (FN) | True Positive (TP)  |")
    print(f"  | {fn:<19} | {tp:<19} |")
    print(f"  +---------------------+---------------------+")

    print("\nTOP 10 IMPORTANT FEATURES:")
    feat_importances = pd.DataFrame({
        'Feature': X_test.columns,
        'Importance': clf.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    for idx, row in feat_importances.iterrows():
        print(f"  - {row['Feature']:<25} : {row['Importance']:.4f}")
    print("=" * 60)

if __name__ == '__main__':
    main()
