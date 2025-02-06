import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Interface Streamlit avec mise en page améliorée
st.set_page_config(layout="wide")

# Appliquer une police personnalisée
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Charger les données
def load_data():
    file_path = "jeux_de_données_anonymisés.xlsx"
    df = pd.read_excel(file_path, sheet_name="Liste_CMD_Annonyme")
    return df

df = load_data()

# Convertir les dates
df['Date Commande Client'] = pd.to_datetime(df['Date Commande Client'])
df['Date CR Ldcom'] = pd.to_datetime(df['Date CR Ldcom'])

# Calcul des KPI
nb_commandes = df.shape[0]
statut_counts = df['Statut_Commande'].value_counts()
df['Délai Livraison'] = (df['Date CR Ldcom'] - df['Date Commande Client']).dt.days
moy_delai = df['Délai Livraison'].mean()
taux_annulation = (df['Opération'].str.contains("ANNULATION", na=False).sum() / nb_commandes) * 100
group_opérateur = df['Opérateur Commercial'].value_counts().nlargest(10)
group_gestinfra = df['Gest_Infra'].value_counts().nlargest(10)

# KPI pour l'état des commandes
etat_commande_counts = df['Etat de la Commande'].value_counts()
taux_en_cours = (etat_commande_counts.get("COMMANDE EN COURS", 0) / nb_commandes) * 100
taux_resilie = (etat_commande_counts.get("RÉSILIÉE", 0) / nb_commandes) * 100

st.title("📊 Tableau de Bord - Suivi des Commandes FTTH")

# Affichage des métriques avec couleurs
st.markdown("### **📌 Indicateurs Clés**")
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔵 Total Commandes", nb_commandes)
col2.metric("🟢 Délai Moyen de Livraison (jours)", f"{moy_delai:.1f}")
col3.metric("🔴 Taux d'annulation", f"{taux_annulation:.2f}%")
col4.metric("🟡 Taux de Commandes en Cours", f"{taux_en_cours:.2f}%")

# Graphiques avec plusieurs onglets
tab1, tab2, tab3 = st.tabs(["📈 Statuts des Commandes (SI/Déploiement)", "📊 Répartition des Commandes", "📋 Données Brutes"])

with tab1:
    col6, col7 = st.columns(2)
    with col6:
        st.subheader("📌 Statuts des Commandes au niveau SI")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(statut_counts, labels=statut_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
        ax.axis("equal")
        st.pyplot(fig)

    with col7:
        st.subheader("📌 Statuts des Commandes au niveau Déploiement")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(etat_commande_counts, labels=etat_commande_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
        ax.axis("equal")
        st.pyplot(fig)

with tab2:
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("📡 Top 10 des Opérateurs Commerciaux")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=group_opérateur.values, y=group_opérateur.index, ax=ax, palette=sns.color_palette("husl", 10))
        ax.set_xlabel("Nombre de Commandes")
        ax.set_ylabel("Opérateurs Commerciaux")
        ax.set_title("Top 10 des Opérateurs Commerciaux")
        st.pyplot(fig)
    with col5:
        st.subheader("🏗️ Top 10 des Gestionnaires d'Infrastructure")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=group_gestinfra.values, y=group_gestinfra.index, ax=ax, palette=sns.color_palette("tab10"))
        ax.set_xlabel("Nombre de Commandes")
        ax.set_ylabel("Gestionnaires d'Infrastructure")
        ax.set_title("Top 10 des Gestionnaires d'Infrastructure")
        st.pyplot(fig)

with tab3:
    st.subheader("📝 Données Brutes")
    st.dataframe(df.style.set_properties(**{'background-color': 'white', 'color': 'black'}))
