from pydantic import BaseModel
from datetime import date

class Averages(BaseModel):
    average_claims_per_agent: float
    average_claims_per_handler: float
    average_claim_amount: float
    average_disaster_radius_miles: float
    average_disaster_length: float


class Agent(BaseModel):
    id: int
    first_name: str
    last_name: str
    state: str
    region: str
    primary_language: str
    secondary_language: str
    years_active: int


class Claim(BaseModel):
    id: int
    disaster_id: int
    status: str
    total_loss: bool
    loss_of_life: bool
    type: str
    severity_rating: int
    estimate_cost: float
    agent_assigned_id: int
    claim_handler_assigned_id: int


class ClaimHandler(BaseModel):
    id: int
    first_name: str
    last_name: str

class Disaster(BaseModel):
    id: int
    type: str
    state: str
    name: str
    description: str
    start_date: date
    end_date: date
    declared_date: date
    lat: float
    long: float
    radius_miles: int


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
