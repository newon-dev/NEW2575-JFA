from fastapi import FastAPI
from db import data_db
import time
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
	handlers=[
		RotatingFileHandler(
			"log.txt",
			maxBytes=1024*1024*1,
			backupCount=0
		)
	],
	level=logging.CRITICAL,
	format='%(asctime)s %(levelname)s %(message)s'
)

time.sleep(10)

db=data_db()

app = FastAPI()


def consulta_tag(tag):
    #retorna eixo e posicao
    result=db.execute_with_response(f'select eixo,posicao from tags where tag="{tag}"')
    if len(result)>0:
        return result[0]
    return 0




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/x/{data}")
def read_x(data):
    logging.critical(f'data x:{data}')
    x=consulta_tag(data)
    logging.critical(x)
    return 200

@app.get("/y/{data}")
def read_y(data):
    logging.critical(f'data y:{data}')
    return 200
