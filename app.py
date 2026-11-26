import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def match_score(cv, offer):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([cv, offer])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100)


def missing_keywords(cv, offer, top=10):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([offer])
    words = vectorizer.get_feature_names_out()
    scores = vectors.toarray()[0]
    ranked = sorted(zip(words, scores), key=lambda x: x[1], reverse=True)
    cv_lower = cv.lower()
    missing = []
    for word, score in ranked:
        if word not in cv_lower:
            missing.append(word)
        if len(missing) == top:
            break
    return missing


st.set_page_config(page_title="InternMatch", page_icon="🎯")
st.title("InternMatch")
st.write("Compare ton CV avec une offre de stage et vois ce qui manque.")

cv_file = st.file_uploader("Ton CV (PDF)", type="pdf")
cv_text = st.text_area("...ou colle ton CV ici", height=150)
offer_text = st.text_area("Offre de stage", height=200)

if cv_file is not None:
    cv_text = read_pdf(cv_file)

if st.button("Analyser"):
    if cv_text == "" or offer_text == "":
        st.warning("Ajoute d'abord ton CV et l'offre.")
    else:
        score = match_score(cv_text, offer_text)
        st.metric("Score de compatibilité", f"{score} / 100")
        st.progress(score / 100)

        if score >= 25:
            st.success("Bon match, postule !")
        elif score >= 12:
            st.info("Match moyen, adapte ton CV à l'offre.")
        else:
            st.error("Match faible, cette offre ne correspond peut-être pas à ton profil.")

        st.subheader("Mots-clés de l'offre absents de ton CV")
        for word in missing_keywords(cv_text, offer_text):
            st.write("- " + word)
