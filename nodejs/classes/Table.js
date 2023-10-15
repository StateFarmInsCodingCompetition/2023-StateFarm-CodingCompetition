export class Table {
    /**
     * Constructor
     *
     * @param {string} tableDataPath - Path to get the data for this table
     */
    constructor(tableDataPath) {
        // The table object
        this.table = null;

        this.tableDataPath = tableDataPath;

        this.config = {
            rowHeaders: true,
            manualColumnResize: true,
            licenseKey: "non-commercial-and-evaluation",
            colHeaders: [],
            data: [],
            height: 350,
            data: [],
            contextMenu: true,
        };
        this.columnIds = [];
    }

    async #initTable() {
        // Reset colHeaders and data
        this.config.colHeaders = [];
        this.config.data = [];

        const rawData = await fetch("../data/" + this.tableDataPath);
        const data = JSON.parse(await rawData.text());

        // Set column headers.
        this.config.colHeaders = Object.keys(data[0]);

        // Insert data to table.
        data.forEach((row) => {
            this.config.data.push(Object.values(row));
        });

        if (this.table != null) {
            this.table.updateSettings({
                colHeaders: this.config.colHeaders,
                data: this.config.data,
            });
        }
    }

    /**
     * Displays this table.
     *
     * @param {HTMLElement} container The HTML div for this table
     */
    async display(container) {
        await this.#initTable();
        this.table = new Handsontable(container, this.config);
    }

    /**
     * Change the data of the table.
     * 
     * @param {string} newPath - The new path.
     */
    async setDataPath(newPath) {
        this.tableDataPath = newPath;
        await this.#initTable();
    }
}
