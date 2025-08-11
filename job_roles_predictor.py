

def job_predictor(result):
  prompt=PromptTemplate.from_template("""
You are an AI career advisor.

Based on the candidate's skill summary below, identify suitable job roles that:
- Are real, standard industry job titles (avoid vague or generic terms like "assistant" without context).
- Are specific enough to be searchable on job boards (include field/domain if relevant, e.g., "Data Analyst" not "Analyst").
- Match the candidate's skills and likely career stage.
- Avoid duplicates or overly similar roles.

**Rules:**
- Output ONLY the ranked list.
- Each line must be in the exact format:
  <rank>.<job role> (Suitability Score: <score>/10): <short, friendly tone to say improvements required for the specific role, comma separated>
- Use motivating language (e.g., "can further strengthen...", "opportunity to deepen...", "would benefit from expanding...").
- No extra sentences, no explanations, no duplication of job titles.

Candidate Skill Summary:
{result}

"""
  )
  chain=LLMChain(llm=llm,prompt=prompt)
  return chain.run({"result":result})

