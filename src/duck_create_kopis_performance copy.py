import duckdb, os
from configparser import ConfigParser

current_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(current_dir, f'../config/config.ini')
database_dir = os.path.join(current_dir, f'../database/kopis')

# config.ini 파일 읽기
parser = ConfigParser()
parser.read(config_dir)
s3_access = parser.get("AWS", "S3_ACCESS")
s3_secret = parser.get("AWS", "S3_SECRET")

# DuckDB에 연결
conn = duckdb.connect(database=database_dir, read_only=False)  

# 쿼리 실행
cursor = conn.cursor()

# 테이블 생성 : 2023년 1월, 서울
cursor.execute("""SELECT column_name
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE table_name = 'performance'""")
cursor.execute("DESCRIBE performance")
returned = cursor.fetchall()

column_list = [column[0] for column in returned]
print(column_list)

# 연결 종료
conn.close()