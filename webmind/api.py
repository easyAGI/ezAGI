# api.py (c) Gregory L. Magnusson MIT licence 2024
# modular APIManager for integration of scalable appliation programming interface as add, remove and list API from .env
# use dotenv for production API key management
import os
from dotenv import load_dotenv, set_key, dotenv_values

class APIManager:
    def __init__(self):
        self.env_file = '.env'
        self.ensure_env_file()
        load_dotenv(self.env_file)  # load environment variables from .env file
        self.api_keys = self.load_env_api_keys()

    def ensure_env_file(self):
        if not os.path.exists(self.env_file):
            open(self.env_file, 'w').close()  # create an empty .env file if it doesn't exist

    def load_env_api_keys(self):
        # Load API keys from environment variables if available
        env_values = dotenv_values(self.env_file)
        api_keys = {}
        for key, value in env_values.items():
            if key.endswith('_API_KEY'):
                service = key.replace('_API_KEY', '').lower()
                api_keys[service] = value
        return api_keys

    def save_api_key(self, service, api_key):
        # Save API key to .env file
        set_key(self.env_file, f'{service.upper()}_API_KEY', api_key)

    def remove_api_key(self, service):
        # Remove API key from .env file
        set_key(self.env_file, f'{service.upper()}_API_KEY', '')

    def get_api_key(self, service):
        return self.api_keys.get(service)

    def add_api_key_interactive(self):
        service = input("Enter the name of the service (e.g., 'openai', 'groq'): ").strip()
        api_key = input(f"Enter the API key for {service}: ").strip()
        self.api_keys[service] = api_key
        self.save_api_key(service, api_key)
        print(f"API key for {service} added successfully")

    def remove_api_key_interactive(self):
        service = input("Enter the name of the service to delete (e.g., 'openai', 'groq'): ").strip()
        if service in self.api_keys:
            del self.api_keys[service]
            self.remove_api_key(service)
            print(f"API key for {service} removed successfully")
        else:
            print(f"API key NOT FOUND for {service}.")

    def list_api_keys(self):
        if self.api_keys:
            print("Stored API keys:")
            for service, key in self.api_keys.items():
                print(f"{service}: {key[:4]}...{key[-4:]}")  # display partial keys for security
        else:
            print("No API keys stored.")

    def manage_api_keys(self):
        while True:
            self.list_api_keys()
            action = input("Choose an action: (a) Add API key, (d) Delete API key, (l) List API keys, (Press Enter to continue): ").strip().lower()
            if not action:
                break
            elif action == 'a':
                self.add_api_key_interactive()
            elif action == 'd':
                api_name = input("Enter the API name to delete: ").strip()
                if api_name:
                    self.remove_api_key(api_name)
            elif action == 'l':
                self.list_api_keys()
