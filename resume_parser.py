

def resume_parser(file_path: str):
    """
    Parse a resume (.pdf or .docx) and return structured info + skills list.

    Args:
        file_path (str): Path to the resume file.

    Returns:
        dict: Contains Name, Phone, Email, Projects, Certifications, Skills, Experience,
              Achievements, and Parsed Skills List.
    """



    # 1. Load document
    if file_path.endswith(".docx"):
        documents = docxloader(file_path).load()
    elif file_path.endswith(".pdf"):
        documents = pdfloader(file_path).load()
    else:
        raise ValueError("Unsupported file type. Use .docx or .pdf")

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 3. Create vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(texts, embeddings)

    # 4. RetrievalQA for structured extraction
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

    output = {
        "Name": qa_chain.run("What is the name?"),
        "Phone": qa_chain.run("What is the contact number?"),
        "Email": qa_chain.run("What is the mail id?"),
        "Projects": qa_chain.run("List the projects done"),
        "Certifications": qa_chain.run("List the certifications"),
        "Skills": qa_chain.run("List the skills"),
        "Experience": qa_chain.run("What is the experience in one line, if not mentioned print fresher"),
        "Achievements": qa_chain.run("List the achievements, if not mentioned print None")
    }

    # 5. Prompt for skill expansion
    prompt = PromptTemplate.from_template(
        """
        You are an expert resume parser. Your task is to extract a **complete list** of skills
        the candidate possesses based on the provided details.

        **Important:**
        - Include both explicit skills (directly mentioned) and implicit skills (that can be
          inferred from projects, certifications, education, tools, or technologies mentioned).
        - Include programming languages, frameworks, libraries, tools, platforms, and
          domain-specific expertise.
        - If a project or certification implies knowledge of a skill, include it even if
          not directly written.
        - Include relevant concepts if projects indicate them.

        **Candidate Details:**
        Projects: {projects}
        Skills: {skills}
        Certifications: {certificates}
        Experience: {experience}
        Achievements: {achievements}

        Output format: A valid Python list of skills (strings), without explanation.
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    summary = chain.run({
        "certificates": output["Certifications"],
        "achievements": output["Achievements"],
        "projects": output["Projects"],
        "skills": output["Skills"],
        "experience": output["Experience"]
    })

    # 6. Parse skills list
    match = re.search(r"\[.*?\]", summary, re.DOTALL)
    if match:
        skills_text = match.group(0)
        skills_list = [s.strip(" '\"\n") for s in skills_text.strip("[]").split(",") if s.strip()]
    else:
        skills_list = []

    output["Parsed_Skills_List"] = skills_list

    return output

