from fastapi import FastAPI

app = FastAPI()

#async def root():
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/home")
def home():
    return {"message": "Home"}

@app.get("/home/{name}")
def read_name(name: str):
    return {'name' : name}

@app.get("/home_err/{name}")
def read_name_err(name: int):
    return {'name' : name}


@app.post("/")
def home_post(msg: str):
    return {"Hello" : "POST", "msg": msg}