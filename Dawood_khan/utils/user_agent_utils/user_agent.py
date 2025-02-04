import json
import os
import random
import config


class UserAgent:
    def __init__(self):
        # Load the user agent list from the given JSON file
        user_agent_file = os.path.join(config.HOME_DIR, "utils/user_agent_utils/user_agent_list.json")
        self.user_agents = self.load(file=user_agent_file)

    @staticmethod
    def load(file):
        """Loads the data from the supplied JSON file"""
        try:
            with open(file, 'r') as fp:
                data = json.load(fp)
        except FileNotFoundError:
            print(f"Error: {file} not found.")
            raise
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {file}.")
            raise

        if not data:
            print(f"Warning: {file} is empty.")
            raise ValueError(f"Empty data in {file}")

        return data.get('browsers', {})

    def user_agent(self):
        """Returns a random user agent selected from the provided data"""
        if not self.user_agents:
            raise ValueError("User agent data is empty, cannot select an agent.")

        # Randomly select a browser and then a user agent for that browser
        browser = random.choice(list(self.user_agents))
        return random.choice(self.user_agents[browser])


if __name__ == '__main__':
    user_agent = UserAgent()
    print(user_agent.user_agent())
