# ollama_handler.py
# code extrapolated from ollama-python for interaction with an ollama installation
# ollama_handler (c) 2024 codephreak MIT licence

import logging
import subprocess
import asyncio
import aiohttp
import ujson as json
from nicegui import ui

class OllamaHandler:
    """
    Class to interact with Llama3 model via the Ollama service.
    """
    def __init__(self):
        self.api_url = "http://localhost:11434/api"
        self.models = []
        self.selected_model = None

    def check_installation(self):
        """
        Check if Ollama is installed and accessible.
        """
        command = "ollama list"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Ollama is installed and accessible.")
                return True
            else:
                logging.error("Ollama is not accessible.")
                return False
        except Exception as e:
            logging.error(f"Failed to check Ollama installation: {e}")
            return False

    def list_models(self):
        """
        List all available models in the Ollama service.
        """
        command = "ollama list"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.models = result.stdout.strip().splitlines()
                return self.models
            else:
                logging.error(f"Ollama API error: {result.stderr}")
                return []
        except Exception as e:
            logging.error(f"Ollama API error: {e}")
            return []

    async def generate_response_async(self, knowledge, model="llama3"):
        """
        Generate a response from the Llama3 model based on the given knowledge prompt using streaming.
        """
        try:
            response_content = ""
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": knowledge,
                    "stream": True
                }
                async with session.post(f"{self.api_url}/generate", json=payload) as response:
                    async for line in response.content:
                        if line:
                            data = json.loads(line.decode('utf-8'))
                            if "response" in data:
                                response_content += data["response"]
                            elif "error" in data:
                                logging.error(f"Error in response: {data['error']}")
                                return f"Error: {data['error']}"
            return response_content
        except Exception as e:
            logging.error(f"Ollama API error: {e}")
            return "Error: Unable to generate a response due to an issue with the Ollama API."

    async def show_ollama_info_async(self, container):
        """
        Show information about the Ollama service.
        """
        command = "ollama show"
        try:
            result = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await result.communicate()
            if result.returncode == 0:
                with container:  # Ensure the correct UI context
                    ui.notify('Ollama information displayed successfully.', type='positive')
                return stdout.decode().strip()
            else:
                logging.error(f"Ollama API error: {stderr.decode().strip()}")
                with container:  # Ensure the correct UI context
                    ui.notify(f'Error displaying Ollama information: {stderr.decode().strip()}', type='negative')
                return ""
        except Exception as e:
            logging.error(f"Ollama API error: {e}")
            with container:  # Ensure the correct UI context
                ui.notify(f'Exception occurred while showing Ollama information: {e}', type='negative')
            return ""

    def install_ollama(self):
        """
        deb variant Linux install Ollama on using the provided installation script
        terminal command as subprocess
        """
        command = "sudo curl -fsSL https://ollama.com/install.sh | sh"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "Ollama installation successful."
            else:
                logging.error(f"Ollama install error: {result.stderr}")
                return "Error: Unable to install Ollama."
        except Exception as e:
            logging.error(f"Ollama install error: {e}")
            return "Error: Unable to install Ollama."

    async def test_ollama(self):
        """
        Test Ollama by generating a response to a default prompt.
        """
        return await self.generate_response_async("explain easy Augmented Generative Intelligence as a framework", self.selected_model)

    def select_model(self, model_name):
        """
        Select the model to use for generating responses.
        """
        self.selected_model = model_name
        logging.info(f"Selected model: {model_name}")

