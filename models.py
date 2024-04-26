from pydantic import BaseModel


class Course(BaseModel):
    id: int
    name: str

class Discussion(BaseModel):
    id: int
    title: str
    user_name: str

class DiscussionEntry(BaseModel):
    message: str

class AssignmentGroup(BaseModel):
    id: int
    name: str

class Assignment(BaseModel):
    assignment_group_id: int
    id: int
    name: str

class AssignmentSubmission(BaseModel):
    submission_url: str
    submission_type: str
    comment: str