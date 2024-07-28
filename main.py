from src.data_collector import *

from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from apscheduler.schedulers.background import BackgroundScheduler

import uvicorn

app = FastAPI()
DB_NAME = './database/economic_articles.db'
TABLE_NAME = 'articles'

class NewsItem(BaseModel):
    title: str
    summary: str
    url: str
    type: str


@app.get("/news", response_model=List[NewsItem])
async def get_news():
    summarized_news = []

    _, row_datas = fetch_all_data_from_db(db_name = DB_NAME, table_name = TABLE_NAME)
    
    for row_data in row_datas:
        print(row_data[1])
        summarized_news.append(
            NewsItem(
                title= row_data[1],
                summary= row_data[4],
                url= row_data[3],
                type= row_data[2])
        )

    return JSONResponse(content=[item.dict() for item in summarized_news], headers={"Content-Type": "application/json; charset=utf-8"})



def main():
    # first
    collect_data()

    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_data, 'interval', seconds=600)  # 10초마다 collect_data 함수 실행
    scheduler.start()
    # 스케줄러가 실행 중에 예외가 발생하지 않도록 try-except 블록을 사용하세요.
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # 서버가 종료되면 스케줄러도 종료합니다.
        scheduler.shutdown()


if __name__ == "__main__":
    main()
