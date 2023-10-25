import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://www.data.gouv.fr/fr/datasets/r/fdf5afbf-ed3c-4c54-a4f0-3581c8a1eca4"

# Charger le dataset en utilisant Pandas
df = pd.read_excel(url)

# Supposons que df est votre DataFrame
# Création d'une liste des années et des mois pour la transformation
years = list(range(2000, 2023))
months = list(range(1, 13))

# Melt du DataFrame pour le rendre "long"
df_melted = df.melt(id_vars=['libellé index'], 
                    value_vars=[f'_{year}_{str(month).zfill(2)}' for year in years for month in months if f'_{year}_{str(month).zfill(2)}' in df.columns], 
                    var_name='date', 
                    value_name='nombre')

# Extraction des années et des mois
df_melted['annee'] = df_melted['date'].str.slice(1, 5)
df_melted['mois'] = df_melted['date'].str.slice(6, 8)

# Lancement de l'application Streamlit
st.title("Histogramme interactif des crimes par année")

def afficher_formulaire():
    st.sidebar.header("Personal information")
    st.sidebar.markdown("---")  # Ligne de séparation

    # informations saisies
    st.sidebar.write("Name : Schumacher")
    st.sidebar.write("First Name : Hubert")
    st.sidebar.write("Group : BI2")
    st.sidebar.write("GitHub link: https://github.com/Hubert-Schumacher")
    st.sidebar.write("Linkedin link: https://www.linkedin.com/in/hubert-schumacher-a5482a1a2/")

afficher_formulaire() 

# Widget pour sélectionner un type de crime
selected_crime = st.selectbox("Sélectionnez un type de crime:", df['libellé index'].unique())

# Filtrage des données en fonction du crime sélectionné
filtered_data = df_melted[df_melted["libellé index"] == selected_crime]

# Création de l'histogramme interactif
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='annee:O',
    y='nombre:Q',
    color='mois:N',
    tooltip=['annee', 'mois', 'nombre']
).properties(
    title=f"Histogramme des {selected_crime} par année"
)

st.altair_chart(chart, use_container_width=True)




total_delits_per_month = df.drop(columns=df.columns[:2]).sum()

# Inversion de l'ordre des données pour commencer par la date la plus ancienne
total_delits_per_month = total_delits_per_month[::-1]

# Tracé des données
plt.figure(figsize=(15, 7))
total_delits_per_month.plot(ax=plt.gca(), marker='o', linestyle='-')
plt.title('Évolution du nombre total de délits par mois')
plt.xlabel('Mois')
plt.ylabel('Nombre total de délits')
plt.xticks(rotation=45)  # Rotation des étiquettes pour une meilleure lisibilité
plt.grid(True)
plt.tight_layout()

st.pyplot()




Homicides_list = [
    "Homicides pour voler et à l'occasion de vols",
    "Homicides pour d'autres motifs",
    "Tentatives d'homicides pour voler et à l'occasion de vols",
    "Tentatives homicides pour d'autres motifs",
    "Coups et blessures volontaires suivis de mort"
]

# Filtrage du DataFrame pour inclure uniquement les délits spécifiés
filtered_df = df[df['libellé index'].isin(Homicides_list)]

# Suppression des colonnes non nécessaires (les deux premières)
filtered_df_trimmed = filtered_df.drop(columns=df.columns[:2])

# Extraction des années et sommation des valeurs pour chaque année
grouped_by_year = filtered_df_trimmed.groupby(lambda x: x.split('_')[1], axis=1).sum()

# Tracé des données
plt.figure(figsize=(15, 7))
for index, row in grouped_by_year.iterrows():
    plt.plot(row.index, row.values, marker='o', label=df.iloc[index]['libellé index'])

plt.title('Évolution des homicides par an')
plt.xlabel('Année')
plt.ylabel('Nombre homicides')
plt.grid(True)
plt.legend(loc='upper left')
plt.tight_layout()

# Remplacez plt.show() par ceci
st.pyplot(plt)


#Pour ajouter des colonnes coportant le total de chaque année

years = list(range(2000, 2023))

for year in years:
    # Columns corresponding to each month of that year
    cols_for_year = [col for col in df.columns if str(year) in col]
    
    # Sum across the columns for that year
    df[f"total_{year}"] = df[cols_for_year].sum(axis=1)




df_sorted = df.sort_values(by='total_2022', ascending=False)

# Création du diagramme à barres
plt.figure(figsize=(20,10))
plt.bar(df_sorted['libellé index'], df_sorted['total_2022'])
plt.title("Histogramme des Fréquences de Crimes pour 2022")
plt.xlabel("Type de Crime")
plt.ylabel("Nombre d'incidents")
plt.xticks(rotation=90, fontsize=8)

# Remplacez plt.show() par ceci
st.pyplot(plt)


#code permetant d'ajouter une colonne qui permet de simplifier la classification


crimes_list = ['Règlements de compte entre malfaiteurs', "Homicides pour voler et à l'occasion de vols", "Homicides pour d'autres motifs", "Tentatives d'homicides pour voler et à l'occasion de vols", "Tentatives homicides pour d'autres motifs", 'Coups et blessures volontaires suivis de mort', 'Autres coups et blessures volontaires criminels ou correctionnels', "Prises d'otages à l'occasion de vols", "Prises d'otages dans un autre but", 'Sequestrations', 'Menaces ou chantages pour extorsion de fonds', 'Menaces ou chantages dans un autre but', 'Atteintes à la dignité et à la personnalité', 'Violations de domicile', 'Vols à main armée contre des établissements financiers', 'Vols à main armée contre des établissements industriels ou commerciaux', 'Vols à main armée contre des entreprises de transports de fonds', 'Vols à main armée contre des particuliers à leur domicile', 'Autres vols à main armée', 'Vols avec armes blanches contre des établissements financiers,commerciaux ou industriels', 'Vols avec armes blanches contre des particuliers à leur domicile', 'Autres vols avec armes blanches', 'Vols violents sans arme contre des établissements financiers,commerciaux ou industriels', 'Vols violents sans arme contre des particuliers à leur domicile', 'Vols violents sans arme contre des femmes sur voie publique ou autre lieu public', "Vols violents sans arme contre d'autres victimes", "Cambriolages de locaux d'habitations principales", 'Cambriolages de résidences secondaires', 'Cambriolages de locaux industriels, commerciaux ou financiers', "Cambriolages d'autres lieux", 'Vols avec entrée par ruse en tous lieux', 'Vols à la tire', "Vols à l'étalage", 'Vols de véhicules de transport avec frêt', "Vols d'automobiles", 'Vols de véhicules motorisés à 2 roues', 'Vols à la roulotte', "Vols d'accessoires sur véhicules à moteur immatriculés", 'Vols simples sur chantier', 'Vols simples sur exploitations agricoles', 'Autres vols simples contre des établissements publics ou privés', 'Autres vols simples contre des particuliers dans deslocaux privés', 'Autres vols simples contre des particuliers dans des locaux ou lieux publics', 'Recels', 'Proxénétisme', 'Viols sur des majeur(e)s', 'Viols sur des mineur(e)s', 'Harcèlements sexuels et autres agressions sexuelles contre des majeur(e)s', 'Harcèlements sexuels et autres agressions sexuelles contre des mineur(e)s', 'Atteintes sexuelles', 'Homicides commis contre enfants de moins de 15 ans', "Violences, mauvais traitements et abandons d'enfants.", 'Délits au sujet de la garde des mineurs', 'Non versement de pension alimentaire', 'Trafic et revente sans usage de stupéfiants', 'Usage-revente de stupéfiants', 'Usage de stupéfiants', 'Autres infractions à la législation sur les stupéfiants', "Délits de débits de boissons et infraction à la règlementation sur l'alcool et le tabac", "Fraudes alimentaires et infractions à l'hygiène", 'Autres délits contre santé publique et la réglementation des professions médicales', 'Incendies volontaires de biens publics', 'Incendies volontaires de biens privés', "Attentats à l'explosif contre des biens publics", "Attentats à l'explosif contre des biens privés", 'Autres destructions er dégradations de biens publics', 'Autres destructions er dégradations de biens privés', 'Destructions et dégradations de véhicules privés', "Infractions aux conditions générales d'entrée et de séjour des étrangers", "Aide à l'entrée, à la circulation et au séjour des étrangers", 'Autres infractions à la police des étrangers', 'Outrages à dépositaires autorité', 'Violences à dépositaires autorité', 'Port ou détention armes prohibées', 'Atteintes aux intérêts fondamentaux de la Nation', 'Délits des courses et des jeux', 'Délits interdiction de séjour et de paraître', 'Destructions, cruautés et autres délits envers les animaux', "Atteintes à l'environnement", 'Chasse et pêche', "Faux documents d'identité", 'Faux documents concernant la circulation des véhicules', 'Autres faux documents administratifs', 'Faux en écriture publique et authentique', 'Autres faux en écriture', 'Fausse monnaie', 'Contrefaçons et fraudes industrielles et commerciales', 'Contrefaçons littéraires et artistique', 'Falsification et usages de chèques volés', 'Falsification et usages de cartes de crédit', 'Escroqueries et abus de confiance', 'Infractions à la législation sur les chèques', 'Travail clandestin', "Emploi d'étranger sans titre de travail", "Marchandage - prêt de main d'oeuvre", 'Index non utilisé', 'Index non utilisé', 'Banqueroutes, abus de biens sociaux et autres délits de société', 'Index non utilisé', 'Index non utilisé', 'Prix illicittes, publicité fausse et infractions aux règles de la concurrence', 'Achats et ventes sans factures', "Infractions à l'exercice d'une profession règlementée", "Infractions au droit de l'urbanisme et de la construction", 'Fraudes fiscales', 'Autres délits économiques et financiers', 'Autres délits']  # (utilisez la liste complète ici)

# Fonction pour catégoriser les crimes
def categorize_crime(crime):
    # Violence et agression
    if any(substring in crime for substring in ["Homicide", "Tentatives d'homicide", "Coups et blessures", "Prises d'otages", "Séquestrations", "Atteintes à la dignité"]):
        return "Violence et agression"
    
    # Vols et cambriolages
    elif any(substring in crime for substring in ["Vols à main armée", "cambriolage", "Vols simples", "Recels"]):
        return "Vols et cambriolages"
    
    # Infractions sexuelles
    elif any(substring in crime for substring in ["Viols", "Agressions sexuelles", "Atteintes sexuelles", "Harcèlements sexuels"]):
        return "Infractions sexuelles"
    
    # Drogues et stupéfiants
    elif any(substring in crime for substring in ["Stupéfiants"]):
        return "Drogues et stupéfiants"
    
    # Destructions
    elif any(substring in crime for substring in ["Incendies", "Attentats"]):
        return "Destructions"
    
    # Infractions concernant les étrangers
    elif any(substring in crime for substring in ["Infractions aux conditions générales", "Aide à l'entrée"]):
        return "Infractions concernant les étrangers"
    
    # Faux et fraudes
    elif any(substring in crime for substring in ["Faux", "Contrefaçons", "Escroqueries", "Fraudes fiscales"]):
        return "Faux et fraudes"
    
    # Infractions professionnelles et commerciales
    elif any(substring in crime for substring in ["Travail clandestin", "Infractions à l'exercice", "Délits de société"]):
        return "Infractions professionnelles et commerciales"
    
    # Autres délits
    else:
        return "Autres délits"

    
    
df['categorie'] = df['libellé index'].apply(categorize_crime)





years = ["total_2014", "total_2015", "total_2016", "total_2017", "total_2018", "total_2019", "total_2020", "total_2021", "total_2022"]

# Pour chaque année
for year in years:
    # Préparation des données en excluant "Autres délits"
    crime_counts = df[df['categorie'] != "Autres délits"].groupby('categorie')[year].sum()

    # Création du graphique en camembert
    plt.figure(figsize=(10, 7))
    plt.pie(crime_counts, labels=crime_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel", len(crime_counts)))
    plt.title(f"Répartition des types de crimes pour {year}")
    st.pyplot(plt)


