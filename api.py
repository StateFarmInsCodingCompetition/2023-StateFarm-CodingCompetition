from fastapi import FastAPI
from simple_data_tool import SimpleDataTool

app = FastAPI()
controller = SimpleDataTool()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/agents")
def read_agents():
    return controller.get_agent_data()


@app.get("/claim-handlers")
def read_claim_handlers():
    return controller.get_claim_handler_data()


@app.get("/disasters")
def read_disasters():
    return controller.get_disaster_data()
