import uvicorn

from app.conf.settings import settings
from app.myapp import get_application

# 不一定非要用app, 可以用其他名字
app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True, debug=settings.DEBUG)
