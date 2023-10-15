from simple_data_tool import SimpleDataTool
# Don't modify test_simple_data_tool.py 
from test.test_simple_data_tool import TestSetOne, TestSetTwo, TestSetThree, TestSetFour

import pytest

dataset = SimpleDataTool()
claims = dataset.get_claim_data()

print(dataset.get_num_closed_claims())
print(dataset.get_num_claims_for_claim_handler_id(47))
print(dataset.get_num_disasters_for_state("Texas"))