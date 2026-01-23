"""
Lesson 2 Solution: Multi-Step Research Assistant
"""

from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


def parse_questions(text: str) -> list[str]:
    """Parse numbered questions from text"""
    lines = text.strip().split('\n')
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Remove number and period
            question = line.split('.', 1)[1].strip() if '.' in line else line
            questions.append(question)
    return questions


def research_assistant(topic: str):
    """Complete research assistant implementation"""
    print(f"Researching: {topic}\n")
    print("=" * 60)
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # Step 1: Generate 3 research questions
    questions_prompt = ChatPromptTemplate.from_template(
        "Generate 3 specific research questions about {topic}. "
        "Format as:\n1. [question]\n2. [question]\n3. [question]\n"
        "Only output the numbered questions, nothing else."
    )
    
    questions_chain = questions_prompt | llm | StrOutputParser()
    
    print("\n📋 Generating research questions...")
    questions_text = questions_chain.invoke({"topic": topic})
    print(f"\nQuestions:\n{questions_text}\n")
    
    # Parse questions into a list
    questions = parse_questions(questions_text)
    
    if len(questions) < 3:
        print("Warning: Could not parse 3 questions. Using fallback.")
        questions = [
            f"What is {topic}?",
            f"What are the applications of {topic}?",
            f"What are the challenges in {topic}?"
        ]
    
    # Step 2: Answer each question in parallel
    answer_prompt = ChatPromptTemplate.from_template(
        "Answer this research question in 2-3 sentences: {question}"
    )
    
    answer_chain = answer_prompt | llm | StrOutputParser()
    
    # Create parallel chains for all 3 questions
    parallel_answer_chain = RunnableParallel(
        answer1=answer_chain,
        answer2=answer_chain,
        answer3=answer_chain
    )
    
    print("🔍 Researching answers in parallel...\n")
    answers = parallel_answer_chain.invoke({
        "answer1": {"question": questions[0]},
        "answer2": {"question": questions[1]},
        "answer3": {"question": questions[2]}
    })
    
    # Print each Q&A pair
    print("=" * 60)
    for i, (q, a_key) in enumerate(zip(questions, ['answer1', 'answer2', 'answer3']), 1):
        print(f"\nQ{i}: {q}")
        print(f"A{i}: {answers[a_key]}")
    print("\n" + "=" * 60)
    
    # Step 3: Synthesize findings
    findings_text = ""
    for i, (q, a_key) in enumerate(zip(questions, ['answer1', 'answer2', 'answer3']), 1):
        findings_text += f"Question {i}: {q}\nAnswer {i}: {answers[a_key]}\n\n"
    
    synthesis_prompt = ChatPromptTemplate.from_template(
        "Based on these research findings about {topic}, write a comprehensive "
        "summary that integrates all the information:\n\n"
        "{findings}\n\n"
        "Write a cohesive summary in 3-4 sentences:"
    )
    
    synthesis_chain = synthesis_prompt | llm | StrOutputParser()
    
    print("\n📝 Final Summary:\n")
    
    # Stream the final summary
    for chunk in synthesis_chain.stream({
        "topic": topic,
        "findings": findings_text
    }):
        print(chunk, end="", flush=True)
    
    print("\n\n" + "=" * 60)
    print("\n✅ Research complete!")


if __name__ == "__main__":
    # Test with a topic
    topic = input("Enter a research topic (or press Enter for 'Quantum Computing'): ").strip()
    if not topic:
        topic = "Quantum Computing"
    
    try:
        research_assistant(topic)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
