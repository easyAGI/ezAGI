
# AUTOMIND.md

The automind folder within the ezAGI project contains essential components that enable advanced reasoning, decision-making, and logic processing for the AGI system. Below is a detailed description of the four primary files in this directory: SocraticReasoning.py, agi.py, logic.py and openmind.py

# SocraticReasoning.py

The SocraticReasoning.py module implements a Socratic reasoning engine that interacts with a chatter model to add, challenge, and draw conclusions from premises. It aims to simulate a logical reasoning process, allowing the AGI to engage in structured dialogues and make informed decisions based on logical premises.

Key Features:

    Initialization: Sets up logging, defines file paths for saving premises, non-premises, conclusions, and truth tables, and ensures necessary directories exist.
    Premise Management: Provides methods to add, validate, and remove premises. Stores valid premises and logs invalid ones.
    Conclusion Drawing: Attempts to draw conclusions based on the current set of premises and validates these conclusions using logic tables.
    Logging: Implements detailed logging mechanisms for general operations and specific errors.
    Interactive Loop: Includes an interactive loop for user commands to add, challenge premises, and draw conclusions.

# agi.py

The agi.py file defines the AGI (Artificial General Intelligence) class, which uses Socratic reasoning to learn from data and make decisions. This file integrates various components such as the chatter model and memory management to facilitate the AGI's decision-making processes.

Key Features:

    AGI Class: Initializes with a chatter instance and Socratic reasoning. Provides methods to learn from data and make decisions based on propositions.
    EasyAGI Class: Manages API keys, initializes the AGI, and handles memory initialization. Contains the main loop to interact with the environment and make decisions.
    Main Loop: Continuously interacts with the environment, processes input data, learns from it, and makes decisions. Logs and stores dialog entries in memory.
    Logging: Includes basic logging setup and ensures proper logging of decisions and interactions.

# logic.py

The logic.py module provides the LogicTables class, which manages logical variables, expressions, and truth tables. It evaluates logical expressions and ensures their validity, supporting the reasoning processes of the AGI.

Key Features:

    Initialization: Sets up logging and ensures directories for logs exist.
    Variable and Expression Management: Methods to add variables and expressions while ensuring they are not duplicated.
    Truth Table Generation: Generates and displays truth tables for the current set of variables and expressions.
    Evaluation and Validation: Evaluates logical expressions and validates them as truths or tautologies.
    Logging: Implements detailed logging for all operations and stores logs in both general and memory-specific files.
    Output Methods: Outputs beliefs and truths to JSON files, ensuring structured storage of logical data.
    
# openmind.py

The openmind.py module orchestrates the internal reasoning loop for continuous AGI reasoning without user interaction. openmind integrates with automind and thus agi components in the automind folder managing memory, handling API keys, and interacts with various language models (LLMs) as a modular extension of the easyAGI UIUX components. openmind simplifies interaction with the automind reasoning engine and the webmind ml compononents of the easyAGI framework to produce conclusions from internal reasoning to make_decision from Socratic Reasoning.

Key Features:

    Initialization: Sets up API managers and AGI instances, initializes memory, and prepares internal queues for handling asynchronous tasks.
    API Key Management: Provides methods to add, delete, and list API keys, ensuring dynamic integration with different LLM services.
    Main Loop: Implements the main asynchronous loop to handle internal reasoning and user input concurrently for continuous processing and response generation of conclusions as thoughts.
    Reasoning Loop: Continuously processes prompts using the AGI instance and updates internal conclusions, saving these to appropriate log files.
    Integration: Seamlessly integrates with the FundamentalAGI class for reasoning and various chatter models for handling input responses.
    Logging: Detailed logging of internal operations, API key management, and reasoning conclusions, ensuring traceability and debugging capabilities.



each module provides example usage to demonstrate how classes and methods can be utilized within the ezAGI project or your AGI project framework. Understanding the practical applications of the classes and their methods ensures seemless modular expansion of ezAGI as a framework for practical reasoning appliations.
