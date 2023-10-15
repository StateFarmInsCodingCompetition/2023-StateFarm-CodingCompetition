import uvicorn
from fastapi import FastAPI, HTTPException
from simple_data_tool import SimpleDataTool
from models import Agents, Claims, Claim, ClaimHandlers, Disasters, Disaster, DisasterCount

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
