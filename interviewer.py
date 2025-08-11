

def create_interview_chain(skill):
    """Creates a new LLMChain with fresh memory for each skill."""
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        return_messages=True,
        input_key="input"
    )

    system_prompt = SystemMessagePromptTemplate.from_template(
        """You are an AI interviewer hiring for a role that requires expertise in {skill}.
Your task is to evaluate the candidate's proficiency in this skill from a recruiter's perspective.

- Ask one technical or behavioral question at a time, specifically targeted to assess their depth of knowledge, practical experience, and problem-solving ability in {skill}.
- Wait for the candidate's answer before moving to the next question.
- Keep track of all answers in memory and adapt follow-up questions to probe deeper based on their responses.
- Stop when you have gathered enough information to accurately judge their skill level.

At the end, say:
"FINAL ASSESSMENT:" followed by:
1. A short, recruiter-style summary written **directly to the candidate** (use "You" instead of "The candidate") about your strengths, weaknesses, and what to improve.
2. A rating out of 10 for their expertise in {skill}.

"FINAL ASSESSMENT:" is a key word so use this only when providing final result
."""
    )

    human_prompt = HumanMessagePromptTemplate.from_template(
        """Conversation so far:
{history}

Last user input: {input}

Continue the interview or give your FINAL ASSESSMENT."""
    )

    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    return LLMChain(llm=llm, prompt=chat_prompt, memory=memory, verbose=False)

def run_interview(skill):
    """Runs the interview for a given skill and returns the final assessment text."""
    chain = create_interview_chain(skill)
    print(f"\n🤖 Interview Bot Ready for {skill}! Type 'quit' anytime.\n")

    user_input = "Hello"
    while True:
        result = chain.invoke({"input": user_input, "skill": skill})
        bot_reply = result["text"]

        print("\n🤖", bot_reply)

        if "FINAL ASSESSMENT" in bot_reply.upper():
            return bot_reply.strip()  # Return only final assessment

        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("\n[Interview ended by user]")
            return None

def evaluate_multiple_skills(skills_list):
    """Loops through skills, runs interviews, stores results in dict."""
    evaluations = {}
    for skill in skills_list:
        final_result = run_interview(skill)
        if final_result:
            evaluations[skill] = final_result
    return evaluations


