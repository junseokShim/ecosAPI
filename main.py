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

REPORT_DB_NAME = './database/economic_reports.db'
REPORT_TABLE_NAME = 'report'

class NewsItem(BaseModel):
    title: str
    summary: str
    url: str
    type: str

class ReportItem(BaseModel):
    title: str
    report: str


@app.get("/news", response_model=List[NewsItem])
async def get_news():
    summarized_news = []

    _, row_datas = fetch_all_data_from_db(db_name = DB_NAME, table_name = TABLE_NAME)
    
    for row_data in row_datas:
        print(row_data[1])
        summarized_news.append(
            NewsItem(
                date = row_data[1],
                title= row_data[2],
                summary= row_data[5],
                url= row_data[4],
                type= row_data[3])
        )

    return JSONResponse(content=[item.dict() for item in summarized_news], headers={"Content-Type": "application/json; charset=utf-8"})


@app.get("/daily_reports", response_model=List[ReportItem])
async def get_daily_reports():
    reports = []

    _, row_datas = fetch_all_data_from_db(db_name = REPORT_DB_NAME, table_name = REPORT_TABLE_NAME)
    
    for row_data in row_datas:
        print(row_data[1])
        reports.append(
            ReportItem(
                title= row_data[1],
                report= row_data[2])
        )

    return JSONResponse(content=[item.dict() for item in reports], headers={"Content-Type": "application/json; charset=utf-8"})


def main():
    # first
    collect_data()
    #report_economic_news()
    

    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_data,     'interval', seconds=3600)       # 경제 뉴스 업데이트
    scheduler.add_job(report_economic_news, 'interval', seconds=21600)  # 경제 리포트 업데이트
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
