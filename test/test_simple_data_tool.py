import pytest
import random
from simple_data_tool import SimpleDataTool


@pytest.fixture
def controller():
    return SimpleDataTool()


def test_read_data_files(controller):
    """Making sure that JSON files load properly. This test does not count towards your score.

    Args:
        controller (SimpleDataTool): utility script that loads JSON files and does comparisons
    """
    assert (len(controller.get_agent_data()) == 100)
    assert (len(controller.get_claim_handler_data()) == 156)
    assert (len(controller.get_claim_data()) == 1000)
    assert (len(controller.get_disaster_data()) == 100)


class TestSetOne:
    def test_get_num_closed_claims(self, controller):
        """Test 1"""
        actual_num_closed_claims = controller.get_num_closed_claims()
        assert actual_num_closed_claims == 362

    def test_get_num_claims_for_claim_handler_id(self, controller):
        """Test 2"""
        assert controller.get_num_claims_for_claim_handler_id(1) == 9
        assert controller.get_num_claims_for_claim_handler_id(93) == 4
        assert controller.get_num_claims_for_claim_handler_id(127) == 6

    def test_get_num_disasters_for_state(self, controller):
        """Test 3"""
        assert controller.get_num_disasters_for_state(
            'Arizona') == 2
        assert controller.get_num_disasters_for_state(
            'Georgia') == 5
        assert controller.get_num_disasters_for_state(
            'Illinois') == 2
        assert controller.get_num_disasters_for_state(
            'Texas') == 9
        assert controller.get_num_disasters_for_state(
            'District of Columbia') == 2


class TestSetTwo:

    def test_get_total_claim_cost_for_disaster(self, controller):
        """Test 4"""
        assert controller.get_total_claim_cost_for_disaster(5) == 377726.38
        assert controller.get_total_claim_cost_for_disaster(0) == None
        assert controller.get_total_claim_cost_for_disaster(
            56) == 1287476.19
        assert controller.get_total_claim_cost_for_disaster(101) == None
        assert controller.get_total_claim_cost_for_disaster(
            78) == 614822.68

    def test_get_average_claim_cost_for_claim_handler(self, controller):
        """Test 5"""
        assert controller.get_average_claim_cost_for_claim_handler(
            2) == 87330.89
        assert round(
            controller.get_average_claim_cost_for_claim_handler(42), 2) == 122195.90
        assert controller.get_average_claim_cost_for_claim_handler(-5) == None
        assert controller.get_average_claim_cost_for_claim_handler(225) == None
        assert round(
            controller.get_average_claim_cost_for_claim_handler(151), 2) == 242134.96

    def test_get_state_with_most_and_least_disasters(self, controller):
        """Test 6"""
        assert controller.get_state_with_most_disasters() == 'California'
        assert controller.get_state_with_least_disasters() == 'Alaska'

    def test_get_most_spoken_agent_language_by_state(self, controller):
        """Test 7"""
        assert controller.get_most_spoken_agent_language_by_state(
            'New Hampshire') == 'Arabic'
        assert controller.get_most_spoken_agent_language_by_state(
            'Wisconsin') == ''
        assert controller.get_most_spoken_agent_language_by_state(
            'Florida') == 'Spanish'

    def test_get_num_of_open_claims_for_agent_and_severity(self, controller):
        """Test 8"""
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            0, 0) == -1
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            25, 11) == -1
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            65, 3) == None
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            24, 1) == 16
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            87, 6) == 3
        assert controller.get_num_of_open_claims_for_agent_and_severity(
            85, 6) == 2


class TestSetThree:

    def test_get_num_disasters_declared_after_end_date(self, controller):
        """Test 9"""
        assert controller.get_num_disasters_declared_after_end_date() == 8

    def test_build_map_of_agents_to_total_claim_cost(self, controller):
        """Test 10"""
        agent_cost_map = controller.build_map_of_agents_to_total_claim_cost()
        assert len(agent_cost_map.keys()) == 100, 'Missing agents in map'

        # Normal cases
        assert agent_cost_map.get(1) == 27856.13
        assert agent_cost_map.get(3) == 2253847.27
        assert agent_cost_map.get(5) == 529685.97
        assert agent_cost_map.get(8) == 282307.93
        assert agent_cost_map.get(13) == 2310862.86

        # Spot-check random agent ids that we expect to have no cost
        expected_agent_ids_without_cost = [2, 6, 9, 12, 16, 22, 25, 32, 33, 37, 38, 40,
                                           41, 44, 45, 48, 50, 51, 52, 53, 54, 61, 64,
                                           65, 67, 69, 72, 81, 90, 93, 96]
        num_agent_ids_without_cost = len(expected_agent_ids_without_cost)
        for i in range(3):
            random_agent_id = expected_agent_ids_without_cost[random.randint(
                0, num_agent_ids_without_cost - 1)]
            assert agent_cost_map.get(random_agent_id) == 0

        # Testing invalid agent ids
        assert agent_cost_map.get(-5) == None
        assert agent_cost_map.get(255) == None

    def test_calculate_disaster_claim_density(self, controller):
        """Test 11"""
        assert controller.calculate_disaster_claim_density(15) == 0.00172
        assert controller.calculate_disaster_claim_density(68) == 0.00029
        assert controller.calculate_disaster_claim_density(101) == None
        assert controller.calculate_disaster_claim_density(64) == 0.01624


class TestSetFour:

    def test_get_top_three_months_with_highest_num_of_claims_desc(self, controller):
        """Test 12"""
        top_three_months = controller.get_top_three_months_with_highest_num_of_claims_desc()
        assert len(top_three_months) == 3
        assert top_three_months[0] == 'April 2023'
        assert top_three_months[1] == 'November 2022'
        assert top_three_months[2] == 'February 2023'
