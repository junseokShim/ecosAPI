import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('./database/economic_articles.db')
    cursor = conn.cursor()

    # 테이블이 이미 존재하는지 확인
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='articles'
    ''')
    result = cursor.fetchone()

    if result is None:
        # 테이블이 존재하지 않으면 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME,
                title TEXT,
                type TEXT,
                link TEXT,
                summary TEXT
            )
        ''')
        print("Table 'articles' created.")
    else:
        print("Table 'articles' already exists.")
    
    conn.commit()
    conn.close()


def insert_article(title, article_type, link, summary):
    conn = sqlite3.connect('./database/economic_articles.db')
    cursor = conn.cursor()
    current_time = datetime.now()
    
    cursor.execute('''
        INSERT INTO articles (created_at, title, type, link, summary)
        VALUES (?, ?, ?, ?, ?)
    ''', (current_time, title, article_type, link, summary))

    conn.commit()
    conn.close()


def update_articles_sorted_by_date_desc():
    conn = sqlite3.connect('./database/economic_articles.db')
    cursor = conn.cursor()
    
    # 임시 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles_sorted (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME,
            title TEXT,
            type TEXT,
            link TEXT,
            summary TEXT
        )
    ''')
    
    # 데이터 정렬 및 임시 테이블에 삽입
    cursor.execute('''
        INSERT INTO articles_sorted (created_at, title, type, link, summary)
        SELECT created_at, title, type, link, summary FROM articles
        ORDER BY created_at DESC
    ''')
    
    # 원래 테이블 삭제
    cursor.execute('DROP TABLE articles')
    
    # 임시 테이블 이름 변경
    cursor.execute('ALTER TABLE articles_sorted RENAME TO articles')
    
    conn.commit()
    conn.close()



def fetch_data_from_db(db_name, table_name, query="SELECT *", columns=None):
    """
    데이터베이스에서 데이터를 조회하는 일반화된 함수.
    
    :param db_name: 데이터베이스 이름
    :param table_name: 테이블 이름
    :param query: 실행할 SQL 쿼리 (기본값: "SELECT *")
    :param columns: 조회할 열 이름의 리스트 (기본값: None, 모든 열 조회)
    :return: 열 이름과 데이터의 튜플
    """
    # 데이터베이스 연결
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 기본 쿼리 구성
    if columns:
        columns_str = ", ".join(columns)
    else:
        columns_str = "*"
    
    # SQL 쿼리 실행
    cursor.execute(f"{query} FROM {table_name}")
    
    # 열 이름 가져오기
    column_names = [description[0] for description in cursor.description]
    
    # 행 데이터 가져오기
    rows = cursor.fetchall()
    
    # 연결 종료
    conn.close()

    return column_names, rows


# 모든 데이터를 조회하는 예제
def fetch_all_data_from_db(db_name, table_name):
    return fetch_data_from_db(db_name, table_name)


# 타이틀만 조회하는 예제
def fetch_title_data_from_db(db_name, table_name):
    columns, rows = fetch_data_from_db(db_name, table_name, query="SELECT title")
    rows = [row[0] for row in rows]
    return columns, rows