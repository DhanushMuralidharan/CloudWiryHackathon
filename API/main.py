from config import app,db
print("The API Server is running!")


@app.get("/")
async def root():
    return {"message": "Hello World"}