import argparse
from gpt_missed_items_analyzer import GptMissedItemsAnalyzer
from llama_missed_item_analyzer import LlamaMissedItemsAnalyzer 

def main():
    parser = argparse.ArgumentParser(description="Analyze missed items in a conversation transcript.")
    parser.add_argument("--model", choices=["gpt", "llama"], required=True, help="The model to use for analysis (gpt or llama).")
    parser.add_argument("--adherence", action="store_true", help="Analyze adherence percentage instead of missed items.")
    parser.add_argument("--company", default="BrightPath Health Insurance", help="The name of the company.")
    parser.add_argument("--script", default="data\\script_list.json", help="The file path to the script JSON.")
    parser.add_argument("--transcript", default="data\\agent_call_transcript.txt", help="The file path to the transcript text.")
    parser.add_argument("--results", default="results.txt", help="The file path to save the results.")

    args = parser.parse_args()

    if args.model == "gpt":
        analyzer = GptMissedItemsAnalyzer(company_name=args.company, script_path=args.script, transcript_path=args.transcript)
        if args.adherence:
            results = analyzer.analyze_adherence_percentage()
        else:
            results = analyzer.analyze_missed_items()
    
    elif args.model == "llama":
        analyzer = LlamaMissedItemsAnalyzer(company_name=args.company, script_path=args.script, transcript_path=args.transcript)
        if args.adherence:
            results = analyzer.analyze_adherence_percentage()
        else:
            results = analyzer.analyze_missed_items()
    
    print(f"Analysis results: {results}")

if __name__ == "__main__":
    main()
