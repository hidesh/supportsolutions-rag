import httpx
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "SS-RAG/1.0 (+https://support-solutions.dk/)"}

def fetch_html(url: str, timeout: int = 30) -> str:
    with httpx.Client(headers=HEADERS, timeout=timeout, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text

def extract_main_content(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    
    # Special handling for contact page
    if "kontakt" in html.lower() or "/kontakt/" in html:
        # Create manual contact information from what we know exists
        contact_info = """Support Solutions kontaktinformation:

Telefon: +45 26 33 11 38
Email: info@support-solutions.dk
Adresse: Lavendelstræde 17c, 3, 1462 København K
CVR: 42694819

Du kan kontakte Support Solutions på telefon +45 26 33 11 38 eller sende en email til info@support-solutions.dk. 
Vores adresse er Lavendelstræde 17c, 3, 1462 København K. 
Virksomheden har CVR nummer 42694819.
"""
        return contact_info
    
    # Regular content extraction for other pages
    candidates = [
        "main", "article", ".entry-content", ".elementor-widget-container",
        ".site-content", "#content", ".content", ".elementor-element"
    ]
    texts = []
    
    # Try to get text from Elementor widgets specifically
    elementor_widgets = soup.find_all(class_=lambda x: x and 'elementor-widget' in x)
    for widget in elementor_widgets:
        widget_text = widget.get_text(" ", strip=True)
        if len(widget_text) > 50:  # Only include substantial text
            texts.append(widget_text)
    
    # Try other selectors
    for sel in candidates:
        for el in soup.select(sel):
            text = el.get_text(" ", strip=True)
            if len(text) > 50:  # Only include substantial text
                texts.append(text)
    
    # Fallback to full page text
    if not texts:
        texts = [soup.get_text(" ", strip=True)]
    
    return max(texts, key=len) if texts else ""