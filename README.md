# InternMatch 🎯

Un petit outil de NLP qui compare un CV avec une offre de stage.

- Donne un **score de compatibilité** sur 100
- Liste les **mots-clés de l'offre absents du CV**
- Fonctionne avec un CV en PDF ou du texte collé

Je l'ai créé pendant ma propre recherche de stage à l'étranger.

## Comment ça marche

1. Les deux textes sont transformés en vecteurs avec **TF-IDF** (chaque mot reçoit un poids : fréquent dans ce texte mais rare en général = important).
2. La **similarité cosinus** entre les deux vecteurs donne le score de compatibilité.
3. Les mots les plus importants de l'offre qui n'apparaissent pas dans le CV sont affichés comme mots-clés manquants.

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

## Ce que j'ai appris

- Transformer du texte en nombres avec TF-IDF
- Mesurer la similarité entre deux documents
- Créer une application web simple en Python

## Limite

L'outil compare des mots, pas leur sens : le CV et l'offre doivent être dans la même langue (anglais conseillé).
