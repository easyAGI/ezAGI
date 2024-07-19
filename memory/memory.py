# memory.py (c) Gregory L. Magnusson MIT licence 2024
# memory creates the local file system folder structure for the easyAGI platform
# memory create short term memory as stm long term memory as ltm epistodic memory as episodic
# stores truth in ./memory/truth as belief, truth and fact where fact is a not a tautology as reasoned from SocraticReasoning and logic
# agency is the executable folder to be controlled by mastermind
# episodic is the memory folder to be used for multi-modal input response memory storage
# conversation input response is saved to short term memory folder stm as memory/stm{timestamp}memory.json
import os
import pathlib
import time
import ujson
import logging

# Define the constants for memory folders
MEMORY_FOLDER = "./memory/"
STM_FOLDER = MEMORY_FOLDER + "stm/"
LTM_FOLDER = MEMORY_FOLDER + "ltm/"
EPISODIC_FOLDER = MEMORY_FOLDER + "episodic/"
TRUTH_FOLDER = MEMORY_FOLDER + "truth/"
LOGS_FOLDER = MEMORY_FOLDER + "logs/"
MINDX_FOLDER = "./mindx/"
AGENCY_FOLDER = MINDX_FOLDER + "agency/"

class DialogEntry:
    def __init__(self, instruction, response):
        self.instruction = instruction
        self.response = response

def create_memory_folders():
    try:
        if not pathlib.Path(MEMORY_FOLDER).exists():
            pathlib.Path(MEMORY_FOLDER).mkdir(parents=True)
        if not pathlib.Path(STM_FOLDER).exists():
            pathlib.Path(STM_FOLDER).mkdir(parents=True)
        if not pathlib.Path(LTM_FOLDER).exists():
            pathlib.Path(LTM_FOLDER).mkdir(parents=True)
        if not pathlib.Path(EPISODIC_FOLDER).exists():
            pathlib.Path(EPISODIC_FOLDER).mkdir(parents=True)
        if not pathlib.Path(TRUTH_FOLDER).exists():
            pathlib.Path(TRUTH_FOLDER).mkdir(parents=True)
        if not pathlib.Path(LOGS_FOLDER).exists():
            pathlib.Path(LOGS_FOLDER).mkdir(parents=True)
        if not pathlib.Path(MINDX_FOLDER).exists():
            pathlib.Path(MINDX_FOLDER).mkdir(parents=True)
        if not pathlib.Path(AGENCY_FOLDER).exists():
            pathlib.Path(AGENCY_FOLDER).mkdir(parents=True)
    except Exception as e:
        logging.error(f"Error creating memory folders: {e}")

def store_in_stm(dialog_entry):
    filename = f"{int(time.time())}.json"
    filepath = os.path.join(STM_FOLDER, filename)
    with open(filepath, "w") as file:
        ujson.dump(dialog_entry.__dict__, file)

def store_in_ltm(dialog_entry):
    filename = f"{int(time.time())}.json"
    filepath = os.path.join(LTM_FOLDER, filename)
    with open(filepath, "w") as file:
        ujson.dump(dialog_entry.__dict__, file)

def store_episodic_memory(episode):
    filename = f"{int(time.time())}.json"
    filepath = os.path.join(EPISODIC_FOLDER, filename)
    with open(filepath, "w") as file:
        ujson.dump(episode, file)

def save_valid_truth(valid_truth):
    filename = f"{int(time.time())}.json"
    filepath = os.path.join(TRUTH_FOLDER, filename)
    with open(filepath, "w") as file:
        ujson.dump(valid_truth, file)

# save conversation memory as input response in short term memory folder ./memory/stm{timestamp}memory.json
def save_conversation_memory(memory):
    create_memory_folders()

    timestamp = str(int(time.time()))
    stm_filename = f"{STM_FOLDER}{timestamp}memory.json"
    with open(stm_filename, 'w') as f:
        ujson.dump(memory, f)

# save internal reasoning including nopremise as separate save in mindx folder as {timestamp}internalmemory.json and nopremise{timestamp}internalmemory.json
def save_internal_reasoning(memory):
    create_memory_folders()

    timestamp = str(int(time.time()))
    if memory['conclusion'] == "No premises available for logic as conclusion.":
        filename = f"{MINDX_FOLDER}nopremise{timestamp}internalmemory.json"
    else:
        filename = f"{MINDX_FOLDER}{timestamp}internalmemory.json"
    with open(filename, 'w') as f:
        ujson.dump(memory, f)

def load_conversation_memory():
    create_memory_folders()
    memory_files = list(pathlib.Path(MEMORY_FOLDER).glob("*.json"))

    all_memory = []
    for file_path in memory_files:
        with open(file_path, "r", encoding="utf-8") as file:
            memory = ujson.load(file)
            all_memory.extend(memory)

    return all_memory

def delete_conversation_memory():
    create_memory_folders()
    memory_files = list(pathlib.Path(MEMORY_FOLDER).glob("*.json"))

    for file_path in memory_files:
        file_path.unlink()

def get_latest_memory():
    create_memory_folders()
    memory_files = sorted(pathlib.Path(MEMORY_FOLDER).glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not memory_files:
        return []

    latest_file = memory_files[0]
    with open(latest_file, "r", encoding="utf-8") as file:
        memory = ujson.load(file)

    return memory

