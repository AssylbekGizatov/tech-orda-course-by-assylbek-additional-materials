"""Complete local CLI baseline: train on local data, select threshold on validation, infer.

CPU only; no API, no external downloads, no unsafe deserialization.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

FEATURES = ['minutes_open', 'affected_users', 'category', 'channel']

def build_model():
    data_path = Path(__file__).resolve().parents[1] / 'datasets' / 'service_tickets.csv'
    df = pd.read_csv(data_path)
    train, valid = df.iloc[:360], df.iloc[360:480]
    preprocess = ColumnTransformer([
        ('num', StandardScaler(), ['minutes_open', 'affected_users']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category', 'channel']),
    ])
    model = Pipeline([('prepare', preprocess), ('model', LogisticRegression(C=1, max_iter=400, random_state=126))])
    model.fit(train[FEATURES], train.breach_sla)
    prob = model.predict_proba(valid[FEATURES])[:, 1]
    candidates = []
    for threshold in np.linspace(.05, .9, 18):
        _, fp, fn, _ = confusion_matrix(valid.breach_sla, prob >= threshold, labels=[0, 1]).ravel()
        candidates.append((int(5*fn + fp), float(threshold)))
    threshold = min(candidates)[1]
    return model, threshold

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minutes-open', type=int, required=True)
    parser.add_argument('--affected-users', type=int, required=True)
    parser.add_argument('--category', choices=['access', 'billing', 'schedule', 'other'], required=True)
    parser.add_argument('--channel', choices=['portal', 'chat', 'email'], required=True)
    args = parser.parse_args()
    if not 0 <= args.minutes_open <= 120 or not 1 <= args.affected_users <= 45:
        parser.error('Demo supports minutes-open 0..120 and affected-users 1..45, the training domain.')
    model, threshold = build_model()
    sample = pd.DataFrame([{'minutes_open': args.minutes_open, 'affected_users': args.affected_users,
                            'category': args.category, 'channel': args.channel}])
    probability = float(model.predict_proba(sample[FEATURES])[0, 1])
    print(json.dumps({'breach_risk': round(probability, 6), 'threshold': threshold,
                      'needs_review': probability >= threshold, 'mode': 'local_synthetic_baseline',
                      'disclaimer': 'Educational synthetic data; not validated for real helpdesk decisions.'},
                     ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
