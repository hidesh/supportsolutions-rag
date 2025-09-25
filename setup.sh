#!/bin/bash

# Support Solutions RAG Chatbot - Setup Script
# Dette script hjælper med at sætte projektet op sikkert

echo "🤖 Support Solutions RAG Chatbot - Setup"
echo "========================================"

# Check om Python er installeret
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 er ikke installeret. Install Python først."
    exit 1
fi

echo "✅ Python3 fundet"

# Check om .env filen eksisterer
if [ ! -f ".env" ]; then
    echo "⚠️  .env fil ikke fundet"
    echo "📄 Kopierer .env.example til .env..."
    cp .env.example .env
    
    echo ""
    echo "🔒 VIGTIGT SIKKERHEDSTRIN:"
    echo "1. Åbn .env filen i din editor"
    echo "2. Erstat 'DIN-OPENAI-API-NOEGLE-HER' med din rigtige OpenAI API-nøgle"
    echo "3. Få din nøgle fra: https://platform.openai.com/api-keys"
    echo "4. ALDRIG commit .env filen til git!"
    echo ""
    echo "❓ Vil du åbne .env filen nu? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
        # Prøv forskellige editorer
        if command -v code &> /dev/null; then
            code .env
        elif command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        else
            echo "Åbn .env filen manuelt i din foretrukne editor"
        fi
    fi
else
    echo "✅ .env fil fundet"
fi

# Check om requirements er installeret
echo ""
echo "📦 Installerer Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installeret"
else
    echo "❌ Fejl ved installation af dependencies"
    exit 1
fi

# Check API-nøgle
echo ""
echo "🔍 Tjekker API-nøgle konfiguration..."
if grep -q "DIN-OPENAI-API-NOEGLE-HER" .env; then
    echo "⚠️  Du skal stadig konfigurere din OpenAI API-nøgle i .env filen!"
    echo "   Åbn .env og erstat 'DIN-OPENAI-API-NOEGLE-HER' med din rigtige nøgle"
else
    echo "✅ API-nøgle ser ud til at være konfigureret"
fi

# Byg index
echo ""
echo "🔨 Bygger search index..."
python3 build_index.py

if [ $? -eq 0 ]; then
    echo "✅ Search index bygget"
else
    echo "❌ Fejl ved bygning af index - tjek din API-nøgle"
    exit 1
fi

echo ""
echo "🎉 Setup fuldført!"
echo ""
echo "🚀 Start serveren med:"
echo "   python3 -m uvicorn app.api:app --reload --port 8000"
echo ""
echo "🌐 Derefter gå til: http://localhost:8000"
echo ""
echo "🔒 Sikkerhedsreminder:"
echo "   - Hold din .env fil privat"
echo "   - Commit aldrig .env til git"
echo "   - Overvåg dit OpenAI API forbrug"