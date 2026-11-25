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
st.write("Compare your CV with an internship offer and see what is missing.")

cv_file = st.file_uploader("Your CV (PDF)", type="pdf")
cv_text = st.text_area("...or paste your CV here", height=150)
offer_text = st.text_area("Internship offer", height=200)

if cv_file is not None:
    cv_text = read_pdf(cv_file)

if st.button("Analyse"):
    if cv_text == "" or offer_text == "":
        st.warning("Add your CV and the offer first.")
    else:
        score = match_score(cv_text, offer_text)
        st.metric("Match score", f"{score} / 100")
        st.progress(score / 100)

        if score >= 25:
            st.success("Good match, apply!")
        elif score >= 12:
            st.info("Average match, adapt your CV to the offer.")
        else:
            st.error("Weak match, this offer may not fit your profile.")

        st.subheader("Keywords from the offer missing in your CV")
        for word in missing_keywords(cv_text, offer_text):
            st.write("- " + word)
