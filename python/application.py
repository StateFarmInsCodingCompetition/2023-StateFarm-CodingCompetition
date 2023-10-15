from simple_data_tool import SimpleDataTool
# Don't modify test_simple_data_tool.py 
from test.test_simple_data_tool import TestSetOne, TestSetTwo, TestSetThree, TestSetFour

dataset = SimpleDataTool()

print(dataset.get_top_three_months_with_highest_num_of_claims_desc())