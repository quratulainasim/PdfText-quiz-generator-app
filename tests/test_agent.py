import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.study_agent import AgentCore

def test_agent():
    print("Initializing Agent...")
    try:
        agent = AgentCore()
    except Exception as e:
        print(f"Failed to init agent: {e}")
        return

    sample_text = """
    Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the aid of chlorophyll. 
    Photosynthesis in plants generally involves the green pigment chlorophyll and generates oxygen as a byproduct.
    The process of photosynthesis is commonly written as: 6CO2 + 6H2O → C6H12O6 + 6O2.
    This means that the reactants, six carbon dioxide molecules and six water molecules, are converted by light energy captured by chlorophyll 
    into a sugar molecule and six oxygen molecules, the products.
    """

    print("\nTesting Summary Generation...")
    summary = agent.generate_summary(sample_text)
    print("Summary Output:")
    print(summary[:200] + "..." if len(summary) > 200 else summary)

    print("\nTesting Quiz Generation...")
    quiz = agent.generate_quiz(sample_text)
    print("Quiz Output:")
    print(quiz[:200] + "..." if len(quiz) > 200 else quiz)

if __name__ == "__main__":
    test_agent()
