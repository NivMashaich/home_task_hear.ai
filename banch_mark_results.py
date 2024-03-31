from gpt_missed_items_analyzer import GptMissedItemsAnalyzer
from llama_missed_item_analyzer import LlamaMissedItemsAnalyzer
from promptsDB import *
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

def save_results(results, file_path):
    with open(file_path, 'w') as file:
        file.write(results)

def main():
    try:
        with open('C:\\Users\\nivm\\OneDrive - AudioCodes Ltd\\Desktop\\ConversationAnalysisTool\\LlamaAdhernceResults.txt', 'r') as file:
            llama_results = file.read()
        with open('C:\\Users\\nivm\\OneDrive - AudioCodes Ltd\\Desktop\\ConversationAnalysisTool\\GptAdherenceResults.txt', 'r') as file:
            gpt_results = file.read()
        
        chat = ChatOpenAI(verbose=True, model="gpt-4-turbo-preview", temperature=0.0)

        adhernce_system = Prompts.AdherenceAndImprovmentsSystemPrompt.__doc__
        adhernce_prompt = Prompts.AdherenceAndImprovmentsPrompt.__doc__
        adhernce_prompt_template = f"{adhernce_system}\n{adhernce_prompt}"

        system_prompt = Prompts.BenchMarkSystemPrompt.__doc__
        human_prompt = Prompts.BenchMarkPrompt.__doc__

        prompt_template = PromptTemplate.from_template(
            template=f"{system_prompt}\n{human_prompt}",
            kwargs=['llama_results', 'gpt_results', 'prompt']
        )

        formatted_prompt = prompt_template.format(
            llama_results=llama_results,
            gpt_results=gpt_results,
            prompt=adhernce_prompt_template
        )

        chat_response = chat.invoke(formatted_prompt)

        # Assuming GptMissedItemsAnalyzer has a save_results method similar to the one in your previous classes
        save_results(chat_response.content, 'BenchMarkResults.txt')
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise
    
    
if __name__ == "__main__":
    main()
    
    
    
    
        
    