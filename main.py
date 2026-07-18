import re
import subprocess
from crewai import Crew, Process

# Import from our refactored package
from src.stitchflow.agents import agent_erp, agent_trends, agent_market, agent_reporter
from src.stitchflow.tasks import task_erp, task_trends, task_market, task_report, task_export_json

def latex_to_pdf(latex_text, filename_base="Procurement_Optimization_Report"):
    # Remove markdown code block wrappers if the LLM accidentally added them
    latex_text = re.sub(r'^```latex\n?', '', latex_text.strip(), flags=re.IGNORECASE)
    latex_text = re.sub(r'^```\n?', '', latex_text.strip())
    latex_text = re.sub(r'\n?```$', '', latex_text.strip())
    
    # Inject geometry package to fix margins and prevent Overfull \hbox
    if "\\usepackage[margin=1in]{geometry}" not in latex_text:
        latex_text = re.sub(r'(\\documentclass\[.*?\]\{.*?\}|\\documentclass\{.*?\})', r'\1\n\\usepackage[margin=1in]{geometry}', latex_text, count=1)
        
    tex_filename = f"{filename_base}.tex"
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_text)
    
    # Run pdflatex
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], check=True)

def save_json_feed(json_text, filepath="dashboard/src/data.json"):
    # Remove markdown code block wrappers
    json_text = re.sub(r'^```json\n?', '', json_text.strip(), flags=re.IGNORECASE)
    json_text = re.sub(r'^```\n?', '', json_text.strip())
    json_text = re.sub(r'\n?```$', '', json_text.strip())
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json_text)

def main():
    # Define Crew
    crew = Crew(
        agents=[agent_erp, agent_trends, agent_market, agent_reporter],
        tasks=[task_erp, task_trends, task_market, task_report, task_export_json],
        process=Process.sequential
    )

    try:
        crew.kickoff()
        
        # Extract specific task outputs
        latex_output = task_report.output.raw
        json_output = task_export_json.output.raw
        
        print("Updating Dashboard JSON feed...")
        save_json_feed(json_output)
        print("Success! Dashboard JSON updated.")
        
        print("Generating PDF via pdflatex...")
        try:
            latex_to_pdf(latex_output)
            print("Success! PDF updated.")
        except Exception as e:
            print(f"PDF generation had warnings or failed: {e}")
            
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()

