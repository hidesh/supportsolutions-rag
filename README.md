# Support Solutions RAG Chatbot 🤖

En intelligent chatbot baseret på RAG (Retrieval Augmented Generation) teknologi, der kan svare på spørgsmål om Support Solutions' services og ekspertise. Systemet kombinerer web scraping, AI embeddings og OpenAI's GPT-4o model for at levere præcise og kontekstuelle svar.

## 🔒 Sikkerhed FØRST

**VIGTIGT**: Denne applikation indeholder sensitive API-nøgler og konfiguration. Følg disse sikkerhedsretningslinjer nøje:

### ⚠️ Hvad du ALDRIG må gøre:
- ❌ Commit `.env` filen til git
- ❌ Del dine API-nøgler offentligt
- ❌ Hardcode API-nøgler direkte i koden
- ❌ Upload `.env` til GitHub, Discord, eller andre platforme

### ✅ Sikkerhedstjekliste:
- ✅ Alle sensitive værdier er i `.env` filen
- ✅ `.env` er tilføjet til `.gitignore`
- ✅ Brug kun miljøvariabler til konfiguration
- ✅ Regenerer API-nøgler hvis de bliver kompromitteret

## 🚀 Hurtig Start

### 1. Klon Repository
```bash
git clone <dit-repository>
cd supportsolutions-rag
```

### 2. Installer Dependencies
```bash
pip install -r requirements.txt
```

### 3. Opsæt Miljøvariabler (KRITISK!)
Opret en `.env` fil i rod-mappen:

```bash
# .env fil - HOLD DENNE PRIVAT!
OPENAI_API_KEY=sk-proj-din-openai-noegle-her
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-large
```

> **⚠️ ADVARSEL**: Denne fil indeholder dine private API-nøgler! Del den ALDRIG og commit den ALDRIG til git.

### 4. Byg Search Index
```bash
python3 build_index.py
```

### 5. Start Serveren
```bash
python3 -m uvicorn app.api:app --reload --port 8000
```

### 6. Åbn Chatbot
Gå til `http://localhost:8000` i din browser.

## 📁 Projektstruktur

```
supportsolutions-rag/
├── .env                    # ⚠️ PRIVAT - API nøgler (ikke i git!)
├── .gitignore              # Sikrer .env ikke committes
├── README.md               # Denne fil
├── requirements.txt        # Python dependencies
├── build_index.py          # Bygger search index fra hjemmeside
├── index.html              # Frontend chatbot interface
├── app/
│   ├── __init__.py
│   ├── api.py             # FastAPI server endpoints
│   ├── config.py          # Indlæser miljøvariabler sikkert
│   ├── rag.py             # RAG logik og FAQ system
│   ├── faq.py             # Foruddefinerede FAQ svar
│   ├── retriever.py       # Document retrieval
│   ├── embed.py           # OpenAI embeddings
│   ├── indexer.py         # FAISS vector database
│   ├── ingest_web.py      # Web scraping
│   └── text_utils.py      # Tekst utilities
└── data/
    ├── chunks.jsonl       # Indekserede tekst chunks
    ├── faiss.index        # Vector database
    └── url_list.txt       # URLs til scraping
```

## 🔧 Konfiguration

### Environment Variables (.env)
```bash
# OpenAI API (PÅKRÆVET)
OPENAI_API_KEY=sk-proj-...          # Din OpenAI API nøgle
CHAT_MODEL=gpt-4o                   # Chat model (anbefalet: gpt-4o)
EMBEDDING_MODEL=text-embedding-3-large  # Embedding model

# API Konfiguration (valgfri)
API_HOST=127.0.0.1                  # Server host
API_PORT=8000                       # Server port
```

### Hvor får du API-nøgler?
1. **OpenAI API**: Gå til [platform.openai.com](https://platform.openai.com/api-keys)
2. Opret en konto og generer en API-nøgle
3. **VIGTIGT**: Hold din nøgle privat og sikker!

## ⚙️ Funktioner

### 🤖 FAQ System
- Øjeblikkelige svar på almindelige spørgsmål
- Intelligent keyword matching
- Automatiske kontakt- og møde-booking knapper

### 🔍 RAG (Retrieval Augmented Generation)
- Web scraping af Support Solutions hjemmeside
- Vector-baseret søgning med FAISS
- Kontekstuelle svar baseret på faktisk indhold

### 🎨 Brugervenlig Interface
- Clean, moderne design
- Kildeangivelser med links
- Responsiv layout til alle enheder

### 📞 Smart Call-to-Action
- Automatiske kontakt-knapper
- Møde-booking integration
- Personaliserede handlingsopfordringer

## 🛠️ Udvikling

### Tilføj Nye FAQ
Rediger `app/faq.py`:
```python
"nyt_emne": {
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "answer": "Dit svar her...",
    "show_contact": True,           # Vis kontakt knap
    "book_meeting": False,          # Vis møde-booking knap
    "meeting_url": "https://..."    # Møde-booking URL
}
```

### Opdater Website URLs
Rediger `data/url_list.txt` og kør:
```bash
python3 build_index.py
```

### Debug Mode
```bash
# Kør med debug logging
python3 -m uvicorn app.api:app --reload --port 8000 --log-level debug
```

## 🔒 Sikkerhedsbedste Praksis

### API Nøgle Sikkerhed
```python
# ✅ KORREKT - Brug miljøvariabler
import os
api_key = os.getenv('OPENAI_API_KEY')

# ❌ FORKERT - Hardcodede nøgler
api_key = "sk-proj-1234567890..."  # ALDRIG gør dette!
```

### .gitignore Opsætning
Sørg for at `.gitignore` indeholder:
```
.env
__pycache__/
*.pyc
.DS_Store
*.log
.vscode/
```

### Miljø Separation
```bash
# Forskellige environments
.env.development
.env.production
.env.local
```

## 🚨 Nødsituation - Kompromitterede Nøgler

Hvis dine API-nøgler bliver eksponeret:

1. **Øjeblikkelig handling:**
   ```bash
   # Gå til OpenAI Platform
   # Deaktiver den kompromitterede nøgle
   # Generer en ny nøgle
   ```

2. **Opdater dit system:**
   ```bash
   # Opdater .env med ny nøgle
   OPENAI_API_KEY=sk-proj-din-nye-noegle
   
   # Genstart serveren
   python3 -m uvicorn app.api:app --reload
   ```

3. **Git cleanup (hvis nødvendigt):**
   ```bash
   # Fjern eksponeret data fra git historie
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```

## 📊 Performance & Monitoring

### System Requirements
- Python 3.8+
- 4GB RAM (anbefalet 8GB)
- 1GB disk space
- Internet forbindelse for OpenAI API

### API Limits
- OpenAI has rate limits - overvåg dit forbrug
- Implementer caching for bedre performance
- Brug FAQ system til almindelige spørgsmål

## 🤝 Contributing

1. Fork projektet
2. Opret feature branch (`git checkout -b feature/AmazingFeature`)
3. **VIGTIGT**: Commit aldrig `.env` filer!
4. Push til branch (`git push origin feature/AmazingFeature`)
5. Åbn en Pull Request

## 📞 Support

Har du problemer eller spørgsmål?
- 📧 Email: [din-email]
- 🌐 Website: [dit-website]
- 📱 GitHub Issues: [link til issues]

## ⚖️ Licens

Dette projekt er licenseret under MIT License - se [LICENSE](LICENSE) filen for detaljer.

---

## 🔐 Sikkerhed Reminder

**Før du committer:**
```bash
# Tjek at .env ikke er inkluderet
git status

# Hvis .env vises, tilføj til .gitignore med det samme!
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore for security"
```

**Husk**: Din sikkerhed afhænger af at holde API-nøgler private! 🔒
