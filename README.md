# AI Agent CLI Tool

## Overview
This project implements a conversational Command Line Interface (CLI) agent, inspired by tools like Cursor and Windsurf. The agent is designed to accept natural language instructions directly from the terminal and autonomously execute tasks.  
+1

The primary objective of this specific implementation is to clone the Scaler Academy website by reasoning through the task iteratively and generating fully functional HTML, CSS, and JavaScript files (including a Header, Hero Section, and Footer). The final output visually resembles the Scaler website and is ready to be opened in a browser.  
+1

## Features
* **Conversational CLI:** Chat with the AI agent directly in your terminal using natural language.  
* **Autonomous Reasoning Loop:** The agent does not generate everything in a single step. It follows a ReAct-style loop: START -> THINK -> TOOL -> OBSERVE -> OUTPUT to methodically build the project.  
+1
* **Tool Calling Capabilities:** The agent is equipped with specific Python tools to fetch website data, execute terminal commands, and write code to files.  
* **Built-in Security Guardrail:** A secondary LLM validation step acts as a security guard to evaluate terminal commands before execution, blocking dangerous actions (like `rm` or `sudo`) while allowing safe project-building commands (like `mkdir` or `touch`).  
* **Rich Terminal Output:** Utilizes the `rich` library to provide beautifully styled, color-coded terminal outputs indicating the agent's current step (Thinking, Tool Calling, Observing, Outputting).  

## Tech Stack
* **Language:** Python 3  
* **LLM Integration:** `huggingface_hub` (`AsyncInferenceClient`)  
* **Data Parsing:** `beautifulsoup4` (for scraping and cleaning source HTML)  
* **Structuring & Validation:** `pydantic` and `langchain_core` (for enforcing strict JSON outputs from the LLM)  
* **Terminal UI:** `rich`
  
## Project Structure
* **main.py:** The core application loop. It handles user input, manages the conversation history, maps LLM tool calls to actual Python functions, and coordinates the execution and security checks.  
+1
* **models.py:** Contains the Pydantic models (`SafetyStatus`, `LlmResponse`) that enforce the strict JSON structure required from the LLM, as well as the `rich` styling configurations.  
* **prompts.py:** Houses the highly specific system prompts. It includes the `getMainLLmPrompt` for the autonomous cloning agent and the `getSecuritySysPrompt` for the safety guardrail agent.  
+1
* **requirements.txt:** Project dependencies.  
* **.env:** Configuration file for API keys and Model IDs.  

## Tools Available to the Agent
* **get_website_html(url):** Fetches the raw HTML of a target website and strips out unnecessary tags (like scripts, images, and SVGs) to provide a clean structural reference.  
* **executeCommandTool(command):** Runs Linux terminal commands (e.g., creating directories) after passing them through the LLM security checker.  
* **write_file(filepath, content):** Safely writes the generated HTML, CSS, and JS code to the local file system.  

## Setup and Installation

**1. Clone the repository and navigate to the directory**

**2. Create and activate a virtual environment (Recommended)**
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`