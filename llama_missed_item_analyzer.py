import json
import logging
import replicate
from typing import Dict, List, Union

from langchain_core.prompts import PromptTemplate
from promptsDB import Prompts

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaMissedItemsAnalyzer:
    def __init__(self, 
                 company_name: str, 
                 script_path: str, 
                 transcript_path: str, 
                 model_name: str = "meta/llama-2-70b-chat", 
                 temperature: float = 0.1, 
                 max_new_tokens: int = 3000,
                 ) -> None:
        
        """
        Initializes the LlamaMissedItemsAnalyzer with the given parameters.

        Args:
            company_name: The name of the company.
            script_path: The file path to the script JSON.
            transcript_path: The file path to the transcript text.
            model_name: The name of the open-source model to use.
            temperature: The temperature for the model.
            max_new_tokens: The maximum number of new tokens for the model.
        """
        self.company_name = company_name
        self.script_path = script_path
        self.transcript_path = transcript_path
        self.model_name = model_name
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
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

    def generate_prompt(self) -> str:
        """
        Generates the prompt for the language model based on the script and transcript.

        Returns:
            A string containing the generated prompt.
        """
        system_prompt = Prompts.SystemLlamaMissedItemPrompts.__doc__
        human_prompt = Prompts.LlamaMissedItemPrompt.__doc__
        prompt_template = PromptTemplate(
            input_variables=['script', 'company_name', 'transcript'],
            template=f"{system_prompt}\n{human_prompt}"
        )
        return prompt_template.format(script=self.script, company_name=self.company_name, transcript=self.transcript)
    
    def analyze_missed_items(self) -> List[str]:
        """
        Analyzes the transcript for missed items using the open-source model and returns the result.

        Returns:
            A list of strings containing the analysis results.
        """
        try:
            prompt = self.generate_prompt()
            input_params = {
                "prompt": prompt,
                "temperature": self.temperature,
                'max_new_tokens': self.max_new_tokens,
            }
            results = ''
            output_iterator = replicate.run(self.model_name, input=input_params)
            for output in output_iterator:
                results += ' '.join(str(output).split('\n'))
            # Save the results to a file
            self.save_results(results, 'missed_items_llama.txt')
            return results
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
    
    def save_results(self, results: str, output_path: str = 'missed_items_llama.txt'):
        try:
            with open(output_path, 'w') as file:
                file.write(results)
                logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise
        
    def get_missed_items(self, results_path: str = 'missed_items_llama.txt') -> List[str]:
        try:
            with open(results_path, 'r') as file:
                missed_items = file.read()
                return missed_items
        except Exception as e:
            logger.error(f"Error reading results: {e}")
            raise
            
  
        
    def analyze_adherence_percentage(self) -> str:
        """
        Analyzes the adherence percentage of the transcript to the script.

        Returns:
            A string containing the adherence percentage and suggestions for improvement.
        """
        missed_items = self.get_missed_items()
        system_prompt = Prompts.AdherenceAndImprovmentsSystemPrompt.__doc__
        human_prompt = Prompts.AdherenceAndImprovmentsPrompt.__doc__
        prompt_template = PromptTemplate.from_template(
            template=f"{system_prompt}\n{human_prompt}",
            template_format="f-string",  # Use f-string format
            kwargs={'script', 'missed_items'}  # Define input variables
        )
        
        results = ''
        try:
            prompt = prompt_template.format(script=self.script, missed_items=missed_items)
            logger.info(f"Prompt generated successfully.")
            print(prompt)
            input_params = {
                "prompt": prompt,
                "temperature": self.temperature
            }
            
            output_iterator = replicate.run(self.model_name, input=input_params)
            for output in output_iterator:
                results += ' '.join(str(output).split('\n'))
                
            self.save_results(results, 'LlamaAdhernceResults.txt')
            logger.info(f"Analysis results are saved in {results}")
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            raise
            
            
        

        

