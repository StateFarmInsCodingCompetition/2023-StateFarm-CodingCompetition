const fs = require("fs").promises;

class SimpleDataTool {
    constructor() {
        this.simpleModels = [];
        this.JSON_FILENAME_SIMPLE = "simple.json";
    }

    async loadSimpleModels() {
        try {
            const jsonData = await fs.readFile(
                this.JSON_FILENAME_SIMPLE,
                "utf-8"
            );
            this.simpleModels = JSON.parse(jsonData);
            return this.simpleModels;
        } catch (err) {
            console.error("Error loading JSON:", err);
            return null;
        }
    }
}

module.exports = SimpleDataTool;
