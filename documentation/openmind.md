# openmind.py (c) 2024  Gregory L. Magnusson MIT licence


openmind.py is the core module of the EasyAGI project that handles the interaction between the user interface and the underlying augemented generative intelligence (AGI) system. This module is responsible for managing API keys, initializing AGI instances, processing user inputs, and displaying results. It integrates with various services like OpenAI, Groq, and LLaMA.

# Dependencies

    os: For interacting with the operating system.
    time: For handling time-related functions.
    datetime: For managing date and time objects.
    asyncio: For asynchronous programming.
    logging: For logging debug and error messages.
    ujson: For fast JSON parsing and encoding.
    httpx: For making HTTP requests.
    nicegui: For building user interfaces.
    memory.memory: For managing memory-related functions.
    automind.automind: For AGI functionalities.
    webmind.api: For API management.
    webmind.chatter: For handling input response.

# Classes and Methods

OpenMind

This class encapsulates the logic for interacting with the AGI, managing API keys, and handling user inputs.
Initialization

```python
def __init__(self):
    self.api_manager = APIManager()
    self.agi_instance = None
    self.initialize_memory()
    self.initialize_agi()
    self.internal_queue = asyncio.Queue()
    self.prompt = ""  # Initialize an empty prompt field
    self.keys_container = None  # Placeholder for keys_container
    self.message_container = None  # Placeholder for message_container
    self.log = None  # Placeholder for log
```
    api_manager: Manages API keys.
    agi_instance: Instance of the AGI system.
    internal_queue: Queue for handling asynchronous tasks.
    prompt: Stores the current user prompt.
    keys_container: Placeholder for the UI element displaying API keys.
    message_container: Placeholder for the UI element displaying messages.
    log: Placeholder for the log UI element.

# initialize_memory

Initializes memory-related folders

```python
def initialize_memory(self):
    create_memory_folders()
```

# add_api_key

Adds a new API key and updates the AGI initialization

``python
def add_api_key(self):
    service = self.service_input.value.strip()
    api_key = self.key_input.value.strip()
    logging.debug(f"Adding API key for {service}: {api_key[:4]}...{api_key[-4:]}")
    if service and api_key:
        self.api_manager.api_keys[service] = api_key
        self.api_manager.save_api_key(service, api_key)
        self.initialize_agi()
        ui.notify(f'API key for {service} added and loaded successfully')
        self.service_input.value = ''
        self.key_input.value = ''
        ui.run_javascript('setTimeout(() => { window.location.href = "/"; }, 1000);')
    else:
        ui.notify('Please provide both service name and API key')
```

# delete_api_key

Deletes an existing API key and updates the AGI initialization

```python
def delete_api_key(self, service):
    logging.debug(f"Deleting API key for {service}")
    if service in self.api_manager.api_keys:
        del self.api_manager.api_keys[service]
        self.api_manager.remove_api_key(service)
        self.initialize_agi()
        ui.notify(f'API key for {service} removed successfully')
        self.list_api_keys()  # Refresh the list after deletion
    else:
        ui.notify(f'No API key found for {service}')
```

# list_api_keys

Lists all stored API keys in the UI

```python
def list_api_keys(self):
    if self.api_manager.api_keys:
        keys_list = [(service, key) for service, key in self.api_manager.api_keys.items()]
        logging.debug(f"Stored API keys: {keys_list}")
        if self.keys_container:
            self.keys_container.clear()
            for service, key in keys_list:
                with self.keys_container:
                    ui.label(f"{service}: {key[:4]}...{key[-4:]}").classes('flex-1')
                    ui.button('Delete', on_click=lambda s=service: self.delete_api_key(s)).classes('ml-4')
            ui.notify('Stored API keys:\n' + "\n".join([f"{service}: {key[:4]}...{key[-4:]}"] for service, key in keys_list]))
    else:
        ui.notify('No API keys in storage')
        if self.keys_container:
            self.keys_container.clear()
            with self.keys_container:
                ui.label('No API keys in storage')
```

# initialize_agi

Initializes the AGI system based on available API keys

```python
def initialize_agi(self):
    openai_key = self.api_manager.get_api_key('openai')
    groq_key = self.api_manager.get_api_key('groq')
    llama_running = self.check_llama_running()

    if openai_key:
        chatter = GPT4o(openai_key)
        self.agi_instance = FundamentalAGI(chatter)
        ui.notify('Using OpenAI for AGI')
        logging.debug("AGI initialized with OpenAI")
    elif groq_key:
        chatter = GroqModel(groq_key)
        self.agi_instance = FundamentalAGI(chatter)
        ui.notify('Using Groq for AGI')
        logging.debug("AGI initialized with Groq")
    elif llama_running:
        # Placeholder for future LLaMA integration
        ui.notify('LLaMA found running, future integration coming')
        logging.debug("LLaMA running on localhost:11434")
    else:
        self.agi_instance = None
        ui.notify('No valid API key or LLaMA instance found. Please add an API key or start LLaMA.')
        logging.debug("No valid API key or LLaMA instance found. AGI not initialized.")
```

# check_llama_running

Checks if the LLaMA service is running.

```python
def check_llama_running(self):
    try:
        response = httpx.get('http://localhost:11434')
        if response.status_code == 200:
            return True
    except httpx.RequestError as e:
        logging.debug(f"LLaMA connection failed: {e}")
    return False
```

# get_conclusion_from_agi

Gets a conclusion from the AGI based on the provided prompt

```python
async def get_conclusion_from_agi(self, prompt):
    """
    Get a conclusion from the AGI based on the provided prompt.
    This method is asynchronous to allow non-blocking operations.
    """
    if self.agi_instance is None:
        return "AGI not initialized. Please add an API key or start LLaMA."
    conclusion = await asyncio.get_event_loop().run_in_executor(None, self.agi_instance.get_conclusion_from_agi, prompt)
    return conclusion
```

# communicate_response

Logs and prints the conclusion from the AGI

```python
def communicate_response(self, conclusion):
    """
    Log and print the conclusion from the AGI.
    """
    # uncomment below to show conclusion in the terminal
    #logging.info(f"Communicating response: {conclusion}")
    self.display_internal_conclusion(conclusion)
    return conclusion
```

# reasoning_loop

Internal reasoning loop for continuous AGI reasoning without user interaction

```python
async def reasoning_loop(self):
    """
    Internal reasoning loop for continuous AGI reasoning without user interaction.
    This loop adds a prompt to the AGI and processes its conclusion periodically.
    The conclusions are currently displayed in the response window and saved to ./memory/logs/thoughts.json including ./memory/logs/notpremise.json
    """
    while True:
        if self.agi_instance is None:
            openai_key = self.api_manager.get_api_key('openai')
            groq_key = self.api_manager.get_api_key('groq')
            llama_running = self.check_llama_running()
            if openai_key or groq_key or llama_running:
                self.initialize_agi()
            else:
                logging.debug("Waiting for API key or LLaMA instance...")
                await asyncio.sleep(5)  # Wait before checking again
                continue

        prompt = self.prompt  # Use the updated prompt from user input
        conclusion = await self.get_conclusion_from_agi(prompt)
        self.display_internal_conclusion(conclusion)
        save_internal_reasoning({"timestamp": int(time.time()), "prompt": prompt, "conclusion": conclusion})
        await asyncio.sleep(10)  # Adjust the delay as necessary
```

# display_internal_conclusion

Displays the internal reasoning conclusion in the response window and logs it to a JSON file

```python
def display_internal_conclusion(self, conclusion):
    """
    Display the internal reasoning conclusion in the response window and log it to a JSON file.
    """
    if conclusion != "No premises available for logic as conclusion.":
        if self.message_container:
            with self.message_container:
                response_message = ui.chat_message(name='funAGI', sent=False)
                response_message.clear()
                with response_message:
                    ui.html(f"Internal reasoning conclusion: {conclusion}")
        logging.info(f"Internal reasoning conclusion: {conclusion}")

    # Determine which log file to write to
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "conclusion": conclusion
    }
    
    if conclusion == "No premises available for logic as conclusion.":
        log_file_path = "./memory/logs/notpremise.json"
    else:
        log_file_path = "./memory/logs/thoughts.json"

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            json.dump([log_entry], file, indent=4)
    else:
        with open(log_file_path, 'r+') as file:
            data = json.load(file)
            data.append(log_entry)
            file.seek(0)
            json.dump(data, file, indent=4)
```

# main_loop

Main loop to handle both internal reasoning and user input

```python

async def main_loop(self):
    """
    Main loop to handle both internal reasoning and user input.
    """
    asyncio.create_task(self.reasoning_loop())

    while True:
        prompt = await self.internal_queue.get()
        if prompt == 'exit':
            break
        self.prompt = prompt  # Update the prompt with the new input
        conclusion = await self.get_conclusion_from_agi(prompt)
        self.communicate_response(conclusion)
        # Save the input-response pair using save_conversation_memory
        save_conversation_memory({"dialog": {"instruction": prompt, "response": conclusion}})
```

# send_message

Handles sending a message to the AGI and updating the UI with the response

```python
async def send_message(self, question):
    if self.message_container:
        with self.message_container:
            ui.chat_message(text=question, name='query', sent=True)
            response_message = ui.chat_message(name='easyAGI', sent=False)
            spinner = ui.spinner(type='dots')

    try:
        conclusion = await self.get_conclusion_from_agi(question)
        if response_message:
            response_message.clear()
            with response_message:
                ui.html(conclusion)

        await self.run_javascript_with_retry('window.scrollTo(0, document.body.scrollHeight)', retries=3, timeout=30.1)

        # Store the dialog entry
        entry = DialogEntry(question, conclusion)
        store_in_stm(entry)
        # saves conversation following each input response to ./memory/stm/timestampmemeory.json from memory.py
        save_conversation_memory({"dialog": {"instruction": question, "response": conclusion}})
    except Exception as e:
        logging.error(f"Error getting conclusion from easyAGI: {e}")
        if self.log:
            self.log.push(f"Error getting conclusion from easyAGI: {e}")
    finally:
        try:
            if self.message_container:
                self.message_container.remove(spinner)  # Correctly remove the spinner
        except KeyError:
            logging.warning("Spinner element not found in message_container.")
```

# run_javascript_with_retry

Runs a JavaScript command with retries

```python
async def run_javascript_with_retry(self, script, retries=3, timeout=10.0):
    for attempt in range(retries):
        try:
            await ui.run_javascript(script, timeout=timeout)
            return
        except TimeoutError:
            logging.warning(f"JavaScript did not respond within {timeout} s on attempt {attempt + 1}")
    raise TimeoutError(f"JavaScript did not respond after {retries} attempts")
```

# read_log_file

Reads the content of a log file and returns it

```python
def read_log_file(self, file_path):
    """
    Read the content of a log file and return it.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Log file not found: {file_path}")
        return f"Log file not found: {file_path}"
    except Exception as e:
        logging.error(f"Error reading log file {file_path}: {e}")
        return f"Error reading log file {file_path}: {e}"
```

# handle_javascript_response

Handles the JavaScript response for the UI

```python

def handle_javascript_response(self, msg):
    request_id = msg.get('request_id')
    result = msg.get('result', None)

    if request_id is not None:
        if result is not None:
            JavaScriptRequest.resolve(request_id, result)
        else:
            # Handle the case where 'result' is missing
            JavaScriptRequest.reject(request_id, 'Missing result in JavaScript response')
            logging.error(f"JavaScript response missing 'result' for request_id: {request_id}. Response: {msg}")
    else:
        # Handle the case where 'request_id' is missing if needed
        logging.error(f"JavaScript response missing 'request_id'. Response: {msg}")

    # Log the entire message for debugging purposes
    logging.debug(f"Received JavaScript response: {msg}")
```

# Usage

    Initialize OpenMind: Create an instance of the OpenMind class
    Manage API Keys: Use add_api_key, delete_api_key, and list_api_keys to manage API keys
    Run Main Loop: Call main_loop to start handling both internal reasoning and user input
