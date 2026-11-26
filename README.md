# InternMatch 🎯

Un petit outil qui vérifie si un CV correspond à une annonce de stage.

## Ce qu'il fait

1. Donne un **score de compatibilité** sur 100 entre ton CV et l'annonce
2. Liste les **mots-clés de l'annonce absents de ton CV** (ceux que cherchent les recruteurs et les logiciels de tri)
3. Vérifie que ton CV contient les **rubriques attendues en France** : expériences, formation, compétences, langues, email, téléphone

Je l'ai créé pendant ma propre recherche de stage.

## Comment ça marche

- Les deux textes sont nettoyés (minuscules, accents retirés, petits mots comme "le", "de", "pour" ignorés).
- Ils sont transformés en vecteurs avec **TF-IDF** : chaque mot reçoit un poids selon son importance.
- La **similarité cosinus** entre les deux vecteurs donne le score.

## Technologies

- Python
- scikit-learn (TF-IDF, similarité cosinus)
- Streamlit (interface web)
- pypdf (lecture des CV en PDF)

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limite

L'outil compare des mots, pas leur sens : le CV et l'annonce doivent être dans la même langue.
Une amélioration possible serait d'utiliser des embeddings pour comparer le sens des phrases.
