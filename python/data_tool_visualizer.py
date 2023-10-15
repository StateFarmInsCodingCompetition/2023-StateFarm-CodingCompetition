import pandas as pd
import matplotlib.pyplot as plt
from simple_data_tool import SimpleDataTool
from collections import defaultdict


class DataToolVisualizer:

    def __init__(self):
        self.data_tool = SimpleDataTool()
        self.agent_data_df = pd.DataFrame(self.data_tool.get_agent_data())
        self.disaster_data_df = pd.DataFrame(self.data_tool.get_disaster_data())
        self.claim_data_df = pd.DataFrame(self.data_tool.get_claim_data())
        self.claim_handler_data_df = pd.DataFrame(self.data_tool.get_claim_handler_data())

    def get_agent_data_df(self):
        return self.agent_data_df

    def get_disaster_data_df(self):
        return self.disaster_data_df

    def get_claim_data_df(self):
        return self.claim_data_df

    def get_claim_handler_data_df(self):
        return self.claim_handler_data_df


    # Shows the cost of disasters by date chronologically
    def disaster_cost_by_date(self):
        df = pd.DataFrame()
        df['declared_date'] = self.disaster_data_df['declared_date']
        df['cost'] = [self.data_tool.get_total_claim_cost_for_disaster(i) for i in self.disaster_data_df['id']]
        df.plot(kind = "scatter", x = 'declared_date', y = 'cost')
        plt.show()

    def plot_estimate_cost_by_severity_rating(self):
        self.claim_data_df.plot(kind = 'scatter', x = 'severity_rating', y = 'estimate_cost')
        plt.show()

    def visualizer(self):
        EXIT_STRINGS = {'q', 'exit', 'quit'}
        CLASS_ID = {
            'agent': 0,
            'disaster': 1,
            'claim': 2,
            'claim handler': 3
        }
        tool = DataToolVisualizer()

        # Ask for user input
        print("Enter 'exit' to leave application")
        while True:
            print("Select a class to examine data on: Agent, Disaster, Claim, Claim Handler")
            user_input = input()
            if user_input.lower() in EXIT_STRINGS:
                return
            if user_input.lower() not in CLASS_ID.keys():
                print("Input not recognized")
                continue
            val = CLASS_ID[user_input.lower()]
            df = pd.DataFrame()
            if val == 0:
                df = tool.get_agent_data_df()
            elif val == 1:
                df = tool.get_disaster_data_df()
            elif val == 2:
                df = tool.get_claim_data_df()
            elif val == 3:
                df = tool.get_claim_handler_data_df()

            columns = df.columns
            while True:
                print("Choose an x-axis and y-axis to visualize a scatter plot(separated by a space): ")
                print(', '.join(columns))
                user_input = input()
                if user_input.lower() in EXIT_STRINGS:
                    return
                arr = user_input.split()
                if len(arr) != 2:
                    print("Please enter 2 arguments")
                    continue
                x_axis, y_axis = arr[0], arr[1]
                if x_axis not in columns:
                    print("x-axis invalid")
                    continue
                if y_axis not in columns:
                    print("y-axis invalid")
                    continue
                df.plot(kind='scatter', x=x_axis, y=y_axis)
                plt.show()
                return

    # Shows a bar graph of the number of disasters in each state in descending order
    def disasters_per_state(self):
        disaster_dict = defaultdict(int)

        # Create an array of tuples between states and their disasters
        for disaster in self.data_tool.get_disaster_data():
            disaster_dict[disaster["state"]] += 1
        state_disaster_pairs = sorted(disaster_dict.items(), key = lambda x: x[1], reverse = True)

        df = pd.DataFrame()
        df['states'] = [x[0] for x in state_disaster_pairs]     # State Column
        df['disasters'] = [x[1] for x in state_disaster_pairs]  # Disaster column
        df.plot(kind = "bar", x = 'states', y = 'disasters')
        plt.show()

    def agents_per_state(self):
        agent_dict = defaultdict(int)

        # Create an array of tuples between states and their agents
        for agent in self.data_tool.get_agent_data():
            agent_dict[agent["state"]] += 1
        state_agent_pairs = sorted(agent_dict.items(), key = lambda x: x[1], reverse = True)

        df = pd.DataFrame()
        df['states'] = [x[0] for x in state_agent_pairs]     
        df['agents'] = [x[1] for x in state_agent_pairs]  
        df.plot(kind = "bar", x = 'states', y = 'agents')
        plt.show()

if __name__ == "__main__":
    tool = DataToolVisualizer()
    tool.visualizer()