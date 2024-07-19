# automind.py (c) 2024 Gregory L. Magnusson MIT license
# draw_conclusion from perceive_environment(self)
import logging
from memory.memory import create_memory_folders, store_in_stm, DialogEntry
from automind.agi import AGI
from webmind.chatter import GPT4o, GroqModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FundamentalAGI')

class FundamentalAGI:
    def __init__(self, chatter):
        self.agi = self.initialize_agi(chatter)
        self.initialize_memory()

    def initialize_memory(self):
        create_memory_folders()
        logger.info("Memory folders initialized.")
    
    def initialize_agi(self, chatter):
        return AGI(chatter)

    def main_loop(self):
        """
        interact with environment for decision
        """
        while True:
            environment_data = self.perceive_environment()
            if environment_data.lower() == 'exit':
                break

            self.agi.reasoning.add_premise(environment_data)
            conclusion = self.agi.reasoning.draw_conclusion()
            self.communicate_response(conclusion)

            entry = DialogEntry(environment_data, conclusion)
            store_in_stm(entry)
            logger.info(f"Stored dialog entry: {entry}")

    def perceive_environment(self):
        """
        prompt input as perception
        """
        agi_prompt = input("") # open prompt for openmind
        return agi_prompt

    def communicate_response(self, conclusion):
        """
        log and print conclusion
        """
        logging.info(f"communicating response: {conclusion}")
        print(conclusion)

    def get_conclusion_from_agi(self, prompt):
        self.agi.reasoning.add_premise(prompt)
        conclusion = self.agi.reasoning.draw_conclusion()
        return conclusion

def main():
    openai_key = input("Enter OpenAI API Key: ").strip()
    groq_key = input("Enter Groq API Key: ").strip()
    
    if openai_key:
        chatter = GPT4o(openai_key)
    elif groq_key:
        chatter = GroqModel(groq_key)
    else:
        print("No suitable API key found. Exiting.")
        return
    
    fundamental_agi = FundamentalAGI(chatter)
    fundamental_agi.main_loop()

if __name__ == "__main__":
    main()

