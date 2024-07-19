# chatter.py (c) Gregory L. Magnusson MIT license 2024
# modular file to include input response mechanisms for multi-model environment
# currently accepts openai groq from API llama3 from URL

import openai
from groq import Groq
import subprocess
import asyncio
import logging

class GPT4o:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def generate_response(self, knowledge, model="gpt-4o"):
        prompt = f"{knowledge}"
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "user", "content": prompt}
                ]
            )
            decision = response.choices[0].message.content
            return decision.lower()
        except openai.APIError as e:
            logging.error(f"openai api error: {e}")
            return "error: unable to generate a response due to an issue with the openai api."

class GroqModel:
    def __init__(self, groq_api_key):
        self.client = Groq(api_key=groq_api_key)

    def generate_response(self, knowledge, model="mixtral-8x7b-32768"):
        prompt = f"{knowledge}"
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "user", "content": prompt}
                ],
                model=model,
            )
            decision = chat_completion.choices[0].message.content
            return decision.lower()
        except Exception as e:
            logging.error(f"groq api error: {e}")
            return "error: unable to generate a response due to an issue with the groq api."

class OllamaModel:
    """
    Class to interact with Llama3 model via the Ollama service.
    """
    def __init__(self):
        self.api_url = "http://localhost:11434/api"

    async def generate_response_async(self, knowledge, model="llama3"):
        """
        Generate a response from the Llama3 model based on the given knowledge prompt using streaming.
        """
        try:
            response_content = ""
            stream = ollama.chat(model=model, messages=[{'role': 'user', 'content': knowledge}], stream=True)
            async for chunk in stream:
                response_content += chunk['message']['content']
            return response_content
        except Exception as e:
            logging.error(f"ollama api error: {e}")
            return "error: unable to generate a response due to an issue with the ollama api."

    async def show_ollama_info_async(self):
        """
        Show information about the Ollama service.
        """
        command = "ollama show"
        try:
            result = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await result.communicate()
            if result.returncode == 0:
                return stdout.decode().strip()
            else:
                logging.error(f"ollama api error: {stderr.decode().strip()}")
                return ""
        except Exception as e:
            logging.error(f"ollama api error: {e}")
            return ""

    def list_models(self):
        """
        List all available models in the Ollama service.
        """
        command = "ollama list"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().splitlines()
            else:
                logging.error(f"ollama api error: {result.stderr}")
                return []
        except Exception as e:
            logging.error(f"ollama api error: {e}")
            return []

    def install_ollama(self):
        """
        Install Ollama using the provided installation script.
        """
        command = "curl -fsSL https://ollama.com/install.sh | sh"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "Ollama installation successful."
            else:
                logging.error(f"ollama install error: {result.stderr}")
                return "error: unable to install ollama."
        except Exception as e:
            logging.error(f"ollama install error: {e}")
            return "error: unable to install ollama."

def check_ollama_installation():
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
