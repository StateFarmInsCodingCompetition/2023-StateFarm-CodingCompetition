const SimpleDataTool = require("./simpleDataTool");

let controller;

beforeEach(() => {
    controller = new SimpleDataTool();
});

test("testLoadSimpleModels", async () => {
    const data = await controller.loadSimpleModels();
    expect(data).not.toBeNull();
    // other assertions based on your test requirements...
});
