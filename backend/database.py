import os
import json
import sqlite3
import datetime
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("DB_NAME", "cybershield_db")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'scans.db')

# Global MongoDB references
mongo_client = None
mongo_db = None
mongo_collection = None
mongo_rules = None
mongo_feedback = None
mongo_community = None
is_mongo_connected = False

def init_sqlite():
    """Initializes SQLite local fallback tables if not exists."""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # Scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                is_phishing INTEGER NOT NULL,
                confidence REAL NOT NULL,
                risk_level TEXT NOT NULL,
                hybrid_score REAL,
                client_type TEXT DEFAULT 'extension',
                timestamp TEXT NOT NULL,
                brand_detected TEXT,
                scraped_title TEXT,
                threat_category TEXT DEFAULT 'Generic',
                ssl_valid INTEGER DEFAULT 0
            )
        ''')
        
        # Safe migration for existing DBs
        try:
            cursor.execute("ALTER TABLE scan_logs ADD COLUMN threat_category TEXT DEFAULT 'Generic'")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE scan_logs ADD COLUMN ssl_valid INTEGER DEFAULT 0")
        except Exception:
            pass

        # Custom Rules Table (Whitelist / Blacklist)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE NOT NULL,
                rule_type TEXT NOT NULL, -- 'whitelist' or 'blacklist'
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        ''')
        
        # User Feedback / False Positive Report Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                reported_label TEXT NOT NULL, -- 'safe' or 'phishing'
                user_comment TEXT DEFAULT '',
                timestamp TEXT NOT NULL,
                status TEXT DEFAULT 'pending_review'
            )
        ''')

        # Community Phishing Reports Table (v4.0 — AI Training Crowdsource)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                user_reported_label TEXT NOT NULL DEFAULT 'unsure',
                auto_scan_phishing INTEGER DEFAULT 0,
                auto_scan_confidence REAL DEFAULT 0.0,
                auto_scan_risk_level TEXT DEFAULT '',
                auto_scan_threat_category TEXT DEFAULT '',
                questions_answers TEXT DEFAULT '{}',
                source TEXT DEFAULT 'app',
                timestamp TEXT NOT NULL,
                status TEXT DEFAULT 'pending_review'
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[DB] SQLite database & custom_rules & user_feedback & community_reports initialized at {SQLITE_DB_PATH}")
    except Exception as e:
        print(f"[DB ERROR] SQLite init failed: {e}")

def init_db():
    """Initializes MongoDB Atlas connection or falls back to SQLite."""
    global mongo_client, mongo_db, mongo_collection, mongo_rules, mongo_feedback, mongo_community, is_mongo_connected
    init_sqlite()

    if MONGODB_URI:
        try:
            from pymongo import MongoClient
            mongo_client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            # Test ping
            mongo_client.admin.command('ping')
            mongo_db = mongo_client[DB_NAME]
            mongo_collection = mongo_db["scan_logs"]
            mongo_rules = mongo_db["custom_rules"]
            mongo_feedback = mongo_db["user_feedback"]
            mongo_community = mongo_db["community_reports"]
            is_mongo_connected = True
            print(f"[DB SUCCESS] Connected to MongoDB Atlas: Cluster0 / {DB_NAME}")
        except Exception as e:
            is_mongo_connected = False
            print(f"[DB WARNING] MongoDB Atlas connection failed ({e}). Falling back to SQLite local database.")
    else:
        print("[DB] No MONGODB_URI specified. Operating with SQLite local database.")

# Auto-initialize upon import
init_db()

def log_scan(scan_data: dict) -> dict:
    """Logs a scan record to MongoDB Atlas and/or SQLite."""
    global is_mongo_connected, mongo_collection
    
    timestamp = scan_data.get("timestamp") or datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    record = {
        "url": scan_data.get("url", ""),
        "is_phishing": bool(scan_data.get("is_phishing", False)),
        "confidence": float(scan_data.get("confidence", 0.0)),
        "risk_level": scan_data.get("risk_level", "SAFE"),
        "hybrid_score": float(scan_data.get("hybrid_score", 0.0)),
        "client_type": scan_data.get("client_type", "extension"),
        "timestamp": timestamp,
        "brand_detected": scan_data.get("brand_detected", ""),
        "scraped_title": scan_data.get("scraped_title", ""),
        "threat_category": scan_data.get("threat_category", "Legitimate / Clean" if not scan_data.get("is_phishing") else "Generic Suspicious"),
        "ssl_valid": 1 if scan_data.get("ssl_valid") else 0
    }

    # 1. Try writing to MongoDB Atlas
    if is_mongo_connected and mongo_collection is not None:
        try:
            res = mongo_collection.insert_one(dict(record))
            record["_id"] = str(res.inserted_id)
        except Exception as e:
            print(f"[DB ERROR] MongoDB insert failed: {e}")

    # 2. Always backup / write to SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scan_logs (url, is_phishing, confidence, risk_level, hybrid_score, client_type, timestamp, brand_detected, scraped_title, threat_category, ssl_valid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record["url"],
            1 if record["is_phishing"] else 0,
            record["confidence"],
            record["risk_level"],
            record["hybrid_score"],
            record["client_type"],
            record["timestamp"],
            record["brand_detected"],
            record["scraped_title"],
            record["threat_category"],
            record["ssl_valid"]
        ))
        conn.commit()
        record["sqlite_id"] = cursor.lastrowid
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] SQLite insert failed: {e}")

    return record

def get_stats() -> dict:
    """Calculates live analytics from MongoDB Atlas or SQLite."""
    global is_mongo_connected, mongo_collection

    if is_mongo_connected and mongo_collection is not None:
        try:
            total_scans = mongo_collection.count_documents({})
            phishing_count = mongo_collection.count_documents({"is_phishing": True})
            safe_count = total_scans - phishing_count
            
            # Today's scans
            today_start = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            today_scans = mongo_collection.count_documents({"timestamp": {"$regex": f"^{today_start}"}})
            
            # Avg confidence
            pipeline = [{"$group": {"_id": None, "avg_conf": {"$avg": "$confidence"}}}]
            res = list(mongo_collection.aggregate(pipeline))
            avg_confidence = round(res[0]["avg_conf"], 1) if res and res[0].get("avg_conf") else 0.0

            return {
                "database_mode": "MongoDB Atlas",
                "total_scans": total_scans,
                "phishing_detected": phishing_count,
                "safe_sites": safe_count,
                "today_scans": today_scans,
                "avg_confidence": avg_confidence,
                "phishing_rate": round((phishing_count / total_scans * 100), 1) if total_scans > 0 else 0.0
            }
        except Exception as e:
            print(f"[DB WARNING] MongoDB stats query failed: {e}. Falling back to SQLite.")

    # SQLite Stats
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM scan_logs")
        total_scans = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE is_phishing = 1")
        phishing_count = cursor.fetchone()[0]
        safe_count = total_scans - phishing_count

        today_start = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE timestamp LIKE ?", (f"{today_start}%",))
        today_scans = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(confidence) FROM scan_logs")
        avg_row = cursor.fetchone()[0]
        avg_confidence = round(avg_row, 1) if avg_row else 0.0

        conn.close()
        return {
            "database_mode": "SQLite (Local Dual Mode)",
            "total_scans": total_scans,
            "phishing_detected": phishing_count,
            "safe_sites": safe_count,
            "today_scans": today_scans,
            "avg_confidence": avg_confidence,
            "phishing_rate": round((phishing_count / total_scans * 100), 1) if total_scans > 0 else 0.0
        }
    except Exception as e:
        print(f"[DB ERROR] SQLite stats failed: {e}")
        return {
            "database_mode": "Error",
            "total_scans": 0,
            "phishing_detected": 0,
            "safe_sites": 0,
            "today_scans": 0,
            "avg_confidence": 0.0,
            "phishing_rate": 0.0
        }

def get_recent_scans(limit: int = 100) -> list:
    """Retrieves recent scans from MongoDB or SQLite."""
    global is_mongo_connected, mongo_collection

    if is_mongo_connected and mongo_collection is not None:
        try:
            cursor = mongo_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"[DB WARNING] MongoDB get_recent_scans failed: {e}")

    # SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, url, is_phishing, confidence, risk_level, hybrid_score, client_type, timestamp, brand_detected, scraped_title, threat_category, ssl_valid
            FROM scan_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        scans = []
        for r in rows:
            scans.append({
                "id": r["id"],
                "url": r["url"],
                "is_phishing": bool(r["is_phishing"]),
                "confidence": r["confidence"],
                "risk_level": r["risk_level"],
                "hybrid_score": r["hybrid_score"],
                "client_type": r["client_type"],
                "timestamp": r["timestamp"],
                "brand_detected": r["brand_detected"],
                "scraped_title": r["scraped_title"],
                "threat_category": r["threat_category"] if "threat_category" in r.keys() else "Generic",
                "ssl_valid": bool(r["ssl_valid"]) if "ssl_valid" in r.keys() else False
            })
        conn.close()
        return scans
    except Exception as e:
        print(f"[DB ERROR] SQLite get_recent_scans failed: {e}")
        return []

def clear_scans() -> bool:
    """Clears all scan history."""
    global is_mongo_connected, mongo_collection
    if is_mongo_connected and mongo_collection is not None:
        try:
            mongo_collection.delete_many({})
        except Exception as e:
            print(f"[DB ERROR] MongoDB clear failed: {e}")
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_logs")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] SQLite clear failed: {e}")
        return False

# ===================================================
# Custom Whitelist / Blacklist Rule Management
# ===================================================
def get_custom_rules() -> list:
    """Returns all custom domain rules."""
    global is_mongo_connected, mongo_rules
    if is_mongo_connected and mongo_rules is not None:
        try:
            cursor = mongo_rules.find({}, {"_id": 0}).sort("created_at", -1)
            return list(cursor)
        except Exception as e:
            print(f"[DB WARNING] MongoDB get_custom_rules failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, domain, rule_type, notes, created_at FROM custom_rules ORDER BY id DESC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB ERROR] SQLite get_custom_rules failed: {e}")
        return []

def add_custom_rule(domain: str, rule_type: str, notes: str = "") -> dict:
    """Adds a domain to whitelist or blacklist."""
    global is_mongo_connected, mongo_rules
    domain = domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    rule_type = rule_type.strip().lower()
    if rule_type not in ["whitelist", "blacklist"]:
        rule_type = "blacklist"
    
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {
        "domain": domain,
        "rule_type": rule_type,
        "notes": notes,
        "created_at": created_at
    }

    if is_mongo_connected and mongo_rules is not None:
        try:
            mongo_rules.update_one({"domain": domain}, {"$set": record}, upsert=True)
        except Exception as e:
            print(f"[DB ERROR] MongoDB add_custom_rule failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO custom_rules (domain, rule_type, notes, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(domain) DO UPDATE SET rule_type=excluded.rule_type, notes=excluded.notes
        """, (domain, rule_type, notes, created_at))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] SQLite add_custom_rule failed: {e}")

    return record

def delete_custom_rule(domain: str) -> bool:
    """Deletes a custom domain rule."""
    global is_mongo_connected, mongo_rules
    domain = domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]

    if is_mongo_connected and mongo_rules is not None:
        try:
            mongo_rules.delete_one({"domain": domain})
        except Exception as e:
            print(f"[DB ERROR] MongoDB delete_custom_rule failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM custom_rules WHERE domain = ?", (domain,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] SQLite delete_custom_rule failed: {e}")
        return False

def add_user_feedback(url: str, reported_label: str, user_comment: str = "") -> dict:
    """Logs user false-positive / false-negative feedback for retraining."""
    global is_mongo_connected, mongo_feedback
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = {
        "url": url.strip(),
        "reported_label": reported_label.strip().lower(),
        "user_comment": user_comment.strip(),
        "timestamp": timestamp,
        "status": "pending_review"
    }

    if is_mongo_connected and mongo_feedback is not None:
        try:
            res = mongo_feedback.insert_one(dict(record))
            record["_id"] = str(res.inserted_id)
        except Exception as e:
            print(f"[DB ERROR] MongoDB feedback insert failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_feedback (url, reported_label, user_comment, timestamp, status)
            VALUES (?, ?, ?, ?, ?)
        """, (record["url"], record["reported_label"], record["user_comment"], record["timestamp"], record["status"]))
        conn.commit()
        record["id"] = cursor.lastrowid
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] SQLite feedback insert failed: {e}")

    return record

def get_user_feedback(limit: int = 50) -> list:
    """Retrieves recent user feedback reports."""
    global is_mongo_connected, mongo_feedback
    if is_mongo_connected and mongo_feedback is not None:
        try:
            cursor = mongo_feedback.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"[DB WARNING] MongoDB get_feedback failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, reported_label, user_comment, timestamp, status FROM user_feedback ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB ERROR] SQLite get_feedback failed: {e}")
        return []

# ===================================================
# Community Phishing Reports — v4.0 Crowdsource AI Training
# ===================================================
def add_community_report(report_data: dict) -> dict:
    """Logs a community phishing report with user answers for AI retraining."""
    global is_mongo_connected, mongo_community
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    record = {
        "url": report_data.get("url", "").strip(),
        "user_reported_label": report_data.get("user_reported_label", "unsure").strip().lower(),
        "auto_scan_phishing": 1 if report_data.get("auto_scan_phishing") else 0,
        "auto_scan_confidence": float(report_data.get("auto_scan_confidence", 0.0)),
        "auto_scan_risk_level": report_data.get("auto_scan_risk_level", ""),
        "auto_scan_threat_category": report_data.get("auto_scan_threat_category", ""),
        "questions_answers": json.dumps(report_data.get("questions_answers", {})),
        "source": report_data.get("source", "app"),
        "timestamp": timestamp,
        "status": "pending_review"
    }

    # MongoDB
    if is_mongo_connected and mongo_community is not None:
        try:
            mongo_record = dict(record)
            mongo_record["questions_answers"] = report_data.get("questions_answers", {})
            res = mongo_community.insert_one(mongo_record)
            record["_id"] = str(res.inserted_id)
        except Exception as e:
            print(f"[DB ERROR] MongoDB community report insert failed: {e}")

    # SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO community_reports (url, user_reported_label, auto_scan_phishing, auto_scan_confidence,
                auto_scan_risk_level, auto_scan_threat_category, questions_answers, source, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record["url"], record["user_reported_label"], record["auto_scan_phishing"],
            record["auto_scan_confidence"], record["auto_scan_risk_level"],
            record["auto_scan_threat_category"], record["questions_answers"],
            record["source"], record["timestamp"], record["status"]
        ))
        conn.commit()
        record["id"] = cursor.lastrowid
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] SQLite community report insert failed: {e}")

    return record

def get_community_reports(limit: int = 50) -> list:
    """Retrieves recent community phishing reports."""
    global is_mongo_connected, mongo_community
    if is_mongo_connected and mongo_community is not None:
        try:
            cursor = mongo_community.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"[DB WARNING] MongoDB get_community_reports failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, url, user_reported_label, auto_scan_phishing, auto_scan_confidence,
                   auto_scan_risk_level, auto_scan_threat_category, questions_answers,
                   source, timestamp, status
            FROM community_reports ORDER BY id DESC LIMIT ?
        """, (limit,))
        rows = []
        for r in cursor.fetchall():
            row = dict(r)
            try:
                row["questions_answers"] = json.loads(row.get("questions_answers", "{}"))
            except Exception:
                row["questions_answers"] = {}
            row["auto_scan_phishing"] = bool(row.get("auto_scan_phishing", 0))
            rows.append(row)
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB ERROR] SQLite get_community_reports failed: {e}")
        return []

def get_community_stats() -> dict:
    """Returns community contribution statistics."""
    global is_mongo_connected, mongo_community

    if is_mongo_connected and mongo_community is not None:
        try:
            total = mongo_community.count_documents({})
            phishing_reports = mongo_community.count_documents({"user_reported_label": "phishing"})
            safe_reports = mongo_community.count_documents({"user_reported_label": "safe"})
            unsure_reports = mongo_community.count_documents({"user_reported_label": "unsure"})
            from_app = mongo_community.count_documents({"source": "app"})
            from_ext = mongo_community.count_documents({"source": "extension"})
            return {
                "total_reports": total,
                "phishing_reports": phishing_reports,
                "safe_reports": safe_reports,
                "unsure_reports": unsure_reports,
                "from_app": from_app,
                "from_extension": from_ext,
                "community_active": total > 0
            }
        except Exception as e:
            print(f"[DB WARNING] MongoDB community stats failed: {e}")

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM community_reports")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM community_reports WHERE user_reported_label = 'phishing'")
        phishing_reports = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM community_reports WHERE user_reported_label = 'safe'")
        safe_reports = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM community_reports WHERE user_reported_label = 'unsure'")
        unsure_reports = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM community_reports WHERE source = 'app'")
        from_app = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM community_reports WHERE source = 'extension'")
        from_ext = cursor.fetchone()[0]
        conn.close()
        return {
            "total_reports": total,
            "phishing_reports": phishing_reports,
            "safe_reports": safe_reports,
            "unsure_reports": unsure_reports,
            "from_app": from_app,
            "from_extension": from_ext,
            "community_active": total > 0
        }
    except Exception as e:
        print(f"[DB ERROR] SQLite community stats failed: {e}")
        return {
            "total_reports": 0, "phishing_reports": 0, "safe_reports": 0,
            "unsure_reports": 0, "from_app": 0, "from_extension": 0,
            "community_active": False
        }

