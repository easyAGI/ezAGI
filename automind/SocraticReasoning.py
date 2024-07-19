# SocraticReasoning.py (c) 2024 Gregory L. Magnusson MIT license
################ memory/logs/ for socratic #####################
# self.socraticlogs_file = './memory/logs/socraticlogs.txt'
# self.premises_file = './memory/logs/premises.json'
# self.not_premises_file = './memory/logs/notpremise.json'
# self.conclusions_file = './memory/logs/conclusions.txt'
# self.truth_tables_file = './memory/logs/truth.json'
import logging
import os
import pathlib
import ujson
from datetime import datetime
from webmind.chatter import GPT4o, GroqModel, OllamaModel
from automind.logic import LogicTables
from memory.memory import create_memory_folders, store_in_stm, DialogEntry
from webmind.api import APIManager

class SocraticReasoning:
    def __init__(self, chatter):
        """
        Initializes the SocraticReasoning instance with necessary configurations.
        
        Args:
            chatter: An instance of the model used for generating responses.
        """
        self.premises = []  # List to hold premises
        self.logger = logging.getLogger('SocraticReasoning')
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all SocraticReasoning logs

        # Ensure the logs directory exists
        logs_dir = './memory/logs'
        os.makedirs(logs_dir, exist_ok=True)

        # File handler for saving Socratic Reasoning logs
        self.socraticlogs_file = './memory/logs/socraticlogs.txt'
        file_handler = logging.FileHandler(self.socraticlogs_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Stream handler to suppress lower-level logs in the terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.CRITICAL)  # Show only critical logs in the terminal
        stream_formatter = logging.Formatter('%(message)s')
        stream_handler.setFormatter(stream_formatter)

        # Adding handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

        # File paths for saving premises, non-premises, conclusions, and truth tables
        self.socraticlogs_file = './memory/logs/socraticlogs.txt'
        self.premises_file = './memory/logs/premises.json'
        self.not_premises_file = './memory/logs/notpremise.json'
        self.conclusions_file = './memory/logs/conclusions.txt'
        self.truth_tables_file = './memory/logs/truth.json'

        self.max_tokens = 100  # Default max tokens for Socratic premise from add_premise(statement)
        self.chatter = chatter  # Chatter model for generating responses
        self.logic_tables = LogicTables()  # Logic tables for reasoning
        self.dialogue_history = []  # List to hold the history of dialogues
        self.logical_conclusion = ""  # Variable to store the conclusion

        create_memory_folders()  # Ensure memory folders are created

    def socraticlogs(self, message, level='info'):
        """
        Logs a message with a specified level.

        Args:
            message: The message to be logged.
            level: The level of logging ('info' or 'error').
        """
        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        self.log_errors(message, level)  # Save Socratic reasoning to ./memory/logs/errorlogs.txt

    def log_errors(self, message, level):
        """
        Stores error logs in ./memory/logs/errorlogs.txt.

        Args:
            message: The error message to be logged.
            level: The level of the error.
        """
        error_logs_path = './memory/logs/errorlogs.txt'
        pathlib.Path(error_logs_path).parent.mkdir(parents=True, exist_ok=True)
        with open(error_logs_path, 'a') as file:
            file.write(f"{level.upper()}: {message}\n")

    def log_not_premise(self, message, level='info'):
        """
        Logs messages that are not considered premises.

        Args:
            message: The message to be logged.
            level: The level of logging.
        """
        not_premises_path = self.not_premises_file
        pathlib.Path(not_premises_path).parent.mkdir(parents=True, exist_ok=True)
        entry = {"level": level.upper(), "message": message}
        try:
            with open(not_premises_path, 'r') as file:
                logs = ujson.load(file)
        except (FileNotFoundError, ValueError):
            logs = []

        logs.append(entry)
        with open(not_premises_path, 'w') as file:
            ujson.dump(logs, file, indent=2)

    def save_premises(self):
        """
        Saves the current list of premises to a JSON file.
        """
        pathlib.Path(self.premises_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.premises_file, 'w') as file:
            ujson.dump(self.premises, file, indent=2)

    def add_premise(self, premise):
        """
        Adds a premise to the list if valid and saves the premises.

        Args:
            premise: The premise to be added.
        """
        if self.parse_statement(premise):  # Check if the premise is valid
            self.premises.append(premise)  # Add the premise to the list
            self.save_premises()  # Save the updated list of premises
        else:
            self.log_not_premise(f'Invalid premise: {premise}', level='error')  # Log invalid premise

    def parse_statement(self, statement):
        """
        Validates a statement to check if it can be a premise.

        Args:
            statement: The statement to be validated.

        Returns:
            bool: True if the statement is valid, False otherwise.
        """
        return isinstance(statement, str) and len(statement) > 0  # Check if the statement is a non-empty string

    def generate_new_premise(self, premise):
        """
        Generates a new premise based on the current premise.

        Args:
            premise: The current premise.

        Returns:
            str: A new premise generated from the current premise.
        """
        premise_text = f"- {premise}"
        new_premise = self.chatter.generate_response(premise_text)
        return new_premise.strip()

    def challenge_premise(self, premise):
        """
        Challenges and removes a premise from the list if it exists.

        Args:
            premise: The premise to be challenged.
        """
        if premise in self.premises:  # Check if the premise exists in the list
            self.premises.remove(premise)  # Remove the premise from the list
            self.socraticlogs(f'Challenged and removed premise: {premise}')  # Log the removal
            self.remove_equivalent_premises(premise)  # Remove equivalent premises
            self.save_premises()  # Save the updated list of premises
        else:
            self.log_not_premise(f'Premise not found: {premise}', level='error')  # Log if premise not found

    def remove_equivalent_premises(self, premise):
        """
        Removes premises that are logically equivalent to the challenged premise.

        Args:
            premise: The premise to be checked for equivalence.
        """
        equivalent_premises = [p for p in self.premises if self.logic_tables.unify_variables(premise, p)]
        for p in equivalent_premises:
            self.premises.remove(p)  # Remove equivalent premise
            self.log_not_premise(f'Removed equivalent premise: {p}')  # Log removal of equivalent premise
        self.save_premises()  # Save the updated list of premises

    def draw_conclusion(self):
        """
        Draws a conclusion based on the current list of premises.

        Returns:
            str: The conclusion derived from the premises.
        """
        if not self.premises:  # Check if there are no premises
            return "No premises available for logic as conclusion."

        current_premise = self.premises[0]  # Start with the first premise
        additional_premises_count = 0  # Counter for additional premises

        # Generate new premises until a valid conclusion is drawn or the maximum limit is reached
        while additional_premises_count < 5:
            new_premise = self.generate_new_premise(current_premise)
            if not self.parse_statement(new_premise):
                continue
            self.premises.append(new_premise)
            self.save_premises()
            additional_premises_count += 1

            # Use the current premise as the input (knowledge) for generating a response
            raw_response = self.chatter.generate_response(current_premise)

            # Process the response to get the conclusion
            conclusion = raw_response.strip()

            self.logical_conclusion = conclusion  # Store the conclusion

            if self.validate_conclusion():  # Validate the conclusion
                break
            else:
                self.log_not_premise('Invalid conclusion. Generating more premises.', level='error')

        # Save the conclusion along with premises
        conclusion_entry = {"premises": self.premises, "conclusion": self.logical_conclusion}
        pathlib.Path(self.premises_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.premises_file, 'w') as file:
            ujson.dump(conclusion_entry, file, indent=2)

        # Log the conclusion to conclusions.txt
        pathlib.Path(self.conclusions_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.conclusions_file, 'a') as file:
            file.write(f"Premises: {self.premises}\nConclusion: {self.logical_conclusion}\n")

        # Save the valid conclusion as a truth
        self.save_truth(self.logical_conclusion)

        # Clear the premises list for the next round
        self.premises = []

        return self.logical_conclusion  # Return the conclusion

    def validate_conclusion(self):
        """
        Validates the logical conclusion.

        Returns:
            bool: True if the conclusion is valid, False otherwise.
        """
        return self.logic_tables.tautology(self.logical_conclusion)  # Validate using logic tables

    def save_truth(self, truth):
        """
        Saves the valid conclusion as a truth in the truth tables.

        Args:
            truth: The truth to be saved.
        """
        truth_tables_entry = {
            "truth": truth,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        pathlib.Path(self.truth_tables_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.truth_tables_file, 'a') as file:
            ujson.dump(truth_tables_entry, file, indent=2)
            file.write("\n")

    def update_logic_tables(self, variables, expressions, valid_truths):
        """
        Updates the logic tables with new variables, expressions, and valid truths.

        Args:
            variables: The logical variables.
            expressions: The logical expressions.
            valid_truths: The valid truths for the logic table.
        """
        self.logic_tables.variables = variables
        self.logic_tables.expressions = expressions
        self.logic_tables.valid_truths = valid_truths

        # Log the truth tables to truth_tables.json
        truth_tables_entry = {
            "variables": variables,
            "expressions": expressions,
            "valid_truths": valid_truths
        }
        pathlib.Path(self.truth_tables_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.truth_tables_file, 'w') as file:
            ujson.dump(truth_tables_entry, file, indent=2)

        # Save a timestamped file in ./memory/truth
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        belief_timestamp_file = f'./memory/truth/belief_{timestamp}.json'
        pathlib.Path(belief_timestamp_file).parent.mkdir(parents=True, exist_ok=True)
        with open(belief_timestamp_file, 'w') as file:
            ujson.dump(truth_tables_entry, file, indent=2)

        # Prepare and save the structured truth log for training
        structured_truth = {
            "variables": variables,
            "expressions": expressions,
            "valid_truths": valid_truths,
            "truth_description": "This log entry captures the current state of the logic tables with the variables, expressions, and valid truths used for reasoning.",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        truth_log_path = './memory/truth/truth_log.json'
        pathlib.Path(truth_log_path).parent.mkdir(parents=True, exist_ok=True)
        with open(truth_log_path, 'a') as file:
            ujson.dump(structured_truth, file, indent=2)
            file.write("\n")

        # Add a log entry to confirm the update
        self.logger.info("Updated logic tables: %s", truth_tables_entry)

    def set_max_tokens(self, max_tokens):
        """
        Sets the maximum number of tokens for generating a response.

        Args:
            max_tokens: The maximum number of tokens.
        """
        self.max_tokens = max_tokens
        self.socraticlogs(f"Max tokens set to: {max_tokens}")

    def interact(self):
        """
        Interacts with the user to add, challenge premises, and draw conclusions.
        """
        while True:
            self.socraticlogs("\nCommands: add, challenge, conclude, set_tokens, exit")
            cmd = input("> ").strip().lower()

            if cmd == 'exit':
                self.socraticlogs('Exiting Socratic Reasoning.')
                break
            elif cmd == 'add':
                premise = input("Enter the premise: ").strip()
                self.add_premise(premise)
            elif cmd == 'challenge':
                premise = input("Enter the premise to challenge: ").strip()
                self.challenge_premise(premise)
            elif cmd == 'conclude':
                conclusion = self.draw_conclusion()
                print(conclusion)
            elif cmd == 'set_tokens':
                tokens = input("Enter the maximum number of tokens for the conclusion: ").strip()
                if tokens.isdigit():
                    self.set_max_tokens(int(tokens))
                else:
                    self.socraticlogs("Invalid number of tokens.", level='error')
                    self.log_not_premise("Invalid number of tokens.", level='error')
            else:
                self.log_not_premise('Invalid command.', level='error')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api_manager = APIManager()  # Initialize API manager to handle API keys
    openai_key = api_manager.get_api_key('openai')
    groq_key = api_manager.get_api_key('groq')
    
    if openai_key:
        chatter = GPT4o(openai_key)  # Use OpenAI model if key is available
    elif groq_key:
        chatter = GroqModel(groq_key)  # Use Groq model if key is available
    else:
        raise ValueError("No suitable API key found. Please add an API key.")

    socratic_reasoning = SocraticReasoning(chatter)  # Initialize SocraticReasoning with the selected model

    # Example usage
    statements = [
        "All humans are mortal.",
        "Socrates is a human."
    ]

    for statement in statements:
        socratic_reasoning.add_premise(statement)  # Add each statement as a premise

    conclusion = socratic_reasoning.draw_conclusion()  # Draw a conclusion based on the premises
    print(conclusion)
    socratic_reasoning.interact()  # Start the interactive loop

