from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    company: str
    date_posted: str
    url: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int