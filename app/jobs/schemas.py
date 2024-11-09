from typing import Optional

from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    """
    Base model representing the core attributes of a job listing.

    Attributes:
        title (str): The job title.
        company (str): The name of the company offering the job.
        date_posted (Optional[str]): The date the job was posted, formatted as a string. Optional.
        url (str): The URL link to the job listing.
        location (str): The location where the job is based.

    Config:
        model_config: Configuration to allow attribute-based model creation.
    """
    title: str
    company: str
    date_posted: Optional[str]
    url: str
    location: str

    model_config = ConfigDict(from_attributes=True)


class JobCreate(JobBase):
    """
    Model for creating a new job listing. Inherits all attributes from JobBase.
    """
    pass


class Job(JobBase):
    """
    Model representing a job listing with an ID.

    Attributes:
        id (int): Unique identifier for the job listing.
    """
    id: int