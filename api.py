from fastapi import FastAPI
from simple_data_tool import SimpleDataTool

app = FastAPI(title="StateFarm Round 1")
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


@app.get("/disasters/{disaster_id}")
def read_disaster(disaster_id: int):
    disasters = controller.get_disaster_data()
    for disaster in disasters:
        if disaster["id"] == disaster_id:
            return disaster
    return {"error": "Disaster not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010)
