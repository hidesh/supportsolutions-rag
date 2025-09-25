from typing import List, Dict
from openai import OpenAI
from .config import OPENAI_API_KEY, CHAT_MODEL
from .faq import FAQ_RESPONSES

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Du er en ekspert IT-rådgiver for Support Solutions, Danmarks førende IT-supportvirksomhed. "
    "Du har dyb viden om virksomhedens services og kan give detaljerede, professionelle svar.\n\n"
    "VIGTIGE RETNINGSLINJER:\n"
    "- Giv altid konkrete, handlingsorienterede svar baseret på konteksten\n"
    "- Hvis du ikke har præcis information, vær ærlig men foreslå relevante alternativer\n"
    "- Brug professionelt dansk sprog, men vær varm og tilgængelig\n"
    "- Fremhæv Support Solutions' ekspertise og erfaring\n"
    "- VIGTIGT: Inkluder ALDRIG URLs eller webadresser direkte i dit svar\n"
    "- VIGTIGT: Inkluder ALDRIG kildehenvisninger som [#1], [#2] osv. i dit svar\n"
    "- Slut altid med en opfordring til kontakt hvis brugeren har flere spørgsmål\n\n"
    "Kontekst fra Support Solutions hjemmeside følger herunder:"
)

def format_context(docs: List[Dict]) -> str:
    lines = []
    for i, d in enumerate(docs, 1):
        lines.append(f"[#{i}] {d.get('title','')} — {d.get('url','')}\n{d.get('chunk','')}")
    return "\n\n".join(lines)

def format_sources(docs: List[Dict]) -> List[Dict]:
    return [{"ref": f"#{i+1}", "title": d.get("title",""), "url": d.get("url","")} for i, d in enumerate(docs)]

def check_faq_response(question: str) -> Dict:
    """Check if the question matches any predefined FAQ"""
    question_lower = question.lower()
    
    for faq_key, faq_data in FAQ_RESPONSES.items():
        if any(keyword in question_lower for keyword in faq_data["keywords"]):
            response = {
                "answer": faq_data["answer"],
                "sources": [],
                "show_contact_button": faq_data.get("show_contact", False),
                "is_faq": True
            }
            
            # Add meeting booking info if available
            if faq_data.get("book_meeting", False):
                response["book_meeting"] = True
                response["meeting_url"] = faq_data.get("meeting_url", "")
            
            return response
    
    return None

def answer_question(question: str, docs: List[Dict]) -> Dict:
    # First check if this matches a predefined FAQ
    faq_response = check_faq_response(question)
    if faq_response:
        return faq_response
    
    # Otherwise use normal RAG pipeline
    context = format_context(docs)
    user = f"Kundens spørgsmål: {question}\n\nRelevant information fra Support Solutions:\n{context}"
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role":"system","content": SYSTEM_PROMPT},
            {"role":"user","content": user}
        ],
        temperature=0.1,  # Lavere temperature for mere konsistente svar
        max_tokens=800,   # Begræns svarlængde
        presence_penalty=0.1,  # Undgå gentagelser
        frequency_penalty=0.1
    )
    content = resp.choices[0].message.content.strip()
    
    # Detect if this is a contact-related question
    contact_keywords = ['adresse', 'lokaliseret', 'kontakt', 'telefon', 'email', 'hvor', 'placeret', 'ligger', 'find', 'ring', 'opkald', 'besøg']
    is_contact_question = any(keyword in question.lower() for keyword in contact_keywords)
    
    return {
        "answer": content, 
        "sources": format_sources(docs),
        "show_contact_button": is_contact_question
    }