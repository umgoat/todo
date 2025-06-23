
import sqlite3
import os

DB_FILE = 'todo.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_task():
    description = input('할 일 내용: ').strip()
    if not description:
        print('할 일 내용을 입력하세요.')
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
    conn.commit()
    conn.close()
    print('할 일이 추가되었습니다.')

def list_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, done FROM tasks ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print('등록된 할 일이 없습니다.')
        return
    print('\n할 일 목록:')
    for row in rows:
        status = '✔' if row[2] else ' '
        print(f'[{row[0]}] [{status}] {row[1]}')
    print()

def complete_task():
    list_tasks()
    try:
        task_id = int(input('완료할 할 일 ID: ').strip())
    except ValueError:
        print('올바른 ID를 입력하세요.')
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
    if cursor.rowcount == 0:
        print('해당 ID의 할 일이 없습니다.')
    else:
        print('할 일이 완료 처리되었습니다.')
    conn.commit()
    conn.close()

def delete_task():
    list_tasks()
    try:
        task_id = int(input('삭제할 할 일 ID: ').strip())
    except ValueError:
        print('올바른 ID를 입력하세요.')
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    if cursor.rowcount == 0:
        print('해당 ID의 할 일이 없습니다.')
    else:
        print('할 일이 삭제되었습니다.')
    conn.commit()
    conn.close()

def main():
    init_db()
    while True:
        print('\n할 일(To-Do) 관리 프로그램')
        print('1. 할 일 추가')
        print('2. 할 일 목록 보기')
        print('3. 할 일 완료 처리')
        print('4. 할 일 삭제')
        print('5. 종료')
        choice = input('선택> ').strip()
        if choice == '1':
            add_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print('프로그램을 종료합니다.')
            break
        else:
            print('올바른 선택이 아닙니다.')

if __name__ == '__main__':
    main()
