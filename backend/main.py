import uvicorn
from fastapi import FastAPI
from routers import posts, incomes

app = FastAPI()

app.include_router(posts.router, prefix="/post")
app.include_router(incomes.router)


if __name__ == '__main__':
    uvicorn.run(router, host="0.0.0.0", port=8000)