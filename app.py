import unicodedata
import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MOTS_VIDES = [
    "a", "au", "aux", "avec", "ce", "ces", "cette", "dans", "de", "des", "du",
    "elle", "en", "et", "etc", "est", "etre", "il", "ils", "je", "la", "le",
    "les", "leur", "lui", "ma", "mais", "me", "mes", "moi", "mon", "ne", "nos",
    "notre", "nous", "on", "ou", "par", "pas", "pour", "qu", "que", "qui", "sa",
    "se", "ses", "son", "sur", "ta", "te", "tes", "toi", "ton", "tu", "un",
    "une", "vos", "votre", "vous", "y", "sont", "sera", "serez", "avez", "avoir",
    "plus", "tres", "tout", "tous", "toute", "toutes", "ainsi", "afin", "chez",
    "entre", "comme", "si", "dont", "ici", "bien", "aussi", "egalement", "h",
    "f", "poste", "stage", "stagiaire", "profil", "mission", "missions",
    "recherchons", "rejoindre", "equipe", "entreprise", "candidat", "candidature",
    "sein", "participerez", "parties", "aurez", "savoir", "souhaitez",
]

SECTIONS_CV = {
    "Expériences": ["experience", "experiences"],
    "Formation": ["formation", "formations", "diplome", "etudes"],
    "Compétences": ["competence", "competences"],
    "Langues": ["langue", "langues", "anglais"],
    "Email": ["@"],
    "Téléphone": ["06", "07", "+33"],
}


def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte.lower())
    return "".join(c for c in texte if unicodedata.category(c) != "Mn")


def lire_pdf(fichier):
    lecteur = PdfReader(fichier)
    texte = ""
    for page in lecteur.pages:
        texte += page.extract_text() + "\n"
    return texte


def score_compatibilite(cv, annonce):
    vectoriseur = TfidfVectorizer(stop_words=MOTS_VIDES)
    vecteurs = vectoriseur.fit_transform([nettoyer(cv), nettoyer(annonce)])
    score = cosine_similarity(vecteurs[0], vecteurs[1])[0][0]
    return round(score * 100)


def mots_cles_manquants(cv, annonce, nombre=10):
    vectoriseur = TfidfVectorizer(stop_words=MOTS_VIDES)
    vecteurs = vectoriseur.fit_transform([nettoyer(annonce)])
    mots = vectoriseur.get_feature_names_out()
    poids = vecteurs.toarray()[0]
    classement = sorted(zip(mots, poids), key=lambda x: x[1], reverse=True)
    cv_propre = nettoyer(cv)
    manquants = []
    for mot, p in classement:
        if mot not in cv_propre and not mot.isdigit():
            manquants.append(mot)
        if len(manquants) == nombre:
            break
    return manquants


def verifier_sections(cv):
    cv_propre = nettoyer(cv)
    resultats = {}
    for section, mots in SECTIONS_CV.items():
        resultats[section] = any(mot in cv_propre for mot in mots)
    return resultats


st.set_page_config(page_title="InternMatch", page_icon="🎯")
st.title("InternMatch")
st.write("Vérifie si ton CV correspond à une annonce de stage, et ce qu'il faut ajouter.")

fichier_cv = st.file_uploader("1. Ton CV (PDF)", type="pdf")
texte_cv = st.text_area("...ou colle le texte de ton CV ici", height=150)
texte_annonce = st.text_area("2. Annonce de stage (colle ici l'annonce à laquelle tu veux postuler)", height=200)

if fichier_cv is not None:
    texte_cv = lire_pdf(fichier_cv)

if st.button("Analyser"):
    if texte_cv == "" or texte_annonce == "":
        st.warning("Ajoute ton CV et l'annonce avant de lancer l'analyse.")
    else:
        score = score_compatibilite(texte_cv, texte_annonce)
        st.metric("Score de compatibilité", f"{score} / 100")
        st.progress(min(score, 100) / 100)

        if score >= 25:
            st.success("Bon match : tu peux postuler.")
        elif score >= 12:
            st.info("Match moyen : ajoute les mots-clés ci-dessous dans ton CV.")
        else:
            st.error("Match faible : cette annonce ne correspond pas trop à ton profil.")

        st.subheader("Mots-clés de l'annonce absents de ton CV")
        st.write("Les recruteurs et les logiciels de tri cherchent ces mots. Ajoute ceux qui sont vrais pour toi.")
        for mot in mots_cles_manquants(texte_cv, texte_annonce):
            st.write("- " + mot)

        st.subheader("Vérification de ton CV")
        for section, present in verifier_sections(texte_cv).items():
            if present:
                st.write("✅ " + section)
            else:
                st.write("❌ " + section + " : introuvable")
