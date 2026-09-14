# Veille finance & stratégie — newsletter hebdomadaire

Pipeline 100% gratuit qui lit les newsletters reçues sur ta boîte Gmail, les résume
par thème avec sources et graphiques via l'API Gemini (tier gratuit), et t'envoie
une synthèse chaque lundi.

## Mise en route (une seule fois)

1. Crée un nouveau repo GitHub **privé** et mets-y tous les fichiers de ce dossier
   en conservant l'arborescence (le dossier `.github/workflows/` doit rester tel quel).
2. Dans **Settings > Secrets and variables > Actions** de ton repo, crée 3 secrets :
   - `GMAIL_ADDRESS` : ton adresse Gmail
   - `GMAIL_APP_PASSWORD` : le mot de passe d'application généré dans les paramètres Google
   - `GEMINI_API_KEY` : ta clé API gratuite depuis aistudio.google.com
3. C'est tout — le workflow tourne automatiquement chaque lundi à 7h UTC.

## Tester sans attendre lundi

Dans l'onglet **Actions** de ton repo GitHub > sélectionne le workflow
"Weekly finance newsletter" > bouton **Run workflow**. Ça déclenche une exécution
immédiate, pratique pour vérifier que tout fonctionne.

## Personnaliser

- **Le ton, les thèmes, la longueur** : modifie le texte `SYSTEM_PROMPT` dans
  `summarize.py`. C'est le principal levier pour ajuster ce que tu reçois, sans
  toucher au reste du code.
- **La fréquence** : modifie la ligne `cron` dans
  `.github/workflows/weekly-newsletter.yml` (format cron standard, en UTC).
- **La fenêtre de lecture des mails** : `fetch_recent_emails(days=7)` dans
  `main.py` — augmente si tu veux couvrir plus large certaines semaines.

## Limites du tier gratuit à garder en tête

- **Gemini API (free tier)** : quota journalier limité selon le modèle utilisé.
  Avec un envoi hebdomadaire, tu restes très largement dans les clous. Si Google
  fait évoluer les noms de modèles, vérifie sur aistudio.google.com que
  `MODEL_NAME` dans `summarize.py` correspond toujours à un modèle gratuit actif.
- **GitHub Actions (repo privé, compte gratuit)** : quota de minutes gratuites
  mensuel largement suffisant pour un run hebdomadaire de quelques minutes.
- **Gmail** : aucune limite pertinente pour ce volume d'usage.
- Aucune étape de ce pipeline ne peut engager de dépense automatiquement — tout
  repose sur des tiers gratuits sans carte bancaire enregistrée.

## Prochaines améliorations possibles

- Ajouter les flux RSS et notifications LinkedIn Newsletter comme sources
  complémentaires aux emails.
- Déduplication d'une semaine sur l'autre (mémoire persistante des sujets déjà traités).
- Archivage des newsletters envoyées (ex. dans un dossier `archives/` du repo).
