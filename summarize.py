"""Turn a batch of raw emails into a structured weekly newsletter using Gemini."""
import os
import json
import google.generativeai as genai

# Check https://ai.google.dev for the current recommended free-tier model name
# if this one is deprecated.
MODEL_NAME = "gemini-2.0-flash"

SYSTEM_PROMPT = """Tu es l'assistant de veille d'un étudiant en finance/stratégie/gestion d'actifs.
On te donne un lot d'emails (newsletters de banques d'investissement, gestionnaires d'actifs,
fonds de PE/VC/dette, hedge funds, cabinets de conseil, cabinets d'avocats), reçus cette semaine.

Ta mission : produire une newsletter hebdomadaire de veille, en français, qui :
1. Est organisée par THÈME (ex: M&A, marchés privés, IA & tech, macro, géopolitique...)
   puis par GÉOGRAPHIE quand c'est pertinent (Amérique du Nord, Europe, Chine, Inde,
   Asie du Sud-Est, Afrique, Amérique latine).
2. Pour chaque point : donne l'idée clé, le ou les chiffres exacts cités, ET la source
   précise (nom de l'émetteur + date de publication) entre parenthèses. N'invente JAMAIS
   un chiffre ou une source qui n'est pas dans le texte fourni. Si tu n'es pas sûr d'un
   chiffre, ne l'inclus pas.
3. Ajoute une section "Idées d'entrepreneuriat" et une section "Secteurs à surveiller
   pour investir", basées uniquement sur les signaux présents dans les emails.
4. Reste synthétique : l'ensemble doit se lire en moins de 20 minutes (environ 2500 à
   3000 mots maximum).
5. Si un chiffre se prête à un graphique simple (évolution dans le temps, comparaison
   entre quelques catégories), ajoute-le dans "chart_data" au format décrit ci-dessous.

Réponds UNIQUEMENT avec un objet JSON valide (aucun texte avant/après, pas de balises
markdown), de la forme :
{
  "sections": [
    {
      "theme": "Nom du thème",
      "items": [
        {"text": "Idée résumée avec le chiffre clé inclus.", "source": "Nom émetteur, date"}
      ]
    }
  ],
  "entrepreneurship_ideas": ["idée 1", "idée 2"],
  "sectors_to_watch": ["secteur 1", "secteur 2"],
  "chart_data": [
    {
      "title": "Titre du graphique",
      "type": "bar ou line",
      "labels": ["2023", "2024", "2025"],
      "values": [10, 12, 15],
      "source": "Nom émetteur, date"
    }
  ]
}
Si aucun chiffre ne se prête à un graphique, renvoie "chart_data": [].
"""


def generate_newsletter_content(emails):
    if not emails:
        return {
            "sections": [],
            "entrepreneurship_ideas": [],
            "sectors_to_watch": [],
            "chart_data": [],
        }

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)

    corpus = "\n\n---\n\n".join(
        f"De: {e['sender']}\nSujet: {e['subject']}\nDate: {e['date']}\nContenu:\n{e['text']}"
        for e in emails
    )

    response = model.generate_content(
        f"Voici les emails reçus cette semaine :\n\n{corpus}",
        generation_config={"response_mime_type": "application/json"},
    )

    try:
        return json.loads(response.text)
    except (json.JSONDecodeError, AttributeError):
        # Fallback so nothing is lost if the model didn't return clean JSON
        return {
            "sections": [
                {
                    "theme": "Résumé brut (erreur de parsing JSON)",
                    "items": [{"text": response.text, "source": ""}],
                }
            ],
            "entrepreneurship_ideas": [],
            "sectors_to_watch": [],
            "chart_data": [],
        }
