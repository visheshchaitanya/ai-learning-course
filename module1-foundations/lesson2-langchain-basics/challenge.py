"""
Lesson 2 Challenge: Multi-Step Research Assistant

Build a research assistant that:
1. Takes a research topic
2. Generates 3 research questions
3. Answers each question in parallel
4. Synthesizes findings into a summary

Use LCEL for composition and parallel execution.
"""

from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from operator import itemgetter


def research_assistant(topic: str):
    """Main research assistant function"""
    print(f"Researching: {topic}\n")
    print("=" * 60)
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # TODO: Step 1 - Generate 3 research questions
    # Create a prompt that asks for 3 numbered questions about the topic
    # Parse the output to extract the questions
    
    questions_prompt = ChatPromptTemplate.from_template(
        "Generate 3 specific research questions about {topic}. "
        "Format as:\n1. [question]\n2. [question]\n3. [question]"
    )
    
    # TODO: Create a chain to generate questions
    questions_chain = questions_prompt | llm | StrOutputParser()
    
    print("\n📋 Generating research questions...")
    questions_text = questions_chain.invoke({"topic": topic})
    print(f"\nQuestions:\n{questions_text}\n")
    
    # TODO: Parse questions into a list
    # You can use simple string splitting or regex
    questions = parse_questions(questions_text)
    
    # TODO: Step 2 - Answer each question in parallel
    # Create a chain that answers a single question
    
    answer_prompt = ChatPromptTemplate.from_template(
        "Answer this research question in 2-3 sentences: {question}"
    )
    
    # TODO: Create answer chain
    answer_chain = answer_prompt | llm | StrOutputParser()
    
    # TODO: Create parallel chains for all 3 questions
    
    # Use RunnableParallel to run them simultaneously
    parallel_answer_chain = RunnableParallel(
        answer0= itemgetter("answer0") | answer_chain,
        answer1= itemgetter("answer1") | answer_chain,
        answer2= itemgetter("answer2") | answer_chain
    )
    
    print("🔍 Researching answers in parallel...\n")
    # answers = parallel_answer_chain.invoke({...})
    answers = parallel_answer_chain.invoke({
        "answer0": {"question": questions[0]},
        "answer1": {"question": questions[1]},
        "answer2": {"question": questions[2]}
    })
    
    # TODO: Print each Q&A pair
    for i in range(3):
        print(f"Question {i+1}: {questions[i]}")
        print(f"Answer {i+1}: {answers[f'answer{i}']}\n")
    
    # TODO: Step 3 - Synthesize findings
    findings = "\n".join([f"Question: {q}\nAnswer: {a}" for q, a in zip(questions, answers)])
    synthesis_prompt = ChatPromptTemplate.from_template(
        "Based on these research findings, write a comprehensive summary:\n\n"
        "{findings}\n\n"
        "Summary:")
    synthesis_chain = synthesis_prompt | llm | StrOutputParser()
    print("\n" + "=" * 60)
    print("📝 Final Summary:\n")
    
    # TODO: Stream the final summary
    for chunk in synthesis_chain.stream({"findings": findings}):
        print(chunk, end="", flush=True)
    
    print("\n" + "=" * 60)


def parse_questions(text: str) -> list[str]:
    """Parse numbered questions from text"""
    # TODO: Implement parsing logic
    # Simple approach: split by newlines and filter lines starting with numbers
    lines = text.strip().split('\n')
    questions = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Remove number and period
            question = line.split('.', 1)[1].strip() if '.' in line else line
            questions.append(question)
    return questions


if __name__ == "__main__":
    # Test with a topic
    topic = input("Enter a research topic (or press Enter for 'Quantum Computing'): ").strip()
    if not topic:
        topic = "Quantum Computing"
    
    research_assistant(topic)
