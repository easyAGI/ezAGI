# ezAGI.py multi-model LLM with automind reasoning from premise to draw_conclusion
# ezAGI (c) Gregory L. Magnusson MIT license 2024
# conversation from main_loop(self) is saved to ./memory/stm/timestampmemory.json from memory.py creating short term memory store of input response
# reasoning_loop(self)conversation from internal_conclusions are saved in ./memory/logs/thoughts.json
# easy augmented generative intelligence UIUX

from nicegui import ui, app  # handle UIUX
from fastapi.staticfiles import StaticFiles  # integrate fastapi static folder and gfx folder
from webmind.ollama_handler import OllamaHandler  # Import OllamaHandler for modular Ollama interactions
from webmind.html_head import add_head_html  # handler for the html head imports and meta tags
from automind.openmind import OpenMind  # Importing OpenMind class from openmind.py
import concurrent.futures
import ujson as json
import asyncio
import aiohttp
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Serve static graphic files and easystyle.css from the 'gfx' directory
app.mount('/gfx', StaticFiles(directory='gfx'), name='gfx')

openmind = OpenMind()  # initialize OpenMind instance

@ui.page('/')
def main():
    global executor, message_container, log, keys_container, log_buttons, text
    executor = concurrent.futures.ThreadPoolExecutor()  # initialize thread pool executor to manage and execute multiple tasks concurrently
    log_buttons = []  # List to store log button references

    async def send() -> None:
        question = text.value  # get value from input field
        text.value = ''  # clear input field for openmind
        await openmind.send_message(question)  # send the question to OpenMind
        await openmind.internal_queue.put(question)  # add question to the internal queue for processing

    # configure HTML head content from html_head.py external module in the webmind folder
    add_head_html(ui)

    # initialize dark mode toggle
    dark_mode = ui.dark_mode()

    async def toggle_dark_mode():
        dark_mode.value = not dark_mode.value  # toggle dark mode value
        dark_mode_toggle.set_text('Light Mode' if dark_mode.value else 'Dark Mode')  # update button
        dark_mode_toggle.classes(remove='light-mode-toggle' if dark_mode.value else 'dark-mode-toggle')  # class remove for dark-mode / light-mode
        dark_mode_toggle.classes(add='dark-mode-toggle' if dark_mode.value else 'light-mode-toggle')  # dark_mode toggle switch

        # update log button styles based on dark mode
        for button in log_buttons:
            button.classes(remove='light-log-buttons' if dark_mode.value else 'dark-log-buttons')
            button.classes(add='dark-log-buttons' if dark_mode.value else 'light-log-buttons')

    # create a row for the dark mode toggle button and FAB button
    with ui.row().classes('justify-between w-full p-4'):
        with ui.row().classes('items-center'):
            with ui.element('q-fab').props('icon=menu color=blue position=fixed top-2 left-2'):
                fab_action_container = ui.element('div').props('vertical')
                keys_list = openmind.api_manager.api_keys.items()
                for service, key in keys_list:
                    def create_fab_action(service):
                        ui.element('q-fab-action').props(f'icon=label color=green-5 label="{service}"').on('click', lambda: openmind.select_model(service))
                    create_fab_action(service)
        dark_mode_toggle = ui.button('Dark Mode', on_click=toggle_dark_mode).classes('light-mode-toggle')

    # define log files and their paths
    log_files = {
        "Premises Log": "./memory/logs/premises.json",
        "Not Premise Log": "./memory/logs/notpremise.json",
        "Truth Tables Log": "./memory/truth/logs.txt",
        "Thoughts Log": "./memory/logs/thoughts.json",
        "Conclusions Log": "./memory/logs/conclusions.txt",
        "Decisions Log": "./memory/logs/truth.json"
    }

    # function to view log files
    def view_log(file_path):
        log_content = openmind.read_log_file(file_path)  # Read log file content
        log_container.clear()  # Clear the existing log content
        with log_container:
            ui.markdown(log_content).classes('w-full')  # Display log content

    # create tabs menu for chat, logs, API keys, and admin
    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('chat').classes('tab-style')
        logs_tab = ui.tab('logs').classes('tab-style')
        api_tab = ui.tab('APIk').classes('tab-style')
        
    # create tab panels for the tabs
    with ui.tab_panels(tabs, value=chat_tab).props('style="background-color: rgba(255, 255, 255, 0.5);"').classes('response-style'):
        message_container = ui.tab_panel(chat_tab).props('style="background-color: rgba(255, 255, 255, 0.5);"').classes('items-stretch response-container')
        openmind.message_container = message_container  # Pass the container to OpenMind

        # create logs tab panel
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')
            log_container = ui.column().classes('w-full')
            openmind.log = log  # Pass the log to OpenMind

            log_buttons_container = ui.column().classes('w-full')
            with log_buttons_container:
                for log_name, log_path in log_files.items():
                    button = ui.button(log_name, on_click=lambda path=log_path: view_log(path)).classes('log-buttons light-log-buttons' if dark_mode.value else 'dark-log-buttons')
                    log_buttons.append(button)  # append button to log_buttons list

        # create API keys tab panel
        with ui.tab_panel(api_tab):
            ui.label('Manage API Keys').classes('text-lg font-bold')
            with ui.row().classes('items-center'):
                openmind.service_input = ui.input('("together", "openai", "groq")').classes('flex-1 input')
                openmind.key_input = ui.input('API Key').classes('flex-1 input')
            with ui.dropdown_button('Actions', auto_close=True):
                ui.menu_item('Add API Key', on_click=openmind.add_api_key).classes('api-action')
                ui.menu_item('List API Keys', on_click=openmind.list_api_keys).classes('api-action')

            keys_container = ui.column().classes('w-full')
            openmind.keys_container = keys_container  # pass the container to OpenMind

    # footer as input field and with external markdown link
    with ui.footer().classes('footer'), ui.column().classes('footer'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input(placeholder='Enter text here').classes('input').on('keydown.enter', send)  # input field with enter key event
        ui.markdown('[easyAGI](https://rage.pythai.net)').classes('footer-link')

    # openmind internal reasoning asynchronous task ensuring non-blocking execution and efficient concurrency
    asyncio.create_task(openmind.main_loop())



logging.debug("starting easyAGI")
ui.run(title='easyAGI')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
