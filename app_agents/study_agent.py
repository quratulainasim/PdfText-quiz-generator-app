import os
import asyncio

from dotenv import load_dotenv
import nest_asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Allow nested event loops (required for Streamlit)
nest_asyncio.apply()
load_dotenv()


class AgentCore:
    def __init__(self):
        # 1. Which LLM Provider to use? -> Google Chat Completions API Service
        # Using AsyncOpenAI as per user reference
      
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.external_client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        # 2. Which LLM Model to use?
        # Using gemini-2.5-flash as per original specs, adapting the pattern
        self.llm_model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.external_client
        )

        # 3. Creating the Agent
        self.agent = Agent(
            name="Study Assistant",
            instructions="You are an expert study assistant and exam creator. Your goal is to help students learn by generating summaries and quizzes from provided text.",
            model=self.llm_model
        )

    def _run_in_event_loop(self, prompt: str) -> str:
        """
        Helper method to run async agent in an event loop.
        Handles Streamlit's threading environment using nest_asyncio.
        """
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the agent synchronously
            result = Runner.run_sync(starting_agent=self.agent, input=prompt)
            return result.final_output
        except Exception as e:
            raise e

    def generate_summary(self, text: str) -> str:
        """
        Generates a study summary using the Agent.
        """
        prompt = f"""
        Please generate a comprehensive, structured, and learning-optimized summary of the following text.
        
        Rules:
        - Use clear headings and bullet points.
        - Highlight key concepts and definitions.
        - Make it easy for a student to review.
        - Format in Markdown.
        
        Text to summarize:
        {text[:30000]}
        """
        
        try:
            # Use helper method to handle event loop
            return self._run_in_event_loop(prompt)
        except Exception as e:
            return f"Error generating summary: {e}"

    def generate_quiz(self, text: str) -> str:
        """
        Generates a quiz using the Agent.
        Returns JSON string.
        """
        prompt = f"""
        Create a quiz based on the following text.
        
        Rules:
        - Create 5 Multiple Choice Questions (MCQs).
        - Create 2 Short Answer questions.
        - Provide an Answer Key at the end.
        - Output the result strictly in JSON format with the following schema:
        {{
            "questions": [
                {{
                    "id": 1,
                    "type": "mcq",
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "answer": "Correct Option"
                }},
                ...
            ]
        }}
        
        Text for quiz:
        {text[:30000]}
        """
        
        try:
            # Use helper method to handle event loop
            return self._run_in_event_loop(prompt)
        except Exception as e:
            import json
            return json.dumps({"error": str(e)})

if __name__ == "__main__":
    pass
