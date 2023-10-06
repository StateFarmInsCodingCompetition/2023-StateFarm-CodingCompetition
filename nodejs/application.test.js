const SimpleDataTool = require("./simpleDataTool");

let controller;

beforeEach(() => {
    controller = new SimpleDataTool();
});

test("testLoadSimpleModels", async () => {
    const data = await controller.loadSimpleModels();
    expect(data).not.toBeNull();
    expect(data.length).toBe(1);

    const model1 = data[0];

    expect(model1).not.toBeNull();
    expect(model1.name).toBe("John Smith");
    expect(model1.integer).toBe(1);
    expect(model1.decimal).toBe(1.99);
});
