import uvicorn
from fastapi import FastAPI, HTTPException
from simple_data_tool import SimpleDataTool
from models import Agents, Claims, Claim, ClaimHandlers, Disasters, Disaster, DisasterCount, Averages
import pandas as pd

app = FastAPI(title="StateFarm Round 1")
controller = SimpleDataTool()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/agents", response_model=Agents)
def read_agents():
    agents = controller.get_agent_data()
    return Agents(agents=agents)


@app.get("/claims", response_model=Claims)
def read_claims():
    claims = controller.get_claim_data()
    return Claims(claims=claims)


@app.get("/claims/{claim_id}", response_model=Claim)
def read_claim(claim_id: int):
    claims = controller.get_claim_data()

    for claim in claims:
        if claim["id"] == claim_id:
            return Claim(**claim)

    raise HTTPException(status_code=404, detail=f"Claim with ID {claim_id} not found")


@app.get("/claim-handlers", response_model=ClaimHandlers)
def read_claim_handlers():
    claim_handlers = controller.get_claim_handler_data()
    return ClaimHandlers(claim_handlers=claim_handlers)


@app.get("/disasters", response_model=Disasters)
def read_disasters():
    disasters = controller.get_disaster_data()
    return Disasters(disasters=disasters)


@app.get("/disasters/{disaster_id}", response_model=Disaster)
def read_disaster(disaster_id: int):
    disasters = controller.get_disaster_data()

    for disaster in disasters:
        if disaster["id"] == disaster_id:
            return Disaster(**disaster)

    raise HTTPException(status_code=404, detail="Disaster not found")


@app.get("/disasters/state/{state}", response_model=DisasterCount)
async def get_disasters_for_state(state: str):
    try:
        num_disasters = controller.get_num_disasters_for_state(state)
        return DisasterCount(state=state, number_of_disasters=num_disasters)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"No data available for state: {state}")


@app.get('/averages', response_model=Averages)
async def get_averages():
    disaster_df = pd.DataFrame(controller.get_disaster_data())
    claim_df = pd.DataFrame(controller.get_claim_data())

    average_claims_per_agent = claim_df.groupby('agent_assigned_id').count().mean()['id']
    average_claims_per_handler = claim_df.groupby('claim_handler_assigned_id').count().mean()['id']
    average_claim_amount = claim_df['estimate_cost'].mean()
    average_disaster_radius_miles = disaster_df['radius_miles'].mean()

    disaster_df['start_date'] = pd.to_datetime(disaster_df['start_date'])
    disaster_df['end_date'] = pd.to_datetime(disaster_df['end_date'])

    disaster_df['disaster_length'] = (disaster_df['end_date'] - disaster_df['start_date']).dt.days
    average_disaster_length = disaster_df['disaster_length'].mean()

    return Averages(
        average_claims_per_agent=average_claims_per_agent,
        average_claims_per_handler=average_claims_per_handler,
        average_claim_amount=average_claim_amount,
        average_disaster_radius_miles=average_disaster_radius_miles,
        average_disaster_length=average_disaster_length
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
