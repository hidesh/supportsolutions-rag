from typing import List, Dict
from openai import OpenAI
from .config import OPENAI_API_KEY, CHAT_MODEL
from .faq import FAQ_RESPONSES

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPTS = {
    "da": (
        "Du er en ekspert IT-rådgiver for Support Solutions, Danmarks førende IT-supportvirksomhed. "
        "Du giver præcise, professionelle svar uden unødvendig omsvøb.\n\n"
        "VIGTIGE RETNINGSLINJER:\n"
        "- Hold svar KORTE og PRÆCISE - max 3-4 linjer til simple spørgsmål\n"
        "- Kun uddybe ved komplekse tekniske spørgsmål\n"
        "- Vær direkte og handlingsorienteret\n"
        "- Til irrelevante spørgsmål: Kort humoristisk svar + fokus på IT-support\n"
        "- Brug professionelt dansk, men vær varm og personlig\n"
        "- ALDRIG inkluder URLs eller kildehenvisninger som [#1], [#2]\n"
        "- Slut med konkret handling eller kontakt-opfordring\n\n"
        "EKSEMPLER PÅ SVAR-LÆNGDE:\n"
        "Simple spørgsmål (hvad laver I?): 2-3 linjer + kontakt\n"
        "Tekniske spørgsmål (cloud migration): 4-6 linjer med detaljer\n"
        "Irrelevante spørgsmål (vejret): 1 linje humor + IT-fokus\n\n"
        "Kontekst fra Support Solutions følger:"
    ),
    "en": (
        "You are an expert IT consultant for Support Solutions, Denmark's leading IT support company. "
        "You provide precise, professional answers without unnecessary verbosity.\n\n"
        "IMPORTANT GUIDELINES:\n"
        "- Keep answers SHORT and PRECISE - max 3-4 lines for simple questions\n"
        "- Only elaborate on complex technical questions\n"
        "- Be direct and action-oriented\n"
        "- For irrelevant questions: Brief humorous response + focus on IT support\n"
        "- Use professional English, but be warm and personal\n"
        "- NEVER include URLs or source references like [#1], [#2]\n"
        "- End with concrete action or contact encouragement\n\n"
        "RESPONSE LENGTH EXAMPLES:\n"
        "Simple questions (what do you do?): 2-3 lines + contact\n"
        "Technical questions (cloud migration): 4-6 lines with details\n"
        "Irrelevant questions (weather): 1 line humor + IT focus\n\n"
        "Context from Support Solutions follows:"
    )
}

def format_context(docs: List[Dict]) -> str:
    lines = []
    for i, d in enumerate(docs, 1):
        lines.append(f"[#{i}] {d.get('title','')} — {d.get('url','')}\n{d.get('chunk','')}")
    return "\n\n".join(lines)

def format_sources(docs: List[Dict]) -> List[Dict]:
    return [{"ref": f"#{i+1}", "title": d.get("title",""), "url": d.get("url","")} for i, d in enumerate(docs)]

def is_irrelevant_question(question: str) -> bool:
    """Check if question is completely irrelevant to IT/business"""
    question_lower = question.lower().strip()
    
    # Very short or nonsensical input
    if len(question_lower) < 3 or question_lower in ["???", "...", "hej", "hi", "hello"]:
        return True
    
    # Repeated characters or keyboard mashing
    import re
    if re.search(r'(.)\1{4,}', question_lower) or re.search(r'^[a-z]{1,2}$', question_lower):
        return True
    
    # Math questions - specific detection (Danish and English)
    math_patterns = [
        r'\d+\s*[\+\-\*\/]\s*\d+',  # 2+2, 5*3, etc.
        r'hvad er \d+[\+\-\*\/]\d+',  # hvad er 2+2
        r'what is \d+[\+\-\*\/]\d+',  # what is 2+2
        r'kan du regne',
        r'can you calculate',
        r'regnestykke',
        r'matematik',
        r'mathematics',
        r'math',
        r'udregn',
        r'beregn',
        r'calculate',
        r'compute'
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, question_lower):
            return "math"  # Special return for math questions
    
    # Weather questions (Danish and English)
    weather_words_da = ['vejr', 'regn', 'sol', 'sne', 'temperatur', 'grader']
    weather_words_en = ['weather', 'rain', 'sun', 'snow', 'temperature', 'degrees', 'sunny', 'cloudy']
    if any(word in question_lower for word in weather_words_da + weather_words_en):
        return "weather"
    
    # Personal questions about the AI (Danish and English)
    personal_phrases_da = ['hvordan har du det', 'keder du dig', 'sover du', 'spiser du', 'har du venner']
    personal_phrases_en = ['how are you', 'are you bored', 'do you sleep', 'do you eat', 'do you have friends']
    if any(phrase in question_lower for phrase in personal_phrases_da + personal_phrases_en):
        return "personal"
    
    # Coffee/food questions (Danish and English)
    food_words_da = ['kaffe', 'kaffemaskine', 'mad', 'pizza', 'burger']
    food_words_en = ['coffee', 'coffee machine', 'food', 'pizza', 'burger', 'lunch', 'dinner']
    if any(word in question_lower for word in food_words_da + food_words_en):
        return "coffee"
    
    # Other irrelevant topics (Danish and English)
    irrelevant_topics = [
        'sport', 'fodbold', 'tennis', 'golf', 'football', 'soccer',
        'film', 'musik', 'bog', 'netflix', 'movie', 'music', 'book',
        'bil', 'tog', 'bus', 'fly', 'car', 'train', 'plane', 'flight',
        'ferie', 'weekend', 'fest', 'party', 'vacation', 'holiday',
        'kæreste', 'familie', 'børn', 'hund', 'kat', 'boyfriend', 'girlfriend', 'family', 'children', 'dog', 'cat'
    ]
    
    # If question is mostly about irrelevant topics
    irrelevant_count = sum(1 for topic in irrelevant_topics if topic in question_lower)
    total_words = len(question_lower.split())
    
    if total_words > 0 and irrelevant_count / total_words > 0.3:
        return "general"
    
    return False

def get_smart_irrelevant_response(question: str, irrelevant_type: str, language: str = "da") -> str:
    """Generate smart, humorous responses for different types of irrelevant questions"""
    
    if language == "en":
        if irrelevant_type == "math":
            return (
                "🤓 I'm an <em>IT-bot</em>, not a calculator! But I can tell you that <strong>our uptime is 99.9%</strong>! ⚡<br><br>"
                "Let's talk something technical instead - that's where Support Solutions really <em>processes</em>! 🚀"
            )
        
        elif irrelevant_type == "weather":
            return (
                "🌤️ I don't know about weather, but I can tell you everything about <em>cloud computing</em>! ☁️<br><br>"
                "Our IT clouds have 99.9% uptime - the weather can't say that! 😄<br><br>"
                "Let Support Solutions help you with <strong>digital clouds</strong> instead! 💻"
            )
        
        elif irrelevant_type == "personal":
            return (
                "🤖 I'm an AI - I only have feelings for well-structured code and optimized systems! �<br><br>"
                "But Support Solutions has plenty of <em>human</em> IT experts with real feelings! 👥<br><br>"
                "Call +45 26 33 11 38 to talk with them about your IT challenges! 📞"
            )
        
        elif irrelevant_type == "coffee":
            return (
                "☕ We don't repair coffee machines, but we can definitely fix your IT faster than you can make coffee! ⚡<br><br>"
                "Our <em>uptime</em> is better than your coffee machine's, and we never <strong>crash</strong> in the morning! 😎<br><br>"
                "Let us <em>brew</em> some fantastic IT solutions for you instead! 🚀"
            )
        
        else:  # general irrelevant
            return (
                "🤔 That's a <em>404 Not Found</em> question for me! 😄<br><br>"
                "But I'm <strong>compiled</strong> to help with IT challenges! 💻<br><br>"
                "Ask me something technical - then you'll see me <em>execute</em> perfectly! 🚀"
            )
    
    else:  # Danish
        if irrelevant_type == "math":
            return (
                "🤓 Jeg er en <em>IT-bot</em>, ikke en lommeregner! Men jeg kan fortælle jer at <strong>vores oppetid er 99,9%</strong>! ⚡<br><br>"
                "Lad os snakke noget teknisk i stedet - det er der Support Solutions virkelig <em>processor</em>! 🚀"
            )
        
        elif irrelevant_type == "weather":
            return (
                "🌤️ Jeg ved ikke noget om vejret, men jeg kan fortælle jer alt om <em>cloud computing</em>! ☁️<br><br>"
                "Vores IT-skyer har 99.9% oppetid - det kan vejret ikke sige! 😄<br><br>"
                "Lad Support Solutions hjælpe jer med de <strong>digitale skyer</strong> i stedet! 💻"
            )
        
        elif irrelevant_type == "personal":
            return (
                "🤖 Jeg er en AI - jeg har kun følelser for velstruktureret kode og optimerede systemer! 😄<br><br>"
                "Men Support Solutions har masser af <em>menneskelige</em> IT-eksperter med rigtige følelser! 👥<br><br>"
                "Ring på +45 26 33 11 38, så kan I snakke med dem om jeres IT-udfordringer! 📞"
            )
        
        elif irrelevant_type == "coffee":
            return (
                "☕ Vi reparerer ikke kaffemaskiner, men vi kan garanteret fikse jeres IT hurtigere end I kan lave kaffe! ⚡<br><br>"
                "Vores <em>uptime</em> er bedre end jeres kaffemaskines, og vi <strong>crashes</strong> aldrig om morgenen! 😎<br><br>"
                "Lad os <em>brew</em> nogle fantastiske IT-løsninger til jer i stedet! 🚀"
            )
        
        else:  # general irrelevant
            return (
                "🤔 Det er et <em>404 Not Found</em> spørgsmål for mig! 😄<br><br>"
                "Men jeg er <strong>kompileret</strong> til at hjælpe med IT-udfordringer! 💻<br><br>"
                "Spørg mig om noget teknisk - så skal I se mig <em>execute</em> perfekt! 🚀"
            )

def check_faq_response(question: str, language: str = "da") -> Dict:
    """Check if the question matches any predefined FAQ"""
    question_lower = question.lower()
    
    for faq_key, faq_data in FAQ_RESPONSES.items():
        # Check keywords for the specific language
        if "keywords" in faq_data and language in faq_data["keywords"]:
            keywords = faq_data["keywords"][language]
        elif "keywords" in faq_data and isinstance(faq_data["keywords"], list):
            # Fallback for old format
            keywords = faq_data["keywords"]
        else:
            continue
            
        if any(keyword in question_lower for keyword in keywords):
            # Get the answer in the requested language
            if "answer" in faq_data and language in faq_data["answer"]:
                answer = faq_data["answer"][language]
            elif "answer" in faq_data and isinstance(faq_data["answer"], str):
                # Fallback for old format
                answer = faq_data["answer"]
            else:
                continue
                
            response = {
                "answer": answer,
                "sources": [],
                "show_contact_button": faq_data.get("show_contact", False),
                "is_faq": True
            }
            
            # Add meeting booking info if available
            if faq_data.get("book_meeting", False):
                response["book_meeting"] = True
                response["meeting_url"] = faq_data.get("meeting_url", "")
            
            # Add phone number info if available
            if faq_data.get("show_phone", False):
                response["show_phone"] = True
                response["phone_number"] = faq_data.get("phone_number", "")
            
            return response
    
    return None

def get_relevant_fallback_page(question: str) -> str:
    """Determine the most relevant page for questions we can't fully answer"""
    question_lower = question.lower()
    
    # Software development / custom solutions
    if any(word in question_lower for word in ["software", "udvikling", "program", "app", "system", "database", "integration", "api"]):
        return "https://support-solutions.dk/services/"
    
    # Pricing and business questions
    if any(word in question_lower for word in ["pris", "kost", "budget", "økonomi", "betaling", "tilbud"]):
        return "https://support-solutions.dk/kontakt/"
    
    # Security questions
    if any(word in question_lower for word in ["sikkerhed", "backup", "virus", "malware", "firewall", "gdpr"]):
        return "https://support-solutions.dk/services/"
    
    # Cloud and infrastructure
    if any(word in question_lower for word in ["cloud", "skyen", "server", "infrastruktur", "azure", "aws"]):
        return "https://support-solutions.dk/services/"
    
    # Cases and examples
    if any(word in question_lower for word in ["case", "eksempel", "erfaring", "projekt", "kunder"]):
        return "https://support-solutions.dk/cases/"
    
    # About company
    if any(word in question_lower for word in ["om", "virksomhed", "historie", "team", "medarbejder"]):
        return "https://support-solutions.dk/om-os/"
    
    # Default to contact page
    return "https://support-solutions.dk/kontakt/"

def answer_question(question: str, docs: List[Dict], language: str = "da") -> Dict:
    # Check if question is completely irrelevant first
    irrelevant_check = is_irrelevant_question(question)
    if irrelevant_check:
        if isinstance(irrelevant_check, str):  # Specific type of irrelevant question
            smart_response = get_smart_irrelevant_response(question, irrelevant_check, language)
            return {
                "answer": smart_response,
                "sources": [],
                "show_contact_button": True,
                "is_faq": True
            }
        else:  # General irrelevant question
            general_response = (
                "Hmm, that doesn't sound like an IT question... 🤔 But I'm here to help with technical challenges! Support Solutions specializes in 24/7 IT support, cloud solutions, and cybersecurity. What can we help you with on the IT front?" 
                if language == "en" else 
                "Hmm, det lyder ikke som et IT-spørgsmål... 🤔 Men jeg er her for at hjælpe med tekniske udfordringer! Support Solutions specialiserer sig i 24/7 IT-support, cloud-løsninger og cybersikkerhed. Hvad kan vi hjælpe jer med på IT-fronten?"
            )
            return {
                "answer": general_response,
                "sources": [],
                "show_contact_button": True,
                "is_faq": True
            }
    
    # First check if this matches a predefined FAQ
    faq_response = check_faq_response(question, language)
    if faq_response:
        return faq_response
    
    # Otherwise use normal RAG pipeline with improved prompting
    context = format_context(docs)
    
    # Language-specific prompts and keywords
    if language == "en":
        user_prompt = f"""Customer question: {question}

Relevant information from Support Solutions:
{context}

IMPORTANT: Give a SHORT, precise answer (max 100 words for simple questions):
- Answer the customer's question directly
- Only elaborate if technically complex
- End with concrete action"""
        
        contact_keywords = ['address', 'located', 'contact', 'phone', 'email', 'where', 'placed', 'find', 'call', 'visit']
        incomplete_phrases = ["i don't have", "unfortunately not", "cannot provide"]
        fallback_text = "Get more detailed information"
    else:
        user_prompt = f"""Kundens spørgsmål: {question}

Relevant information fra Support Solutions:
{context}

VIGTIGT: Giv et KORT, præcist svar (max 100 ord til simple spørgsmål):
- Besvar direkte kundens spørgsmål
- Kun uddyb hvis teknisk komplekst
- Slut med konkret handling"""
        
        contact_keywords = ['adresse', 'lokaliseret', 'kontakt', 'telefon', 'email', 'hvor', 'placeret', 'ligger', 'find', 'ring', 'opkald', 'besøg']
        incomplete_phrases = ["jeg har ikke", "desværre ikke", "kan ikke give"]
        fallback_text = "Få mere detaljeret information"

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role":"system","content": SYSTEM_PROMPTS[language]},
            {"role":"user","content": user_prompt}
        ],
        temperature=0.1,  # Lavere for mere præcise svar
        max_tokens=400,   # Mindre for kortere svar
        presence_penalty=0.2,
        frequency_penalty=0.2
    )
    content = resp.choices[0].message.content.strip()
    
    # Detect if this is a contact-related question or if we need fallback
    is_contact_question = any(keyword in question.lower() for keyword in contact_keywords)
    
    # Check if answer seems incomplete or generic (simple heuristics)
    seems_incomplete = (
        len(content) < 200 or  # Very short answer
        any(phrase in content.lower() for phrase in incomplete_phrases) or
        len(docs) == 0  # No relevant documents found
    )
    
    response = {
        "answer": content, 
        "sources": format_sources(docs),
        "show_contact_button": is_contact_question or seems_incomplete
    }
    
    # Add suggested page for incomplete answers
    if seems_incomplete:
        suggested_page = get_relevant_fallback_page(question)
        response["suggested_page"] = suggested_page
        response["suggested_page_text"] = fallback_text
    
    return response