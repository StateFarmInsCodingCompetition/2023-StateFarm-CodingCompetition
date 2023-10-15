const SimpleDataTool = require("../simpleDataTool");

let controller;

beforeAll(() => {
    controller = new SimpleDataTool();
});



describe("Api Extensions", () => {
    test("Get's Agent by Id", () => {
        expect(controller.getAgent(1)[0].first_name).toBe("Catha");
    })

    test("Get's Disaster by Id", () => {
        expect(controller.getDisaster(1)[0].name).toBe("Alaska Flood");
    })

    test("Get's Handler by Id", () => {
        expect(controller.getClaimHandler(1)[0].first_name).toBe("Barnabe");
    })

    test("Get's Handler by Id", () => {
        expect(controller.getClaim(1)[0].type).toBe("Auto");
    })
})
