import json
import logging
from typing import Dict, List, Union
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from promptsDB import Prompts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GptMissedItemsAnalyzer:
    
    def __init__(self, 
                 company_name: str, 
                 script_path: str, 
                 transcript_path: str, 
                 model_name: str = "gpt-4", 
                 temperature: float = 0.0,
                 ) -> None:
        """
        Initializes the MissedItemsAnalyzer with the given parameters.

        Args:
            company_name: The name of the company.
            script_path: The file path to the script JSON.
            transcript_path: The file path to the transcript text.
            model_name: The name of the language model to use.
            temperature: The temperature for the language model.
        """
        self.company_name = company_name
        self.script_path = script_path
        self.transcript_path = transcript_path
        self.model_name = model_name
        self.temperature = temperature
        self.llm = ChatOpenAI(temperature=self.temperature, model=self.model_name)
        self.script, self.transcript = self._load_data()


    def _load_data(self) -> Union[Dict, str]:
        """
        Loads the script and transcript from their respective file paths.

        Returns:
            A tuple containing the script (as a dictionary) and the transcript (as a string).
        """
        try:
            with open(self.script_path, 'r') as json_file:
                script = json.load(json_file)
            with open(self.transcript_path, 'r') as file:
                transcript = file.read()
            return script, transcript
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise

    def generate_prompt(self) -> ChatPromptTemplate:
        """
        Generates the prompt for the language model based on the script and transcript.

        Returns:
            A ChatPromptTemplate object containing the generated prompt.
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(Prompts.MissedItemsSystemPrompt.__doc__)
        human_message_prompt = HumanMessagePromptTemplate.from_template(Prompts.MissedItemsPrompt.__doc__)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        return chat_prompt


    def analyze_missed_items(self) -> str:
        """
        Analyzes the transcript for missed items and returns the result in JSON format.

        Returns:
            A JSON string containing the analysis results.
        """
        try:
            prompt = self.generate_prompt()
            kwargs = {
                'script': self.script,
                'company_name': self.company_name,
                'transcript': self.transcript
            }
            result = self.llm.invoke(prompt.format_messages(**kwargs))
            content = result.to_json()['kwargs']['content']

            json_str = self.extract_valid_json_from_output(content)
            self.missed_items = json.loads(json_str)  

            
            self.save_results_as_json(json.loads(json_str))
            
            return json_str
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
    
    
    def extract_valid_json_from_output(self, output: str) -> str:
        """
        Extracts the valid JSON string from the output of the language model.

        Args:
            output: The output string from the language model.

        Returns:
            A valid JSON string.
        """
        start_index = output.find('[')
        end_index = output.rfind(']') + 1
        return output[start_index:end_index]
    
    def save_results(self, results: str, output_path: str = 'GptAdherenceResults.txt') -> None:
        """
        Saves the analysis results to the specified output path.

        Args:
            results: The analysis results to save.
            output_path: The file path to save the results.
        """
        try:
            with open(output_path, 'w') as file:
                file.write(results)
                logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise
    
    def save_results_as_json(self, results, output_path: str = 'missed_items_gpt.json') -> None:
        """
        This function saves the analysis results to a JSON file.

        Args:
            results: The analysis results to save.
            output_path: The file path to save the JSON file.
        """
        try:
            with open(output_path, 'w') as file:
                json.dump(results, file, indent=4)
                logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving results to JSON: {e}")
            raise
        
    def get_missed_items(self, results_path: str = 'missed_items_gpt.json') -> List[str]:
        try:
            with open(results_path, 'r') as file:
                results = file.read()
            missed_items = json.loads(results)
            return missed_items
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")


        
    def analyze_adherence_percentage(self) -> float:
        """
        Use Openai to Calculates the adherence percentage of the agent Using ChatOpenAI.
        
        Returns:
            A detailed review of the call transcript, Areas for improvement, and the adherence percentage.
            Also, The prompts that been used for this task.
        """
        
        try:
            missed_items = self.get_missed_items()
            system_message_prompt = SystemMessagePromptTemplate.from_template(Prompts.AdherenceAndImprovmentsSystemPrompt.__doc__)
            human_message_prompt = HumanMessagePromptTemplate.from_template(Prompts.AdherenceAndImprovmentsPrompt.__doc__)
            chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
            logger.info("Prompt generated successfully.")
            kwargs = {
                'script': self.script,
                'missed_items': missed_items
            }
            prompt = chat_prompt.format_messages(**kwargs)
            result = self.llm.invoke(prompt)
            self.save_results(result.content)
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
        
    def evaluate_performance(self, script, missed_items, gpt_results, llama_results):
        """
        Evaluate the performance of the GPT and Llama models based on the adherence percentage and missed items.
        
        Args:
            script: The script used for the sales call.
            missed_items: The list of missed items from the call transcript.
            gpt_results: The results from the GPT model.
            llama_results: The results from the Llama model.
        
        Returns:
            A dictionary containing the evaluation results.
        """
        
            

