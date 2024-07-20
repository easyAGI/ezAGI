# memory.py
Author: Gregory L. Magnusson
License: MIT License, 2024

The memory.py module is designed for the easyAGI platform to manage the local file system folder structure and memory storage. It handles the creation and management of short-term memory (STM), long-term memory (LTM), and episodic memory, and stores truths based on Socratic reasoning and logic. The module ensures that different types of memory are appropriately stored, retrieved, and managed.
Folder Structure

    STM (Short Term Memory): Stores recent conversation inputs and responses.
    LTM (Long Term Memory): Stores long-term memory entries.
    Episodic Memory: Stores multi-modal input response memory.
    Truth: Stores beliefs, truths, and facts, distinguishing facts from tautologies using Socratic reasoning.
    Agency: Contains executable files controlled by the mastermind component.
    Logs: Stores log files for debugging and tracking purposes.
    MINDX: Contains internal reasoning and no-premise logs.

Constants

The following constants define the folder structure for the memory system:
```python
MEMORY_FOLDER = "./memory/"
STM_FOLDER = MEMORY_FOLDER + "stm/"
LTM_FOLDER = MEMORY_FOLDER + "ltm/"
EPISODIC_FOLDER = MEMORY_FOLDER + "episodic/"
TRUTH_FOLDER = MEMORY_FOLDER + "truth/"
LOGS_FOLDER = MEMORY_FOLDER + "logs/"
MINDX_FOLDER = "./mindx/"
AGENCY_FOLDER = MINDX_FOLDER + "agency/"
```
# Classes

# DialogEntry
```python
class DialogEntry:
    def __init__(self, instruction, response):
        self.instruction = instruction
        self.response = response
```
A simple class to encapsulate an instruction-response pair.

# Functions

# create_memory_folders
```python
def create_memory_folders():
    ...
```
Creates the necessary folder structure for the memory system if it doesn't already exist

# store_in_stm

```python
def store_in_ltm(dialog_entry):
    ...
```
Stores a DialogEntry object in the short-term memory (STM) folder.

# store_in_ltm
```python
def store_in_ltm(dialog_entry):
    ...
```
Stores a DialogEntry object in the long-term memory (LTM) folder

# store_episodic_memory
```python
def store_episodic_memory(episode):
    ...
```
Stores an episodic memory entry

# save_valid_truth
```python
def save_valid_truth(valid_truth):
    ...
```
Saves a valid truth entry in the truth folder.

# save_conversation_memory
```python
def save_conversation_memory(memory):
    ...
```
Saves conversation input and response to the short-term memory folder

# save_internal_reasoning
```python
def save_internal_reasoning(memory):
    ...
```
Saves internal reasoning, including no-premise entries, to the MINDX folder

# load_conversation_memory
```python
def load_conversation_memory():
    ...
```
Loads all conversation memories from the memory folder

# delete_conversation_memory
```python
def delete_conversation_memory():
    ...
```
# def get_latest_memory():
    ...
```python
def get_latest_memory():
    ...
```

Usage Examples
# Creating Memory Folders

```python
create_memory_folders()
```
Ensure the folder structure exists before performing any memory operations.


# Store dialogue entries in Short-Term Memory
```
```python
dialog_entry = DialogEntry("Hello, how are you?", "I am good, thank you!")
store_in_stm(dialog_entry)
```
# Store in Long-Term Memory

```python
store_in_ltm(dialog_entry)
```
# Storing Episodic Memory
```
python
episode = {"event": "User logged in", "timestamp": time.time()}
store_episodic_memory(episode)
```
# Saving Valid Truth
```
python
valid_truth = {"statement": "The sky is blue", "verified": True}
save_valid_truth(valid_truth)
```
# Saving Conversation Memory
```
python
conversation_memory = {
    "instruction": "Tell me a joke.",
    "response": "Why did the scarecrow win an award? Because he was outstanding in his field!"
}
save_conversation_memory(conversation_memory)
```
# Saving Internal Reasoning
```
```python
internal_reasoning = {
    "conclusion": "This is a well-formed logical statement.",
    "premises": ["Premise 1", "Premise 2"]
}
save_internal_reasoning(internal_reasoning)
```
# Loading Conversation Memory
```
python
all_memory = load_conversation_memory()
print(all_memory)
```
# Deleting Conversation Memory
```
python
delete_conversation_memory()
```
# Getting the Latest Memory
```
python
latest_memory = get_latest_memory()
print(latest_memory)
```

The memory.py module is a crucial component of the easyAGI platform providing a structured approach to managing different types of memory and truths. By creating and maintaining a well-organized file system, memory.py ensures that conversation data, internal reasoning, and truths are stored, retrieved, and managed efficiently. This documentation provides a detailed overview of the module's functionality, helping easyAGI developers understand and utilize memory storage capabilities effectively to enhance LLM
