import React, {useState} from "react";
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';
import '@mui/icons-material/';
import {get} from "../BackendLink";

const VISIBLE_FIELDS = ['name', 'rating', 'country', 'dateCreated', 'isAdmin'];

function CRM() {
    const [claimData, setClaimData] = useState(null);
    const [agentData, setAgentData] = useState(null);
    const [claimHandlerData, setClaimHandlerData] = useState(null);
    const [disasterData, setDiasterData] = useState(null);

    get('/get_agent_data', {}).then(async (response) => {
        let json = await response.json();
        setAgentData(json); // Trigger state set
    });

    get('/get_claim_data', {}).then(async (response) => {
        let json = await response.json();
        setClaimData(json); // Trigger state set
    });

    get('/get_claim_handler_data', {}).then(async (response) => {
        let json = await response.json();
        setClaimHandlerData(json); // Trigger state set
    });

    get('/get_disaster_data', {}).then(async (response) => {
        let json = await response.json();
        setDiasterData(json); // Trigger state set
    });

    let agentGridData = {
        columns: [{field: 'id', headerName: 'ID'},
            {field: 'first_name', headerName: 'First Name'},
            {field: 'last_name', headerName: 'Last Name'},
            {field: 'state', headerName: 'State'},
            {field: 'region', headerName: 'Region'},
            {field: 'primary_language', headerName: 'Primary Language'},
            {field: 'secondary_language', headerName: 'Secondary Language'},
            {field: 'years_active', headerName: 'Years Active'}
        ],
        rows: agentData
    }

    let claimGridData = {
        columns: [{field: 'agent_assigned_id', headerName: 'Agent ID'},
            {field: 'claim_handler_assigned_id', headerName: 'Claim ID'},
            {field: 'disaster_id', headerName: 'Disaster ID'},
            {field: 'estimate_cost', headerName: 'Estimate Cost'},
            {field: 'loss_of_life', headerName: 'Loss of Life'},
            {field: 'severity_rating', headerName: 'Severity'},
            {field: 'status', headerName: 'Status'},
            {field: 'total_loss', headerName: 'Total Loss'},
            {field: 'type', headerName: 'Type'}
        ],
        rows: claimData
    }


    let claimHandlerGridData = {
        columns: [{field: 'id', headerName: 'ID'},
            {field: 'first_name', headerName: 'First Name'},
            {field: 'last_name', headerName: 'Last Name'}
        ],
        rows: claimHandlerData
    }

    let disasterGridData = {
        columns: [{field: 'id', headerName: 'ID'},
            {field: 'type', headerName: 'Type'},
            {field: 'state', headerName: 'State'},
            {field: 'name', headerName: 'Name'},
            {field: 'description', headerName: 'Description'},
            {field: 'start_date', headerName: 'Start Date'},
            {field: 'end_date', headerName: 'End Date'},
            {field: 'declared_date', headerName: 'Declared Date'},
            {field: 'lat', headerName: 'Latitude'},
            {field: 'long', headerName: 'Longitude'},
            {field: 'radius_miles', headerName: 'Radius (Miles)'}
        ],
        rows: disasterData
    }


    return (
        <div className="content">
            <h2 className="pill">Agents</h2>
            <div style={{ height: 400, width: 'fit-content' }}>
                {agentData == null ? <h3>Loading...</h3> : <DataGrid {...agentGridData} slots={{ toolbar: GridToolbar }} />}
            </div><br/>

            <h2 className="pill">Claims</h2>
            <div style={{ height: 400, width: 'fit-content' }}>
                {claimData == null ? <h3>Loading...</h3> : <DataGrid {...claimGridData} slots={{ toolbar: GridToolbar }} />}
            </div><br/>

            <h2 className="pill">Claim Handlers</h2>
            <div style={{ height: 400, width: 'fit-content' }}>
                {claimHandlerData == null ? <h3>Loading...</h3> : <DataGrid {...claimHandlerGridData} slots={{ toolbar: GridToolbar }} />}
            </div><br/>

            <h2 className="pill">Disasters</h2>
            <div style={{ height: 400, width: 'fit-content' }}>
                {disasterData == null ? <h3>Loading...</h3> : <DataGrid {...disasterGridData} slots={{ toolbar: GridToolbar }} />}
            </div>
        </div>
    )
}

export default CRM;