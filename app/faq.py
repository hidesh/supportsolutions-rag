# Support Solutions FAQ
# 
# Her kan du tilføje specifikke spørgsmål og svar som systemet skal prioritere
# Format:
# "nøgle": {
#     "keywords": [liste af nøgleord der trigger dette svar],
#     "answer": "Dit svar her",
#     "show_contact": True/False (om kontakt-knap skal vises)
# }

FAQ_RESPONSES = {
    "priser": {
         "keywords": ["pris", "kost", "betaling", "økonomi", "budget", "månedlig", "årlig", "hvad koster"],
         "answer": "Vi tilbyder fleksible IT-support løsninger, som tilpasses jeres behov, størrelse og eksisterende setup. Afhængig af hvilken konsulent eller løsning der er relevant, kan vi skræddersy en model, der passer bedst til jer. Kontakt os, så finder vi sammen den rette løsning.",
         "show_contact": True
    },
    
    "implementering": {
        "keywords": ["implementering", "opsætning", "installation", "hvor lang tid", "tidshorisont", "opstart", "igangsættelse"],
        "answer": "Vi kan typisk implementere vores IT-support løsninger inden for 1-2 uger afhængigt af kompleksiteten af jeres IT-miljø. Processen inkluderer analyse af eksisterende systemer, opsætning af monitoring og integration med jeres workflows. Vi sørger for en gnidningsløs overgang.",
        "show_contact": True
    },
    
    "services": {
        "keywords": ["ydelser", "services", "tilbyder", "kan i", "hjælpe med", "specialister", "kompetencer"],
        "answer": "<strong>🔧 Vores IT-services</strong><br><br><strong>Support & Drift:</strong><br>• 24/7 IT-support og hotline<br>• Proaktiv systemovervågning<br>• Fejlfinding og problemløsning<br>• Helpdesk og bruger-support<br><br><strong>Cloud & Infrastruktur:</strong><br>• Cloud-migration til Azure/AWS<br>• Server-opsætning og vedligeholdelse<br>• Netværk og sikkerhedsløsninger<br>• Backup og disaster recovery<br><br><strong>Sikkerhed & Compliance:</strong><br>• Cybersikkerhed og firewall<br>• GDPR-compliance rådgivning<br>• Email-sikkerhed og spam-filter<br>• Sikkerhedsaudit og penetrationstest<br><br><strong>Rådgivning:</strong><br>• IT-strategi og digitaliseringsplaner<br>• System-integration og optimering<br>• Leverandør-evaluering og indkøb",
        "show_contact": True
    },
    
    "response_tid": {
        "keywords": ["responstid", "hvor hurtigt", "reaktionstid", "support tid", "hvor lang tid", "svar tilbage"],
        "answer": "Vi garanterer en responstid på under 4 timer på alle support-henvendelser i arbejdstiden (8-17). For kritiske systemer tilbyder vi 24/7 support med maksimal responstid på 1 time. Vores gennemsnitlige løsningstid er under 2 timer for almindelige problemer.",
        "show_contact": True
    },
    
    "cloud_migration": {
        "keywords": ["cloud", "skyen", "migration", "flytning", "azure", "aws", "google cloud", "cloud løsninger"],
        "answer": "Vi er specialister i cloud-migration og hjælper virksomheder med at flytte deres IT-infrastruktur til skyen sikkert og effektivt. Vi arbejder primært med Microsoft Azure, men har også erfaring med AWS og Google Cloud. Processen inkluderer analyse, planning, migration og efterfølgende drift.",
        "show_contact": True
    },
    
    "sikkerhed": {
        "keywords": ["sikkerhed", "cybersikkerhed", "sikker", "beskyttelse", "virus", "malware", "backup", "firewall", "sikre", "beskyttet"],
        "answer": "Cybersikkerhed er vores højeste prioritet. Vi implementerer multi-layer sikkerhedsløsninger inkl. avancerede firewalls, endpoint protection, email-sikkerhed, backup-systemer og security monitoring 24/7. Vi hjælper også med compliance til GDPR og andre regulativer.",
        "show_contact": True
    },
    
    "kunder_cases": {
        "keywords": ["kunder", "cases", "cases", "projekter", "erfaring", "tidligere", "eksempler", "reference", "success", "case studies", "hvem har i hjulpet", "danx", "chr hansen", "sentia", "hvad har i lavet", "lavet hos", "arbejdet med", "hjulpet med", "løst", "løsninger", "gjort", "portfolie"],
        "answer": "<strong>🏆 Vores kunder og projekter</strong><br><br><strong>DANX (Certificerings-digitalisering):</strong><br>• Digitaliseret buscertifikat-processen<br>• Automatiseret workflows og compliance<br>• <em>70% reduktion i sagsbehandlingstid</em><br><br><strong>Chr. Hansen (Cloud-migration):</strong><br>• Migreret produktionssystemer til Azure<br>• Optimeret netværksarkitektur<br>• <em>40% reduktion i IT-driftsomkostninger</em><br><br><strong>SENTIA (24/7 IT-support):</strong><br>• Kritisk hosting-miljø support<br>• Avancerede sikkerhedsløsninger<br>• <em>99.9% oppetid på systemer</em><br><br><strong>Andre projekter:</strong><br>• Små startups → Store koncerner<br>• Alle brancher og størrelser<br>• Skræddersyede løsninger",
        "show_contact": True
    },
    
    "danx_case": {
        "keywords": ["danx", "bus", "certificering", "buscertifikat", "digitalisering", "digital løsning"],
        "answer": "DANX-projektet involverede digitalisering af hele deres buscertifikat-proces. Vi udviklede en omfattende digital løsning som erstattede manuelle processer, implementerede automatiserede workflows og sikrede compliance med alle regulativer. Projektet reducerede sagsbehandlingstid med 70% og forbedrede kundeoplevelsen markant.",
        "show_contact": True
    },
    
    "chr_hansen_case": {
        "keywords": ["chr hansen", "chr. hansen", "biotech", "cloud migration", "infrastruktur"],
        "answer": "For Chr. Hansen gennemførte vi en omfattende cloud-migration af deres IT-infrastruktur. Vi migrerede kritiske produktionssystemer til Azure, implementerede avancerede backup-løsninger og optimerede deres netværksarkitektur. Resultatet var 40% reduktion i IT-driftsomkostninger og forbedret system-stabilitet.",
        "show_contact": True
    },
    
    "sentia_case": {
        "keywords": ["sentia", "hosting", "datacentre", "24/7", "kritiske systemer"],
        "answer": "SENTIA havde behov for omfattende IT-support til deres kritiske hosting-miljøer. Vi implementerede 24/7 monitoring og support, avancerede sikkerhedsløsninger og proaktiv systemvedligeholdelse. Vores løsning sikrede 99.9% oppetid på kritiske systemer og hurtig respons på alle incidents.",
        "show_contact": True
    },
    
    "arbejde_projekter": {
        "keywords": ["hvad laver i", "hvilke opgaver", "arbejde", "job", "aktiviteter", "hvad beskæftiger", "arbejder med", "fokus", "specialiserer", "gør i", "type arbejde"],
        "answer": "Vi specialiserer os i at levere komplet IT-support og -løsninger til danske virksomheder. Vores arbejde spænder fra daglig IT-support og fejlfinding til store digitaliserings- og cloud-migration projekter. Vi arbejder både med proaktiv IT-drift, cybersikkerhed, applikationsstyring og strategisk IT-rådgivning. Hver dag hjælper vi virksomheder med at optimere deres IT-miljøer og sikre stabil drift.",
        "show_contact": True
    },
    
    "virksomhed_om": {
        "keywords": ["hvad handler", "hvad beskæftiger", "om virksomheden", "hvad er", "forretning", "firma", "company", "business", "hvad gør i", "jeres virksomhed"],
        "answer": "<strong>🚀 Support Solutions - Jeres IT-partner</strong><br><br><strong>Hvad vi gør:</strong><br>• 24/7 IT-support og fejlløsning<br>• Cloud-migration og modernisering<br>• Cybersikkerhed og backup-løsninger<br>• Applikationsstyring og optimering<br>• Strategisk IT-rådgivning<br><br><strong>Vores ekspertise:</strong><br>• +10 års erfaring med virksomheds-IT<br>• Specialister i Microsoft Azure<br>• GDPR-compliance og sikkerhed<br>• Proaktiv overvågning og vedligeholdelse<br><br><strong>Hvem vi hjælper:</strong><br>• Små og mellemstore virksomheder<br>• Startups der skal skalere IT<br>• Etablerede firmaer der vil modernisere<br>• Virksomheder med kritiske IT-behov",
        "show_contact": True
    },
    
    "book_moede": {
        "keywords": ["book møde", "book et møde", "møde", "aftale", "tid", "planlægge møde", "kan vi mødes", "vil gerne møde", "booking", "konsultation", "snak", "drøfte", "præsentation", "demo", "vi skal snakke"],
        "answer": "Det lyder fantastisk! Vi vil meget gerne møde jer og høre mere om jeres IT-udfordringer. Et møde giver os mulighed for at forstå jeres specifikke behov og præsentere, hvordan vi kan hjælpe. I kan nemt booke et møde direkte i vores kalender - vælg den tid der passer jer bedst.",
        "show_contact": True,
        "book_meeting": True,
        "meeting_url": "https://support-solutions.dk/book-et-moede/"
    }
}

# INSTRUKTIONER TIL AT TILFØJE NYE FAQ:
# 
# 1. Tilføj en ny sektion med et unikt nøgle-navn
# 2. List alle ord/sætninger der skal trigge dette svar i "keywords"
# 3. Skriv dit præcise svar i "answer"
# 4. Sæt "show_contact" til True hvis kontakt-knap skal vises
# 
# EKSEMPEL:
# "nyt_emne": {
#     "keywords": ["keyword1", "keyword2", "sætning der trigger"],
#     "answer": "Dit specifikke svar til dette spørgsmål...",
#     "show_contact": True
# }