#!/usr/bin/env python3
"""
Test FAQ system
"""

import sys
import os
sys.path.append('.')

from app.rag import check_faq_response

def test_faq():
    test_questions = [
        "Hvad koster jeres services?",
        "Hvor lang tid tager implementering?",
        "Hvilke ydelser tilbyder I?",
        "Hvor hurtigt svarer I på support?",
        "Kan I hjælpe med cloud migration?",
        "Er jeres løsninger sikre?",
        "Dette er et random spørgsmål"  # Should return None
    ]
    
    for question in test_questions:
        print(f"\n🔍 Spørgsmål: {question}")
        result = check_faq_response(question)
        if result:
            print(f"✅ FAQ Match!")
            print(f"📝 Svar: {result['answer'][:100]}...")
            print(f"📞 Kontakt knap: {'Ja' if result['show_contact_button'] else 'Nej'}")
        else:
            print("❌ Intet FAQ match - bruger normal RAG")

if __name__ == "__main__":
    test_faq()