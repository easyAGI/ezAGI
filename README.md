# ezAGI
easy Augmented Generative Intelligence for LLM

> **Development has consolidated at [github.com/easyGLM/ezAGI](https://github.com/easyGLM/ezAGI) (v1.0.0+).**
> This repository is a frozen historical snapshot of the minimal development
> version that displayed reasoning capabilities as log files.

The complete easy AGI system — multi-provider reasoning (openai, groq,
together, anthropic, ollama local + Ollama Cloud), Socratic validation with
confidence-scored truths, the ezAGI console separating production chat from
the internal reasoning trace, MASTERMIND agency and SimpleMind learning —
lives at [easyGLM/ezAGI](https://github.com/easyGLM/ezAGI).

```bash
git clone https://github.com/easyGLM/ezAGI/
cd ezAGI
python3 -m venv agi
source agi/bin/activate
pip install -r requirements.txt
python3 ezAGI.py
```

Lineage (documented in
[docs/lineage.md](https://github.com/easyGLM/ezAGI/blob/main/docs/lineage.md)):
**AUTOMINDx → aGLM → MASTERMIND → RAGE → funAGI → ezAGI → mindX**

The Ollama point of departure remains at
[llamagi/lmagi](https://github.com/llamagi/lmagi).

ezAGI (c) 2024–2026 PYTHAI · Gregory L. Magnusson (Professor Codephreak) · MIT
— a [PYTHAI](https://github.com/pythaiml) project
