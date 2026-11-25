# InternMatch 🎯

A small NLP tool that compares a CV with an internship offer.

- Gives a **match score** out of 100
- Lists the **keywords from the offer missing in the CV**
- Works with a PDF CV or pasted text

I built it while looking for my own internship abroad.

## How it works

1. Both texts are turned into vectors with **TF-IDF** (each word gets a weight: frequent in this text, rare in general = important).
2. The **cosine similarity** between the two vectors gives the match score.
3. The most important words of the offer that do not appear in the CV are shown as missing keywords.

## Built with

- Python
- scikit-learn (TF-IDF, cosine similarity)
- Streamlit (web interface)
- pypdf (reads PDF CVs)

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What I learned

- Turning text into numbers with TF-IDF
- Measuring similarity between documents
- Building a simple web app in Python
