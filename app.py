from flask import Flask, request, jsonify
from models import db, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'  # SQLite 資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 在第一次執行時建立資料庫
with app.app_context():
    db.create_all()

# ======================
# RESTful API
# ======================

# 1️⃣ 取得所有筆記
@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes])

# 2️⃣ 取得單一筆記
@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

# 3️⃣ 新增筆記
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(
        title=data['title'],
        author=data['author'],
        content=data['content']
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201

# 4️⃣ 更新筆記
@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    note = Note.query.get_or_404(note_id)
    note.title = data.get('title', note.title)
    note.author = data.get('author', note.author)
    note.content = data.get('content', note.content)
    db.session.commit()
    return jsonify(note.to_dict())

# 5️⃣ 刪除筆記
@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully."})

if __name__ == '__main__':
    app.run(debug=True)