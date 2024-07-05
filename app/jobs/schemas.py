from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    company: str
    location: str
    date_posted: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class Job(JobBase):
    id: int