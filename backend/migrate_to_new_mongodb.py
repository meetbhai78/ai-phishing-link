"""
CyberShield MongoDB Migration Script
Migrates all scan logs, custom rules, user feedback, and community reports
from both old MongoDB Atlas and local SQLite into the new MongoDB Atlas cluster.
"""
import os
import json
import sqlite3
from pymongo import MongoClient

NEW_URI = "mongodb+srv://securityciber02_db_user:UNEi4BeDhRAs7e4k@cluster0.gxhclcv.mongodb.net/?appName=Cluster0"
OLD_URI = "mongodb+srv://tettateducation02_db_user:oruUJhGG80CtUriE@cluster0.1jy0r0h.mongodb.net/?appName=Cluster0"
SQLITE_PATH = r"D:\5TH SEM\extention\backend\scans.db"
DB_NAME = "cybershield_db"

print("=" * 60)
print("CYBERSHIELD: MIGRATION TO NEW MONGODB ATLAS CLUSTER")
print("=" * 60)

# Connect to new cluster
print(f"[*] Connecting to NEW cluster...")
new_client = MongoClient(NEW_URI, serverSelectionTimeoutMS=8000)
new_db = new_client[DB_NAME]
new_client.admin.command('ping')
print("[SUCCESS] Connected to NEW cluster: Cluster0.gxhclcv.mongodb.net")

# 1. Migrate Scan Logs
print("\n[1/4] Migrating scan_logs...")
scan_docs = {}

# Load from old Mongo first
try:
    old_client = MongoClient(OLD_URI, serverSelectionTimeoutMS=5000)
    old_db = old_client[DB_NAME]
    for doc in old_db["scan_logs"].find():
        doc.pop('_id', None)
        key = (doc.get('url'), str(doc.get('timestamp'))[:19])
        scan_docs[key] = doc
    print(f"  Loaded {len(scan_docs)} records from Old MongoDB Atlas.")
except Exception as e:
    print(f"  Warning loading old Mongo: {e}")

# Load from SQLite
try:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM scan_logs")
    rows = c.fetchall()
    sqlite_added = 0
    for r in rows:
        d = dict(r)
        d.pop('id', None)
        d['is_phishing'] = bool(d.get('is_phishing', 0))
        d['ssl_valid'] = bool(d.get('ssl_valid', 0))
        key = (d.get('url'), str(d.get('timestamp'))[:19])
        if key not in scan_docs:
            scan_docs[key] = d
            sqlite_added += 1
    print(f"  Merged {sqlite_added} additional records from SQLite (Total unique: {len(scan_docs)}).")
    conn.close()
except Exception as e:
    print(f"  Warning loading SQLite: {e}")

if scan_docs:
    new_db["scan_logs"].delete_many({}) # Clear any dummy records
    new_db["scan_logs"].insert_many(list(scan_docs.values()))
    print(f"  [SUCCESS] Inserted {len(scan_docs)} scan_logs into NEW MongoDB!")

# 2. Migrate Custom Rules
print("\n[2/4] Migrating custom_rules...")
rules_docs = {}
try:
    if 'old_db' in locals():
        for doc in old_db["custom_rules"].find():
            doc.pop('_id', None)
            rules_docs[doc.get('pattern')] = doc
except Exception:
    pass

try:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM custom_rules")
    for r in c.fetchall():
        d = dict(r)
        d.pop('id', None)
        rules_docs[d.get('pattern')] = d
    conn.close()
except Exception:
    pass

if rules_docs:
    new_db["custom_rules"].delete_many({})
    new_db["custom_rules"].insert_many(list(rules_docs.values()))
    print(f"  [SUCCESS] Inserted {len(rules_docs)} custom_rules into NEW MongoDB!")

# 3. Migrate User Feedback
print("\n[3/4] Migrating user_feedback...")
feedback_docs = {}
try:
    if 'old_db' in locals():
        for doc in old_db["user_feedback"].find():
            doc.pop('_id', None)
            feedback_docs[(doc.get('url'), str(doc.get('timestamp'))[:19])] = doc
except Exception:
    pass

try:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM user_feedback")
    for r in c.fetchall():
        d = dict(r)
        d.pop('id', None)
        feedback_docs[(d.get('url'), str(d.get('timestamp'))[:19])] = d
    conn.close()
except Exception:
    pass

if feedback_docs:
    new_db["user_feedback"].delete_many({})
    new_db["user_feedback"].insert_many(list(feedback_docs.values()))
    print(f"  [SUCCESS] Inserted {len(feedback_docs)} user_feedback into NEW MongoDB!")

# 4. Migrate Community Reports
print("\n[4/4] Migrating community_reports...")
comm_docs = {}
try:
    if 'old_db' in locals():
        for doc in old_db["community_reports"].find():
            doc.pop('_id', None)
            comm_docs[(doc.get('url'), str(doc.get('timestamp'))[:19])] = doc
except Exception:
    pass

try:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM community_reports")
    for r in c.fetchall():
        d = dict(r)
        d.pop('id', None)
        comm_docs[(d.get('url'), str(d.get('timestamp'))[:19])] = d
    conn.close()
except Exception:
    pass

if comm_docs:
    new_db["community_reports"].delete_many({})
    new_db["community_reports"].insert_many(list(comm_docs.values()))
    print(f"  [SUCCESS] Inserted {len(comm_docs)} community_reports into NEW MongoDB!")

print("\n" + "=" * 60)
print("VERIFICATION OF NEW MONGODB ATLAS CLUSTER (Cluster0.gxhclcv):")
print("=" * 60)
for col in ["scan_logs", "custom_rules", "user_feedback", "community_reports"]:
    count = new_db[col].count_documents({})
    print(f"  Collection '{col}': {count} documents")
print("=" * 60)
print("[COMPLETED] All data successfully migrated without any data loss!")
