# from app.routers import ...
from fastapi import FastAPI
from app.init_db import connect_db, init_db

app = FastAPI()

def main():
    init_db()
  


if __name__ == "__main__":
    main()
