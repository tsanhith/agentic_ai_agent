# 🤖 Robust Agentic AI (Offline Edition)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-success)

A **deterministic, tool-using AI Agent** built from scratch in Python. Unlike standard chatbots, this agent follows a strict **"Think → Execute → Wait"** protocol to perform multi-step tasks, manipulate local files, and validate mathematical operations without hallucinating

---

## ⚡ Why This Agent?

Most AI scripts fail because they try to do too much at once. This agent is engineered for **reliability**:

- **🛡️ Sequential Execution:** Enforces a strict _Stop & Wait_ rule. The agent cannot write a report until it has actually received data from a tool.
- **🧮 Smart Calculator:** Capable of processing entire files of data (e.g., "Find the average of `scores.txt`") rather than just simple arithmetic.
- **✅ Input Sanitization:** Includes a dedicated `validator.py` module that strips garbage text from inputs and prevents crashes (like Division by Zero).
- **🔁 Loop Protection:** Automatically detects if the agent is getting stubborn (retrying failed actions) and forces a stop.

---

## 📂 Project Structure

```text
├── agent.py         # The "Brain" (Manages LLM loop & decision making)
├── tools.py         # The "Hands" (Calculator, Read/Write File logic)
├── validator.py     # The "Guardrails" (Cleans outputs & catches errors)
├── config.py        # Settings (API Keys, Model selection)
├── requirements.txt # Project dependencies
└── sample_data/     # Sandbox folder for all agent file operations
```
