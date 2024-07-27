import sqlite3

def create_database():
    conn = sqlite3.connect('./database/economic_articles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            type TEXT,
            link TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_article(title, article_type, link, summary):
    conn = sqlite3.connect('./database/economic_articles.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, type, link, summary)
        VALUES (?, ?, ?, ?)
    ''', (title, article_type, link, summary))
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