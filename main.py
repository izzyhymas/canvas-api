import os

from models import Course, Discussion, DiscussionEntry

from dotenv import load_dotenv
import requests

from fastapi import FastAPI


load_dotenv()

app = FastAPI()

access_token = lambda: os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {
    "Authorization": f"Bearer {access_token()}"
}

@app.get("/courses")
async def get_courses() -> list[Course]:
    response = requests.get(url=f"{base_url}/courses", headers=headers)
    r_json = response.json()

    courses: list[Course] = []
    for course_json in r_json:
        course = Course(id=course_json["id"], name=course_json["name"])
        courses.append(course)    
    
    return courses

@app.get("/discussions")
async def get_discussions(course_id: int) -> list[Discussion]:
    response = requests.get(url=f"{base_url}/courses/{course_id}/discussion_topics", headers=headers)
    r_json = response.json()

    discussions: list[Course] = []
    for discussion_json in r_json:
        discussion = Discussion(id=discussion_json["id"], title=discussion_json["title"], user_name=discussion_json["user_name"])
        discussions.append(discussion)

    return discussions

@app.post("/discussions/entry")
async def post_discussion(course_id: int, topic_id: int, body: DiscussionEntry):
    response = requests.post(url=f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries", headers=headers, data=body.model_dump())
    r_json = response.json()
    return
