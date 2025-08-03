from typing import List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl


class Branding(BaseModel):
    icon: str
    color: str


class InputItem(BaseModel):
    description: str
    required: bool
    default: Optional[str] = None


class OutputItem(BaseModel):
    description: str


class RunsUsingNode(BaseModel):
    using: Literal["node12", "node16", "node20"]
    main: str
    pre: Optional[str] = None
    post: Optional[str] = None


class RunsUsingDocker(BaseModel):
    using: Literal["docker"]
    image: str
    args: Optional[List[str]] = None
    entrypoint: Optional[Union[str, List[str]]] = None
    env: Optional[Dict[str, str]] = None


class RunsUsingComposite(BaseModel):
    using: Literal["composite"]
    steps: List[Dict[str, Any]]
    env: Optional[Dict[str, str]] = None
    shell: Optional[str] = None
    working-directory: Optional[str] = Field(None, alias="working-directory")


Runs = Union[RunsUsingNode, RunsUsingDocker, RunsUsingComposite]


class GitHubActionModel(BaseModel):
    name: str
    description: str
    author: Optional[str] = None
    branding: Optional[Branding] = None
    inputs: Optional[Dict[str, InputItem]] = None
    outputs: Optional[Dict[str, OutputItem]] = None
    runs: Runs
