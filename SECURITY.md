# 🔒 Sikkerhedsretningslinjer

Denne fil beskriver vigtige sikkerhedsforanstaltninger for Support Solutions RAG Chatbot.

## 🚨 Kritiske Sikkerhedsregler

### 1. API-nøgle Beskyttelse
- ❌ **ALDRIG** commit `.env` filen til git
- ❌ **ALDRIG** del dine API-nøgler offentligt (Discord, email, chat)
- ❌ **ALDRIG** hardcode API-nøgler i koden
- ❌ **ALDRIG** upload `.env` til GitHub, cloud storage, eller andre tjenester
- ✅ Brug altid miljøvariabler fra `.env` filen
- ✅ Regenerer nøgler øjeblikkeligt hvis de bliver kompromitteret

### 2. Git Sikkerhed
```bash
# Tjek altid hvad du committer
git status
git diff --staged

# Sørg for .env ALDRIG er synlig
git ls-files | grep .env  # Skulle ikke returnere noget
```

### 3. Miljøvariabel Validering
Koden tjekker automatisk for sikkerhedsproblemer:
```python
# app/config.py tjekker for placeholder-værdier
if api_key == "DIN-OPENAI-API-NOEGLE-HER":
    raise ValueError("Du skal konfigurere din rigtige OpenAI API-nøgle i .env!")
```

## 🔍 Sikkerhedstjekliste

Før du pusher til GitHub:
- [ ] `.env` filen er i `.gitignore`
- [ ] Ingen API-nøgler er hardcodet i koden
- [ ] `.env.example` indeholder kun placeholder-værdier
- [ ] `git status` viser ikke `.env` filen
- [ ] Alle sensitive data er i miljøvariabler

## 🚨 Hvis API-nøgler Bliver Kompromitteret

### Øjeblikkelige Skridt:
1. **Gå til OpenAI Platform**: https://platform.openai.com/api-keys
2. **Deaktiver den kompromitterede nøgle** øjeblikkeligt
3. **Generer en ny API-nøgle**
4. **Opdater din `.env` fil** med den nye nøgle
5. **Genstart applikationen**

### Git Historie Cleanup (hvis nødvendigt):
```bash
# Hvis du ved et uheld har committet .env
git rm --cached .env
git commit -m "Remove .env from tracking"

# For at fjerne fra hele git-historien (FORSIGTIG!)
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch .env' \
--prune-empty --tag-name-filter cat -- --all
```

## 📊 Overvågning og Begrænsninger

### OpenAI API Limits
- Overvåg dit forbrug på: https://platform.openai.com/usage
- Sæt budgetgrænser for at undgå overraskende regninger
- Implementer rate limiting i din applikation

### Logging Sikkerhed
```python
# ✅ KORREKT - Log ikke sensitive data
logger.info(f"API request made with model: {model}")

# ❌ FORKERT - Log aldrig API-nøgler
logger.info(f"Using API key: {api_key}")  # ALDRIG!
```

## 🛡️ Bedste Praksis

### Udvikling vs Production
```bash
# Brug forskellige nøgler til forskellige miljøer
.env.development    # Udvikling
.env.production     # Production
.env.local          # Lokal test
```

### Backup og Recovery
- Hold backup af dine API-nøgler sikkert (password manager)
- Dokumenter hvilke nøgler bruges hvor
- Hav en plan for nøgle-rotation

### Team Sikkerhed
Når flere personer arbejder på projektet:
- Del aldrig `.env` filer direkte
- Brug secure channels til at dele nøgle-information
- Implementer nøgle-rotation rutiner
- Begræns API-nøgle tilladelser til minimum nødvendige

## 🔒 Compliance og Regulering

### GDPR Overvejelser
- Denne applikation gemmer ikke personlige data permanent
- Chat-beskeder sendes til OpenAI's servere
- Læs OpenAI's privacy policy: https://openai.com/privacy/

### Data Behandling
- Web scraping data fra offentlige websites
- Ingen følsom kunde-data opbevares lokalt
- Alle API-kald er over HTTPS

## 📞 Sikkerhed Support

Hvis du opdager sikkerhedsproblemer:
1. **Rapporter ikke sikkerhedsproblemer offentligt**
2. Kontakt projekt-maintainer direkte
3. Inkluder detaljeret beskrivelse af problemet
4. Vent på bekræftelse før offentlig disclosure

## 🔄 Sikkerhed Updates

Dette dokument opdateres regelmæssigt. Tjek for updates når du:
- Opdaterer dependencies
- Ændrer API-konfiguration  
- Implementerer nye funktioner
- Deployer til nye miljøer

---

**Husk**: Sikkerhed er ikke en one-time setup, men en kontinuerlig proces! 🔐