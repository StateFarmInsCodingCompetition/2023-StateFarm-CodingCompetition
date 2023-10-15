import { Table } from "./classes/Table.js";

const container = document.querySelector("#table");
const table = new Table("sfcc_2023_agents.json");
table.display(container);

document.getElementById("load-table").addEventListener("click", () => {
    const e = document.getElementById("table-select");
    const dataPath = e.value;
    table.setDataPath(dataPath);
});
