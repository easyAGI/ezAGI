# agi.py (c) Gregory L. Magnusson MIT license 2024
# input from environment to learn from data to make decisions
# get input from environment_data = self.perceive_environment() learn_from_date(self, data) to make_decisions(self, proposition_p, proposition_q)
import logging
from automind.SocraticReasoning import SocraticReasoning
from automind.logic import LogicTables
from memory.memory import store_in_stm, DialogEntry
from webmind.chatter import GPT4o, Groq
from webmind.api import APIManager  # ensure this import statement is added

class AGI:
    def __init__(self, chatter):
        # Initialize AGI with a chatter instance and SocraticReasoning
        self.chatter = chatter
        self.reasoning = SocraticReasoning(self.chatter)

    def learn_from_data(self, data):
        # Learn from input data
        proposition_p = data  # For simplicity, treat the entire input as one proposition
        proposition_q = "processed data"  # placeholder for further processing if needed
        return proposition_p, proposition_q

    def make_decisions(self, proposition_p, proposition_q):
        # Make decisions based on propositions
        self.reasoning.add_premise(proposition_p)
        self.reasoning.add_premise(proposition_q)
        self.reasoning.draw_conclusion()
        return self.reasoning.logical_conclusion

class EasyAGI:
    def __init__(self):
        # Initialize EasyAGI with APIManager and AGI instances
        self.api_manager = APIManager()
        self.api_manager.manage_api_keys()  # call the method directly from APIManager
        self.agi = AGI(self.api_manager)
        self.initialize_memory()

    def initialize_memory(self):
        # Initialize memory folders
        create_memory_folders()

    def main_loop(self):
        # main_loop to interact with the environment and make decisions
        while True:
            environment_data = self.perceive_environment()  # get input from the environment
            if environment_data.lower() == 'exit':  # exit condition
                break

            proposition_p, proposition_q = self.agi.learn_from_data(environment_data)  # Learn from data
            decision = self.agi.make_decisions(proposition_p, proposition_q)  # Make a decision
            self.communicate_response(decision)  # Communicate the decision

            entry = DialogEntry(environment_data, decision)  # store the dialog entry in memory
            store_in_stm(entry)

    def perceive_environment(self):
        # Get input from the user
        agi_prompt = input("")  # environment is empty prompt
        return agi_prompt

    def communicate_response(self, decision):
        # Log and print the decision
        logging.info(f"Communicating response: {decision}")
        print(decision)

def main():
    # Entry point of the program
    easy_agi = EasyAGI()  # Initialize EasyAGI
    easy_agi.main_loop()  # Start the main loop

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
