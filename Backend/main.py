from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from mongoengine import connect, disconnect
from models import Url as mongo_url_model
from pydantic import BaseModel
import random
import string
import hashlib
from dotenv import load_dotenv
import os


# Load variables from .env file
load_dotenv()


class Url(BaseModel):
    url: str


def generate_random_keyword(length):
    # Define the characters that can be used in the keyword (alphabets and digits)
    characters = string.ascii_letters + string.digits

    # Generate a random keyword of the specified length
    keyword = "".join(random.choice(characters) for _ in range(length))

    return keyword


app = FastAPI()

# app.mount("/Frontend", StaticFiles(directory="../Frontend"), name="Frontend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["POST", "GET"],
#     allow_headers=["*"],
# )


@app.on_event("startup")
async def startup():
    mongo_url = os.getenv("MONGO_URL")
    db = os.getenv("DB_NAME")

    # Connect to MongoDB
    connect(db=db, host=mongo_url)


@app.on_event("shutdown")
async def shutdown():
    # Close the MongoDB connection
    disconnect()


# Post request for shortened url
@app.post("/url")
def short_url(base_url: Url):
    url = base_url.url

    # check if url is there in database
    object = mongo_url_model.objects(base_url=url).first()

    if object:
        return f"{os.getenv('DOMAIN')}/{object.tiny_url}"

    # generate tiny_url

    hashed_url = url.encode("utf-8")
    tiny_url = hashlib.sha256(hashed_url).hexdigest()
    tiny_url = tiny_url[:10]

    # save to database
    mongo_save = mongo_url_model()
    mongo_save.tiny_url = tiny_url
    mongo_save.base_url = url
    mongo_save.save()

    return f"{os.getenv('DOMAIN')}/{tiny_url}"


@app.get("/{key}")
def redirect_url(key):
    # check if the value is there in mongodb
    object = mongo_url_model.objects(tiny_url=key).first()

    # REdirect with base_url if object is not none
    if object != None:
        return RedirectResponse(object.base_url)
    return "Url not found"


@app.get("/")
async def get_html_file():
    file_path = "../Frontend/index.html"
    return FileResponse(file_path, media_type="text/html")

if __name__ == "__main__":
    uvicorn.run(app)