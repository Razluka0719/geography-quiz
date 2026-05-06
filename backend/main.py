from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# フロントエンド（HTML）からの通信を許可する設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースの初期化
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id TEXT PRIMARY KEY,
            attempts INTEGER DEFAULT 0,
            corrects INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 通信データの構造定義
class AnswerUpdate(BaseModel):
    question_id: str
    is_correct: bool

# --- APIの処理 ---

@app.get("/")
def home():
    return {"status": "Running", "message": "地理クイズ統計サーバー稼働中"}

# 統計を取得する
@app.get("/stats/{q_id}")
def get_stats(q_id: str):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT attempts, corrects FROM stats WHERE id = ?", (q_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        attempts, corrects = row
        rate = int((corrects / attempts) * 100) if attempts > 0 else 0
        return {"attempts": attempts, "rate": rate}
    return {"attempts": 0, "rate": 0}

# 回答結果をDBに書き込む
@app.post("/update")
def update_stats(data: AnswerUpdate):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stats (id, attempts, corrects) VALUES (?, 1, ?)
        ON CONFLICT(id) DO UPDATE SET
            attempts = attempts + 1,
            corrects = corrects + (EXCLUDED.corrects)
    ''', (data.question_id, 1 if data.is_correct else 0))
    conn.commit()
    conn.close()
    return {"status": "updated"}