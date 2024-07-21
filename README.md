# ezAGI
easy Augmented Generative Intelligence for LLM

an exercise in multi-model integration for LLM rational enhancement from ezAGI
with a focus on llama3 integration using ollama in tandem with together.ai llama3

easyAGI has been tested with groq API, openAI API, ollama llama3 from URL, and together.ai API for llama3


# requirements
python3 > 3.7<br />
pip<br />
<a href="https://console.groq.com/docs/quickstart">groq API key</a> or <br />
<a href="https://openai.com/index/openai-api/">openai API key</a> or <br />
<a href="https://api.together.xyz/signin?redirectUrl=/settings/api-keys">together.ai</a><br />


# LINUX INSTALL

sudo apt install git

```bash
git clone https://github.com/easyGLM/ezAGI/
cd ezAGI
python3 -m venv agi
source agi/bin/activate
pip install -r requirements.txt
# activate ezAGI.py with internal reasoning (EXPERIMENTAL)
python3 ezAGI.py
```

# WINDOWS INSTALL

open command prompt
```bash
Press Win + R, type cmd, press Enter
```
```bash
git clone https://github.com/easyGLM/ezAGI/
cd ezAGI
python3 -m venv agi
agi\Scripts\activate
pip install -r requirements.txt
# activate ezAGI.py with internal reasoning (EXPERIMENTAL)
python3 ezAGI.py
```



