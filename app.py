from flask import Flask, request, jsonify
import MySQLdb
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)


db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="Nimabachi8787",
    db="task_manager",
    charset="utf8"
)


@app.route('/')
def home():
    return "Flask and MySQL are connected!"


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_title = data.get('title')
    due_date = data.get('due_date')

    
    if due_date and datetime.strptime(due_date, '%Y-%m-%d') < datetime.now():
        return jsonify({'error': '截止日期不能早於當前時間'}), 400

    
    if not task_title or not task_title[0].isalnum():
        return jsonify({'error': '任務名稱的第一個字必須是數字、字母或中文字'}), 400

    try:
        with db.cursor() as cursor:
            
            cursor.execute("SELECT * FROM tasks WHERE title = %s", (task_title,))
            if cursor.fetchone():
                return jsonify({'error': '任務名稱已存在'}), 400

            
            query = "INSERT INTO tasks (title, summary, description, due_date, priority, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (task_title, data.get('summary'), data.get('description'), due_date, data.get('priority')))
            db.commit()

        return jsonify({'message': '任務新增成功'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        with db.cursor() as cursor:
            
            query = """
                SELECT id, title, summary, description, due_date, priority, created_at, updated_at 
                FROM tasks
            """
            cursor.execute(query)
            tasks = cursor.fetchall()

           
            results = []
            for task in tasks:
                results.append({
                    'id': task[0],
                    'title': task[1],
                    'summary': task[2],
                    'description': task[3],
                    'due_date': str(task[4]) if task[4] else None,
                    'priority': task[5],
                    'created_at': str(task[6]) if task[6] else None,
                    'updated_at': str(task[7]) if task[7] else None
                })

            return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/delete', methods=['DELETE'])
def delete_task_by_title():
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({'error': '請提供任務名稱'}), 400

    try:
        with db.cursor() as cursor:
           
            query = "DELETE FROM tasks WHERE title = %s"
            cursor.execute(query, (title,))
            db.commit()

            if cursor.rowcount == 0:
                return jsonify({'error': 'Task not found'}), 404

        return jsonify({'message': '刪除成功!'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/update', methods=['PUT'])
def update_task():
    data = request.get_json()
    old_title = data.get('old_title')
    new_title = data.get('title')
    new_due_date = data.get('due_date')
    new_priority = data.get('priority')

    
    if not old_title:
        return jsonify({'error': '請選擇一個任務進行更新'}), 400

  
    if new_due_date and datetime.strptime(new_due_date, '%Y-%m-%d') < datetime.now():
        return jsonify({'error': '截止日期不能早於當前時間'}), 400

 
    if new_title and not new_title[0].isalnum():
        return jsonify({'error': '任務名稱的第一個字必須是數字、字母或中文字'}), 400

    try:
        with db.cursor() as cursor:
            
            if new_title:
                cursor.execute("SELECT * FROM tasks WHERE title = %s AND title != %s", (new_title, old_title))
                if cursor.fetchone():
                    return jsonify({'error': '新的任務名稱已存在'}), 400

          
            if new_priority is None or new_priority == "":
                cursor.execute("SELECT priority FROM tasks WHERE title = %s", (old_title,))
                result = cursor.fetchone()
                new_priority = result[0] if result else None

        
            query = """
                UPDATE tasks
                SET title = %s, summary = %s, description = %s, due_date = %s, priority = %s, updated_at = NOW()
                WHERE title = %s
            """
            cursor.execute(query, (new_title or old_title, data.get('summary'), data.get('description'), new_due_date, new_priority, old_title))
            db.commit()

        return jsonify({'message': '任務更新成功'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<title>', methods=['GET'])
def get_task_details(title):
    if not title:
        return jsonify({'error': '請提供任務名稱'}), 400

    try:
        with db.cursor() as cursor:
            query = "SELECT title, summary, description, due_date, priority FROM tasks WHERE title = %s"
            cursor.execute(query, (title,))
            task = cursor.fetchone()

            if not task:
                return jsonify({'error': '找不到該任務'}), 404

            return jsonify({
                'title': task[0],
                'summary': task[1],
                'description': task[2],
                'due_date': str(task[3]),
                'priority': task[4]
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
