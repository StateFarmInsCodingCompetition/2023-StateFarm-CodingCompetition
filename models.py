from pydantic import BaseModel


class Agent(BaseModel):
    id: int
    name: str


class Claim(BaseModel):
    id: int
    title: str


class ClaimHandler(BaseModel):
    id: int
    name: str


class Disaster(BaseModel):
    id: int
    type: str


class DisasterCount(BaseModel):
    state: str
    number_of_disasters: int


class Agents(BaseModel):
    agents: list[Agent]


class Claims(BaseModel):
    claims: list[Claim]


class ClaimHandlers(BaseModel):
    claim_handlers: list[ClaimHandler]


class Disasters(BaseModel):
    disasters: list[Disaster]
