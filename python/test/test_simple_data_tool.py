import pytest
from simple_data_tool import SimpleDataTool

@pytest.fixture
def controller():
    return SimpleDataTool()

def test_read(controller):
    simple_models = controller.load_simple_models()

    assert(simple_models is not None)
    assert(len(simple_models) == 1)

    model_1 = simple_models[0]

    assert(model_1.get("name") == "John Smith")
    assert(model_1.get("integer") == 1)
    assert(model_1.get("decimal") == 1.99)