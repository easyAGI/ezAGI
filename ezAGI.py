# ollama UI (c) 2024 Gregory L. Magnusson MIT licence
from nicegui import ui, app  # handle UIUX
from fastapi.staticfiles import StaticFiles  # integrate fastapi static folder and gfx folder
from webmind.chatter import OllamaModel, check_ollama_installation
from automind.openmind import OpenMind  # import OpenMind class from openmind.py
from webmind.html_head import add_head_html  # handler for the html head imports and meta tags
import concurrent.futures # asynchronous concurrent execution
import aiohttp # asynchronous HTTP client/server
import asyncio # asynchronous I/O for network
import logging # logging for error handling
import ujson as json # faster json file handling

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class OllamaAGI:
    def __init__(self):
        self.ollama_model = OllamaModel()
        self.models = []
        self.selected_model = None
        self.init_ui()

    def init_ui(self):
        ui.label('ezAGI').classes('text-2xl mb-4')

        with ui.tabs().classes('w-full') as tabs:
            chat_tab = ui.tab('Chat')
            logs_tab = ui.tab('Logs')
            api_tab = ui.tab('API Keys')

        with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
            self.message_container = ui.tab_panel(chat_tab).classes('items-stretch')
            with ui.tab_panel(logs_tab):
                self.log = ui.log().classes('w-full h-full')
                self.log_container = ui.column().classes('w-full')
            with ui.tab_panel(api_tab):
                ui.label('Manage API Keys').classes('text-lg font-bold')
                with ui.row().classes('items-center'):
                    self.service_input = ui.input('Service (e.g., "openai", "groq")').classes('flex-1')
                    self.key_input = ui.input('API Key').classes('flex-1')
                with ui.dropdown_button('Actions', auto_close=True):
                    ui.menu_item('Add API Key', on_click=self.add_api_key)
                    ui.menu_item('List API Keys', on_click=self.list_api_keys)

                self.keys_container = ui.column().classes('w-full')

        with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6 input-area'):
            with ui.row().classes('w-full no-wrap items-center'):
                placeholder = 'Enter your prompt here'
                self.text_input = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                    .classes('w-full self-center').on('keydown.enter', self.handle_generate_response)
            ui.markdown('[Ollama AGI](https://github.com/autoGLM/ollamaAGI)').classes('text-xs self-end mr-8 m-[-1em] text-primary')

        with ui.row().classes('items-center mb-4'):
            ui.button('Check Ollama Installation', on_click=self.check_installation).classes('mr-2')
            ui.button('List Models', on_click=self.list_models).classes('mr-2')
            ui.button('Install Ollama', on_click=self.install_ollama).classes('mr-2')
            ui.button('Show Ollama Info', on_click=lambda: asyncio.create_task(self.show_ollama_info())).classes('mr-2')
            ui.button('Test Ollama', on_click=lambda: asyncio.create_task(self.test_ollama())).classes('mr-2')

        with ui.element('q-fab').props('icon=menu color=blue'):
            self.fab_action_container = ui.element('div').props('vertical')

        self.response_output = ui.label().classes('text-lg mt-4')

    def check_installation(self):
        if check_ollama_installation():
            ui.notify('Ollama is installed and accessible.', type='positive')
            logging.info("Ollama is installed and accessible.")
        else:
            ui.notify('Ollama is not installed or accessible.', type='negative')
            logging.warning("Ollama is not installed or accessible.")

    def list_models(self):
        try:
            logging.debug("Running 'ollama list' command.")
            result = self.ollama_model.list_models()
            if result:
                logging.debug(f"'ollama list' output:\n{result}")
                self.models = [line.split()[0] for line in result[1:]]  # Extract model names
                if self.models:
                    ui.notify('Models listed successfully.', type='positive')
                    logging.info("Models listed successfully.")
                    self.update_fab_actions()
                else:
                    ui.notify('No models found.', type='negative')
                    logging.warning("No models found.")
            else:
                logging.error("Error listing models.")
                ui.notify('Error listing models.', type='negative')
        except Exception as e:
            logging.error(f"Exception during model listing: {e}")
            ui.notify('Exception occurred while listing models.', type='negative')

    def update_fab_actions(self):
        logging.debug("Clearing existing FAB actions.")
        self.fab_action_container.clear()
        for model in self.models:
            logging.debug(f"Adding FAB action for model: {model}")
            with self.fab_action_container:
                ui.element('q-fab-action').props(f'icon=label color=green-5 label="{model}"').on('click', lambda m=model: self.select_model(m))

    def select_model(self, model_name):
        self.selected_model = model_name
        ui.notify(f'Selected model: {model_name}', type='info')
        logging.info(f"Selected model: {model_name}")

    async def handle_generate_response(self, e):
        await self.generate_response()

    async def generate_response(self):
        prompt = self.text_input.value
        if not prompt:
            ui.notify('Please enter a prompt.', type='warning')
            logging.warning("No prompt entered. Please enter a prompt.")
            return
        if not self.selected_model:
            ui.notify('Please select a model first.', type='warning')
            logging.warning("No model selected. Please select a model first.")
            return

        logging.debug(f"Generating response using model: {self.selected_model} with prompt: {prompt}")
        try:
            response_content = ""
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.selected_model,
                    "prompt": prompt,
                    "stream": True
                }
                logging.debug(f"Sending payload: {payload}")
                async with session.post(self.ollama_model.api_url + "/generate", json=payload) as response:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                if "response" in data:
                                    response_content += data["response"]
                                    self.response_output.set_text(response_content)
                                elif "error" in data:
                                    logging.error(f"Error in response: {data['error']}")
                                    ui.notify(f"Error: {data['error']}", type='negative')
                            except json.JSONDecodeError as e:
                                logging.error(f"JSON decode error: {e}")
                                ui.notify(f"JSON decode error: {e}", type='negative')
                logging.info("Generated response successfully.")
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            ui.notify(f"Error generating response: {e}", type='negative')

    async def show_ollama_info(self):
        try:
            logging.debug("Running 'ollama show' command.")
            result = await self.ollama_model.show_ollama_info_async()
            if result:
                logging.debug(f"'ollama show' output:\n{result}")
                with self.message_container:
                    self.response_output.set_text(result)
                ui.notify('Ollama information displayed successfully.', type='positive')
                logging.info("Ollama information displayed successfully.")
            else:
                logging.error("Error displaying Ollama information.")
                with self.message_container:
                    ui.notify('Error displaying Ollama information.', type='negative')
        except Exception as e:
            logging.error(f"Exception during showing Ollama information: {e}")
            with self.message_container:
                ui.notify(f"Exception occurred while showing Ollama information: {e}", type='negative')

    async def test_ollama(self):
        try:
            logging.debug("Running 'ollama test' command.")
            prompt = "Why is the sky blue?"
            response_content = ""
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.selected_model,
                    "prompt": prompt,
                    "stream": True
                }
                logging.debug(f"Sending payload: {payload}")
                async with session.post(self.ollama_model.api_url + "/generate", json=payload) as response:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8'))
                                if "response" in data:
                                    response_content += data["response"]
                                elif "error" in data:
                                    logging.error(f"Error in response: {data['error']}")
                                    with self.message_container:
                                        ui.notify(f"Error: {data['error']}", type='negative')
                            except json.JSONDecodeError as e:
                                logging.error(f"JSON decode error: {e}")
                                ui.notify(f"JSON decode error: {e}", type='negative')
                logging.info("Ollama test completed successfully.")
                with self.message_container:
                    self.response_output.set_text(f"Test prompt: {prompt}\nResponse: {response_content}")
        except Exception as e:
            logging.error(f"Error during Ollama test: {e}")
            with self.message_container:
                ui.notify(f"Error during Ollama test: {e}", type='negative')

    def install_ollama(self):
        logging.debug("Running Ollama installation command.")
        response = self.ollama_model.install_ollama()
        with self.message_container:
            ui.notify(response, type='info')
        logging.info(f"Ollama installation response: {response}")

    def add_api_key(self):
        with self.message_container:
            ui.notify('API key added.', type='positive')
        logging.info('API key added.')

    def list_api_keys(self):
        with self.message_container:
            ui.notify('API keys listed.', type='positive')
        logging.info('API keys listed.')

if __name__ in {"__main__", "__mp_main__"}:
    ollama_agi = OllamaAGI()
    ui.run()
