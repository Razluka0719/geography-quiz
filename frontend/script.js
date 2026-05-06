// JSの正誤判定関数の追加部分

function checkAnswer(selected, btnElement) {
    const q = questions[currentIdx];
    let isCorrect = (selected === q.answer);

    // （画面を緑や赤にする処理は省略）

    // ★ サーバーに結果を送信する処理
    sendResultToServer(q.id, isCorrect);
}

// サーバーと通信する関数
async function sendResultToServer(questionId, isCorrect) {
    // PythonサーバーのURLへデータを送る
    await fetch('http://localhost:8000/update_stats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            question_id: questionId,
            is_correct: isCorrect
        })
    });
}