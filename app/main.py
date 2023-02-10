import uvicorn

from app.myapp import get_application

# 不一定非要用app, 可以用其他名字
app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
