export class ChartController {
    constructor() {
        this.config = {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "Number of Claims",
                        data: [],
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        };
    }

    /**
     * Load data for this chart.
     * Didn't have time to implement APIs,
     * so the code here is duplicated from simpleDataTool.js :(
     */
    async #loadData() {
        // Read disasters from json file.
        let rawData = await fetch("../data/sfcc_2023_disasters.json");
        const sfcc2023Disasters = JSON.parse(await rawData.text());

        // Map from months to number of claims.
        const monthsToClaims = new Map();

        sfcc2023Disasters.forEach((disaster) => {
            const date = new Date(disaster.declared_date);
            const declaredMonth = date.getFullYear() + "/" + (date.getMonth() + 1);
            this.#increaseValueForMap(monthsToClaims, declaredMonth, 1);
        });

        const sortedList = [...monthsToClaims.entries()].sort((a, b) => {
            if (a[0] > b[0]) {
                return 1;
            }
            return -1;
        });
        sortedList.forEach((point) => {
            this.config.data.labels.push(point[0]);
            this.config.data.datasets[0].data.push(point[1]);
        });
    }

    /**
     * Safely updates a map by adding val to m[key].
     * This code is duplicated from simpleDataTool.js,
     * since I didn't have enough time to implement Rest API to call from there.
     * 
     * @param {Map} m - The map to update.
     * @param {string} key - The key where value needs to be updated.
     * @param {int} val - The val to add to current value.
     */
    #increaseValueForMap(m, key, val = 1) {
        if (!m.has(key)) {
            m.set(key, val);
        } else {
            m.set(key, m.get(key) + val);
        }
    }

    /**
     * Display this chart.
     *
     * @param {HTMLElement} container The container to display to.
     */
    async display(container) {
        await this.#loadData();
        new Chart(container, this.config);
    }
}
