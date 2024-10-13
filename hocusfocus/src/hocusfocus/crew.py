import random
from tabulate import tabulate
from crewai import Agent, Crew, Task

class HocusfocusCrew:
    def __init__(self):
        self.agent_data = {}
        self.high_usage_agent = self.create_high_usage_agent()
        self.medium_usage_agent = self.create_medium_usage_agent()
        self.low_usage_agent = self.create_low_usage_agent()
        self.simulation_data = []

    def create_high_usage_agent(self):
        agent = Agent(
            role="High Usage Smartphone User",
            goal="Gradually reduce social media usage and increase reading time while maintaining a realistic usage pattern.",
            backstory="You're a heavy smartphone user, typically spending about 10 hours a day on your device, with 8 hours dedicated to social media and 2 hours for other activities.",
            verbose=True
        )
        self.agent_data[agent] = {
            "motivation_modifier": 0.03,
            "activity_probabilities": [0.2, 0.8, 0.1, 0.2]  # [nothing, social media, reading, regular]
        }
        return agent

    def create_medium_usage_agent(self):
        agent = Agent(
            role="Medium Usage Smartphone User",
            goal="Balance screen time between social media and other activities, while increasing reading time.",
            backstory="You're a moderate smartphone user, typically spending about 8 hours a day on your device, with 4 hours dedicated to social media and 4 hours for other activities.",
            verbose=True
        )
        self.agent_data[agent] = {
            "motivation_modifier": 0.02,
            "activity_probabilities": [0.3, 0.6, 0.1, 0.3]  # [nothing, social media, reading, regular]
        }
        return agent

    def create_low_usage_agent(self):
        agent = Agent(
            role="Low Usage Smartphone User",
            goal="Maintain low screen time while balancing necessary tasks and occasional leisure.",
            backstory="You're a light smartphone user, typically spending about 4 hours a day on your device, with 1 hour dedicated to social media and 3 hours for other activities. You're focused on using your device primarily for necessary tasks.",
            verbose=True
        )
        self.agent_data[agent] = {
            "motivation_modifier": 0.01,
            "activity_probabilities": [0.3, 0.4, 0.1, 0.3]  # [nothing, social media, reading, regular]
        }
        return agent

    def simulate_day(self, agent):
        activities = ["nothing", "social_media", "reading", "regular"]
        daily_activities = []
        activity_counts = {activity: 0 for activity in activities}

        for _ in range(16):  # Simulate 16 hours
            rand_num = random.random()
            cumulative_prob = 0
            chosen_activity = None

            for i, prob in enumerate(self.agent_data[agent]["activity_probabilities"]):
                cumulative_prob += prob
                if rand_num < cumulative_prob:
                    chosen_activity = activities[i]
                    break

            daily_activities.append(chosen_activity)
            activity_counts[chosen_activity] += 1

        # Update probabilities based on the day's activities
        new_probabilities = self.agent_data[agent]["activity_probabilities"].copy()
        motivation_modifier = self.agent_data[agent]["motivation_modifier"]

        new_probabilities[0] += motivation_modifier  # nothing
        new_probabilities[1] -= motivation_modifier  # social_media
        new_probabilities[2] += 2 * motivation_modifier * activity_counts["reading"]  # reading
        new_probabilities[3] += motivation_modifier  # regular

        # Normalize probabilities
        total_prob = sum(new_probabilities)
        self.agent_data[agent]["activity_probabilities"] = [prob / total_prob for prob in new_probabilities]

        return {
            "total_time": activity_counts["social_media"] + activity_counts["reading"] + activity_counts["regular"],
            "social_media_time": activity_counts["social_media"],
            "read_time": activity_counts["reading"],
            "regular_time": activity_counts["regular"]
        }

    def process_result(self, agent, day, result):
        return {
            'agent_name': agent.role,
            'day': day,
            'total_time': result['total_time'],
            'social_media_time': result['social_media_time'],
            'read_time': result['read_time'],
            'regular_time': result['regular_time']
        }

    def print_results_table(self):
        headers = ["Agent Name", "Day", "Total Time", "Social Media Time", "Read Time", "Regular Time"]
        table_data = [[d['agent_name'], d['day'], d['total_time'], d['social_media_time'], d['read_time'], d['regular_time']] 
                      for d in self.simulation_data]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def run_simulation(self, days=7):
        agents = [self.high_usage_agent, self.medium_usage_agent, self.low_usage_agent]
        
        for day in range(1, days + 1):
            print(f"\n--- Simulating Day {day} ---")
            
            for agent in agents:
                result = self.simulate_day(agent)
                processed_result = self.process_result(agent, day, result)
                
                self.simulation_data.append(processed_result)
                print(f"\n{agent.role}:")
                print(f"Total time: {processed_result['total_time']} hours")
                print(f"Social media time: {processed_result['social_media_time']} hours")
                print(f"Read time: {processed_result['read_time']} hours")
                print(f"Regular time: {processed_result['regular_time']} hours")
        
        # Print the table at the end of the simulation
        self.print_results_table()