from pydantic import BaseModel


class Averages(BaseModel):
    average_claims_per_agent: float
    average_claims_per_handler: float
    average_claim_amount: float
    average_disaster_radius_miles: float
    average_disaster_length: float


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
