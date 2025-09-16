from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import sqlite3
import re
from datetime import datetime
from typing import Dict, Optional

app = FastAPI(title="Log Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            level TEXT,
            message TEXT,
            user_id TEXT,
            request_id TEXT,
            session_id TEXT,
            raw_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class LogParser:
    def __init__(self):
        self.patterns = {
            'timestamp': r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            'level': r'(ERROR|WARN|INFO|DEBUG|FATAL)',
            'user_id': r'user[_-]?id[=:]\s*(\w+)',
            'request_id': r'request[_-]?id[=:]\s*([\w-]+)',
            'session_id': r'session[_-]?id[=:]\s*([\w-]+)'
        }
    
    def parse_line(self, line: str) -> Optional[Dict]:
        try:
            parsed = {
                'timestamp': None,
                'level': None,
                'message': line.strip(),
                'user_id': None,
                'request_id': None,
                'session_id': None,
                'raw_text': line
            }
            
            time_match = re.search(self.patterns['timestamp'], line)
            if time_match:
                try:
                    parsed['timestamp'] = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            level_match = re.search(self.patterns['level'], line)
            if level_match:
                parsed['level'] = level_match.group(1)
            
            for field in ['user_id', 'request_id', 'session_id']:
                match = re.search(self.patterns[field], line, re.IGNORECASE)
                if match:
                    parsed[field] = match.group(1)
            
            return parsed
        except Exception as e:
            print(f"Parse error: {e}")
            return None

@app.post("/upload-logs/")
async def upload_logs(file: UploadFile = File(...)):
    try:
        parser = LogParser()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        content = await file.read()
        lines = content.decode('utf-8').split('\n')
        
        batch = []
        for line in lines:
            if line.strip():
                parsed = parser.parse_line(line)
                if parsed:
                    batch.append((
                        parsed['timestamp'],
                        parsed['level'],
                        parsed['message'],
                        parsed['user_id'],
                        parsed['request_id'],
                        parsed['session_id'],
                        parsed['raw_text']
                    ))
        
        cursor.executemany('''
            INSERT INTO log_entries (timestamp, level, message, user_id, request_id, session_id, raw_text)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', batch)
        
        conn.commit()
        conn.close()
        
        return JSONResponse({"status": "success", "message": f"Processed {len(batch)} logs"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/error-stats/")
async def get_error_stats(hours: int = 24):
    try:
        conn = sqlite3.connect(DB_PATH)
        query = """
            SELECT level, COUNT(*) as count, 
                   GROUP_CONCAT(DISTINCT user_id) as user_ids,
                   GROUP_CONCAT(DISTINCT request_id) as request_ids
            FROM log_entries 
            WHERE timestamp >= datetime('now', ?)
            GROUP BY level
            ORDER BY count DESC
        """
        
        cursor = conn.cursor()
        cursor.execute(query, [f"-{hours} hours"])
        results = cursor.fetchall()
        conn.close()
        
        stats = []
        for level, count, user_ids, request_ids in results:
            stats.append({
                "level": level,
                "count": count,
                "user_ids": user_ids.split(',') if user_ids else [],
                "request_ids": request_ids.split(',') if request_ids else []
            })
        
        return JSONResponse({"stats": stats})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/")
async def search_logs(query: str = "", limit: int = 50):
    try:
        conn = sqlite3.connect(DB_PATH)
        
        if query:
            search_query = """
                SELECT * FROM log_entries 
                WHERE raw_text LIKE ? OR user_id LIKE ? OR request_id LIKE ?
                ORDER BY timestamp DESC LIMIT ?
            """
            cursor = conn.cursor()
            cursor.execute(search_query, [f"%{query}%", f"%{query}%", f"%{query}%", limit])
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM log_entries ORDER BY timestamp DESC LIMIT ?", [limit])
        
        results = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in results:
            logs.append({
                "id": row[0],
                "timestamp": row[1],
                "level": row[2],
                "message": row[3],
                "user_id": row[4],
                "request_id": row[5],
                "session_id": row[6],
                "raw_text": row[7]
            })
        
        return JSONResponse({"logs": logs, "count": len(logs)})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
