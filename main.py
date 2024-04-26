import os

from models import Course, Discussion, DiscussionEntry, AssignmentGroup, Assignment, AssignmentSubmission

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

@app.get("/courses/{course_id}/assignment_groups")
async def get_assignment_groups(course_id: int):
    response = requests.get(url=f"{base_url}/courses/{course_id}/assignment_groups?per_page=100", headers=headers)
    r_json = response.json()
    print()

    assignment_groups: list[AssignmentGroup] = []
    for assignment_group_json in r_json:
        assignment_group = AssignmentGroup(id=assignment_group_json["id"], name=assignment_group_json["name"])
        assignment_groups.append(assignment_group)
        return r_json

    return assignment_groups

@app.get("/courses/{course_id}/assignment_groups/{assignment_group_id}/assignments")
async def get_assignment(course_id: int, assignment_group_id: str) -> list[Assignment]:
    response = requests.get(url=f"{base_url}/courses/{course_id}/assignment_groups/{assignment_group_id}/assignments", headers=headers)
    r_json = response.json()
    print()

    assignments: list[Assignment] = []
    for assignment_json in r_json:
        assignment = Assignment(assignment_group_id=assignment_json["assignment_group_id"], id=assignment_json["id"], name=assignment_json["name"])
        assignments.append(assignment)
        print()

    return assignments

import json

@app.post("/courses/{course_id}/assignments/{assignment_id}/submissions")
async def submit_assignment(course_id: int, assignment_group_id: int, assignment_id: int, submission: AssignmentSubmission):
    submission_body: dict[str, str] = {
        "submission[url]": submission.submission_url,
        "submission[submission_type]": submission.submission_type,
        "comment[text_comment]": submission.comment,
    }

    response = requests.post(url=f"{base_url}/courses/{course_id}/assignments/{assignment_id}/submissions", headers=headers, data=submission_body)
    r_json = response.json()
    print(r_json)
