# Conversation Analysis scripts for Hear.ai

## Initial Assumptions:

- Content Format: It is assumed that the content will be in JSON format. 
  The information was extracted from a PDF and structured using OpenAI's GPT-4.
- Conversation Chunking: For testing purposes, it is assumed that the full conversation fits into one chunk. 
  In a real-world scenario, the conversation would be chunked into smaller parts for accurate analysis.
- Modularity: The tool is designed to be modular, allowing for easy changes to models, prompts, and role scripts for convenience and flexibility.


# Overview
The script is designed to analyze conversation transcripts against a provided script.
It identifies missed items and calculates the adherence percentage to the script. 


# Results file:
- missed_items_gpt.json: Holds the extracted missed items as json
- missed_items_llama.txt: Holds the extrected missed items 
- GptAdherenceResults.txt: Holds the adherene result
- LlamaAdhernceResults: Holds the llama adherence results
- BenchMarkResults.txt: Holds the benchmark results from both models.
- promptsDB.py: contains all the prompts that were used in this tool
  

# Directory Structure:
- gpt_missed_items_analysis.py: This is a gpt utility script that is used to analyze the conversation transcript and calculate the missed items 
  Using langchain for prompt managment.
- llama_missed_items_analysis.py: This is a llama utility script that is used to analyze the conversation transcript and calculate the missed items
  Using replicate library.
- prompts.py: This Module contain the prompts that are used in the scripts.


# Features
- Missed Items Analysis: Identifies items from the script that were missed during the conversation.
- Adherence Percentage: Calculates the percentage of adherence to the script based on the missed items.
- benchmarking: The tool can be used to benchmark different models for conversation analysis.


# Usage
- Required Environment Variables
- OPENAI_API_KEY: Your API key for OpenAI. Required for using OpenAI's models.
- REPLICATE_API_TOKEN: Your API token for Replicate. Required for using Replicate's models
  
- Install the required dependencies: pip install -r requirements.txt
- Run the tool with the desired options:

- Extract missed items using llama : python main.py --model llama --script path/to/script.json --transcript path/to/transcript.txt
- Extract missed items using gpt : python main.py --model gpt --script path/to/script.json --transcript path/to/transcript.txt 
- Use the --adherence flag to calculate the adherence percentage instead of missed items
  Example : python main.py --model gpt --adherence --script path/to/script.json --transcript path/to/transcript.txt --adherence





# RoadMap 
# Phase 2: Future Improvements
**For the next phase, the following improvements are considered:**

- Test different types of prompt engineering techniques.
- Develop automated agents to streamline the conversation analysis process.
- Long Input Handling: Implement embeddings to handle and chunk long inputs for better accuracy.
- Cosine Similarity: Use cosine similarity to measure the similarity between the script and transcript.
- Sentiment Analysis: Integrate a classification model to score the tone of the conversation based on positive and negative analysis.
- MetaData analysis: Extract the metadata from the conversation and analyze it for better insights.
- Database Integration: Store results, transcripts, and scripts in a database for regression testing and prompt efficiency evaluation.
- Model Evaluation: Utilize frameworks like LangFuse to evaluate model accuracy and performance.
- Comprehensive Evaluation: Evaluate models based on criteria such as consistency, accuracy, token usage, format adherence, response time, etc..
- Remove Hardcoded Values: Remove hardcoded values and make the tool more flexible and configurable.
- Developing an ELO Rating system for rate models continuously and automated





# Conclusion
- This tool serves as a demo for analyzing conversation transcripts and calculating script adherence. 
- The next phase aims to enhance the tool's accuracy, efficiency, and functionality for better conversation analysis and model evaluation.