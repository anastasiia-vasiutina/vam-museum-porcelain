#Import von Bibliotheken und Modulen
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time


#--------------------DATEN-IMPORT--------------------
#Einlesen der Objektmetadaten als DataFrame-Objekt
df = pd.read_csv("vam_final.csv", encoding="utf-8")
#---------------------------------------------------


#---------------------FUNKTIONEN----------------------

#Funktion nimmt ein DataFrame sowie zwei Spaltennamen als Strings entgegen und gibt ein neues DataFrame zurück, in dem die Werte der zweiten Spalte nach den Werten der ersten Spalte gruppiert sind und deren Frequenz in der Spalte Anzahl bereits mittels der Funktion .size() gezählt ist

#DOPPELSTATISTIK-FUNKTION
def get_double_stat(df, column_name_a, column_name_b):
    df_double = df[[f"{column_name_a}", f"{column_name_b}"]]
    df_double_grouped = df_double.groupby([f"{column_name_a}", f"{column_name_b}"]).size().reset_index(name="count")
    return df_double_grouped


#Das Gleiche, wie bei der Funktion oben, aber diesmal für drei Spalten

#TRIPELSTATISTIK-FUNKTION
def get_triple_stat(df, column_name_a, column_name_b, column_name_c):
    df_triple = df[[f"{column_name_a}", f"{column_name_b}", f"{column_name_c}"]]
    df_triple_grouped = df_triple.groupby([f"{column_name_a}", f"{column_name_b}", f"{column_name_c}"]).size().reset_index(name="count")
    return df_triple_grouped



#------------------HEADER-----------------------------
#Titel der Website
st.title(":blue[Datenanalyse der Porzellanbestände im Victoria and Albert Museum]", text_alignment="center")

#Liste von IIIF-Links zu sechs Abbildungen aus dem Datensatz
list_images = ["https://framemark.vam.ac.uk/collections/2019LV0550/full/!1000,1000/0/default.jpg",
"https://framemark.vam.ac.uk/collections/2019LM2449/full/!1000,1000/0/default.jpg",
"https://framemark.vam.ac.uk/collections/2019LL0659/full/!1000,1000/0/default.jpg",
"https://framemark.vam.ac.uk/collections/2009CP2969/full/!1000,1000/0/default.jpg",
"https://framemark.vam.ac.uk/collections/2010DY9844/full/!1000,1000/0/default.jpg",
"https://framemark.vam.ac.uk/collections/2010EC3866/full/!1000,1000/0/default.jpg"]

#In diesem Container werden die IIIF-Links aus der Liste von oben aufgerufen. Diese Bilder werden als Dekoration genutzt
with st.container(horizontal=True):
    for i in list_images:
        st.image(i, width=100)



#------------------TABELLE----------------------------
#Überschrift 
st.header("Datensatz im Tabellenformat:", divider="blue")
#Hier wird eine zusätzliche Spalte in der Tabelle erstellt, die IIIF-Links zu Objektabbildungen enthält
df["IIIF_IMAGE_URL"] = ("https://framemark.vam.ac.uk/collections/" + df["_primaryImageId"].astype(str) + "/full/full/0/default.jpg")

#Dieser Code wurde aus der Dokumentation von Streamlit entnommen. Er ermöglicht in der Tabelle die Objektabbildungen anzuzeigen. Dafür nutzt der Code die IIIF-Links aus der Spalte "IIIF_IMAGE_URL". Die Spalte mit Abbildungen wird immer links verankert.
st.data_editor(
    df,
    column_config={
        "IIIF_IMAGE_URL": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots", pinned = True
        )
    },
    hide_index=True,
)
#Gesamtzahl der Objekte im Datensatz:
st.write(f"Der Datensatz enthält {len(df)} Objekte")


#-----------------PALLETTE----------------------------
#Hier werden Farben für die Diagramme festgelegt. Vier Paletten enthalten unterschiedliche Reihenfolge und Anzahl von Farben, die abhängig von dem Umfang jeweiliges Diagramms genutzt werden können
colors_simple = ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#48CAE4", "#90E0EF", "#ADE8F4", "#CAF0F8", "#FFFAE5", "#FFE169","#EDC531", "#C9A227", "#926C15", "#76520E"]


colors_mixed =["#559BF6",
               "#9FBBFB",
               "#57DCF7",
               "#0CBBD2",
               "#D1F1FD",
               "#A1E6F3", 
               "#FDE4CF",
               "#FFCFD2",
               "#03045E",
               "#025BD0",
               "#BBD0FF",
               "#023E8A",
               "#c1d3fe",  
               "#044BA8",
               "#025BD0",
               "#1176F9",
               "#C7D6F7",
               "#CAF6FF",
               "#0096C7",
               "#237099",
               "#BBD0FF", 
               "#B8C0FF", 
               "#C8B6FF",
               "#788BFF",
               "#7781C0",
               "#c1d3fe", 
               "#FFD6FF", 
               "#FFF3DC", 
               "#F5DD90",
               "#bbe6e4",
               "#98F5E1",
               "#B9FBC0",
               "#E9F5DB",
               "#B5C99A"]


colors_mixed2 =["#559BF6",
               "#9FBBFB",
               "#57DCF7",
               "#0CBBD2",
               "#D1F1FD",
               "#A1E6F3", 
               "#03045E",
               "#025BD0",
               "#BBD0FF",
               "#023E8A",
               "#c1d3fe",  
               "#044BA8",
               "#025BD0",
               "#C7D6F7",
               "#CAF6FF",
               "#0096C7",
               "#237099",
               "#BBD0FF", 
               "#B8C0FF", 
               "#C8B6FF",
               "#788BFF",
               "#1176F9",
               "#7781C0",
               "#c1d3fe", 
               "#FFD6FF", 
               "#FFF3DC", 
               "#F5DD90",
               "#FDE4CF",
               "#FFCFD2",
               "#bbe6e4",
               "#98F5E1",
               "#B9FBC0",
               "#E9F5DB",
               "#B5C99A"]


#-------------------RECHNUNG--------------------------

#Diese Funktion nimmt eine Spalte entgegen und entfernt aus der Spalte alle nan-Werte. Sie gibt schließlich die Anzahl der in der Spalte existierenden Daten

def get_numbers(df, colum_name):
    df_subset = df.dropna(subset=colum_name)
    number = len(df_subset)
    return number

#Berechnung der Datenanzahl von bestimmten Spalten 
accession = get_numbers(df, "accessionYear")
maker = get_numbers(df, "_primaryMaker__name")
association = get_numbers(df, "_primaryMaker__association")
currentLoc = get_numbers(df, "_currentLocation__displayName")
cent_num = get_numbers(df, "century")
country_num = get_numbers(df, "country")
place_num = get_numbers(df, "place")
technique_filtered_num = get_numbers(df, "technique_filtered")
style = get_numbers(df, "_sampleStyle")

#Tabellarische Übersicht von vorhandenen Daten in bestimmten Spalten

st.markdown(f"""
| Spalte   |Anzahl der vorhandenen Werten| 
|----------|:-------------:|
| accessionYear |  {accession}|
| _primaryMaker__name |    {maker}   |
| _primaryMaker__association | {association} |
|_currentLocation__displayName|{currentLoc}|
|century|{cent_num}|
|country|{country_num}|
|place|{place_num}|
|technique_filtered|{technique_filtered_num}|
|_sampleStyle|{style}|
   
            """)

#Text
st.write("Beim Bewegen des Mauszeigers auf die jeweilige Grafik, erscheinen am oberen rechten Rand erweiterte Optionen. Darunter finden Sie die Buttons zum Vergrößern und zum Anzeigen im Full-Screen-Modus. Mit der „Lupe“ können Sie einen bestimmten Bereich auswählen, der danach vergrößert angezeigt wird.")



#----------------LAGE IM MUSEUM-----------------------

#Überschrift
st.header("1. Verteilung der Objekte nach Museumsstandorte", divider="blue")

#Neues DataFrame "df_museum" wird erstellt. Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "_currentLocation__displayName" berechnet
df_museum = df["_currentLocation__displayName"].value_counts().reset_index()

#Umbenennung von Spalten in dem DataFrame
df_museum.columns = ["location", "count"]

#Erstellung des Balkendiagramms
museum_bar = px.bar(df_museum, #Datenquelle
                    width=800, #Breite
                    height=800, #Größe
                    x="count", #x-Achse
                    y="location", #y-Achse
                    orientation="h" #Horizontale Orientierung
                    )

#Anzeigen der Grafik       
st.plotly_chart(museum_bar, use_container_width=True)



#-------------VERTEILUNG DER LÄNDER-------------------
#Überschrift
st.header("2. Verteilung der Objekte nach Herkunftsländern", divider="blue")
#Initialisierung eines neuen DataFrames "df_counties_filtered", das die Spalte "country" enthält, in der keine nan-Werte mehr vorhanden sind
df_counties_filtered = df[df["country"] != ""]

#Mittels der Funktion .value_counts() wird die Häufigkeit von Werten in der Spalte "country" berechnet
counties_distribution = df_counties_filtered["country"].value_counts().reset_index()

#Umbenennung von Spalten
counties_distribution.columns = ["country", "count"]

#Erstellung eines Kreisdiagramms
fig_pie_countries = px.pie(
    counties_distribution,
    names="country",
    values="count",
    color_discrete_sequence=colors_simple
)
#Einstellungen für den Layout
fig_pie_countries.update_traces(textposition='inside', textinfo='percent+label')
#Anzeigen des Kreisdiagramms
st.plotly_chart(fig_pie_countries, use_container_width=True)







#----------------KARTE--------------------------------
#Überschrift
st.header("3. Geografische Verteilung der Objekte", divider="blue")
#Initialisierung des DataFrames "df_geo_data_filtered", die die Spalte mit Koordinaten enthält
df_geo_data_filtered = df.dropna(subset=["coordinates"])

#Mithilfe von st.map (streamliteigene Kartendarstellung) werden Geodaten auf einer Weltkarte dargestellt
st.map(df_geo_data_filtered, latitude="latitude", longitude="longitude", size=20, color="#03045E")



#--------------VERTEILUNG DER JAHRHUNDERTE------------
#Überschrift
st.header("4.1. Verteilung der Objekte nach Jahrhunderten", divider="blue")
#Neues DataFrame wird erstellt "centuries_distribution". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "century" berechnet.
centuries_distribution = df["century"].value_counts().reset_index()

#Umbenennung von Spalten
centuries_distribution.columns = ["century", "count"]

#Reihnfolge der Jahrhunderte in der Legende
century_order=["7.0", 
               "9.0", 
               "10.0", 
               "11.0", 
               "12.0",
               "13.0",
               "14.0",
               "15.0",
               "16.0",
               "17.0",
               "18.0",
               "19.0",
               "20.0",
               "21.0"
            ]
centuries_distribution = centuries_distribution.sort_values(by="century")
#Erstellung des Kreisdiagramms
fig_pie_centuries = px.pie(
    centuries_distribution,
    names="century",
    values="count",
    color_discrete_sequence=colors_mixed2,
    category_orders={"century": century_order}
)
#Layout für das Kreisdiagramm
fig_pie_centuries.update_traces(textposition='inside', textinfo='percent+label')
#Anzeigen des Diagramms
st.plotly_chart(fig_pie_centuries, use_container_width=True)



# -----------LÄNDER NACH DEN JAHRHUNDERTEN------------
#Überschrift
st.header("4.2. Verteilung der Objekte nach Herkunftsländern und Jahrhunderten", divider="blue")


#Initialisierung des DataFrames "df_cent_country" mithilfe der Funktion  get_double_stat(), der Spalten "country" und "century" enthält
df_cent_country = get_double_stat(df, "country", "century")

#Erstellung des Balkendiagramms
cent_country_bar = px.bar(df_cent_country, 
                          x="count", 
                          y="century", 
                          color="country", 
                          orientation="h",
                          color_discrete_sequence=colors_mixed2)
#Anzeigen des Balkendiagramms
st.plotly_chart(cent_country_bar, use_container_width=True)


#-----------LÄNDER NACH EINEM JAHRHUNDERT-------------
#Überschrift
st.header("5. Verteilung der Objekte eines Jahrhunderts nach Herkunftsländern", divider="blue")

#Erstellung des Slider-Widgets mit dem Maximalwert 21 und dem Minimalwert 7
century = st.slider("Tragen Sie ein Jahrhundert ein", min_value=7, max_value=21)

#Erstellung des Buttons "Tabelle Anzeigen" 
button_pressed = st.button("Tabelle anzeigen")
#Bedingung, wenn der Button "Tabelle anzeigen" angeklickt ist:
if button_pressed:
    #Initialisierung eines DataFrames "df_one_century", das auf dem DataFrame df_cent_country basiert und Werte für ein ausgewähltes Jahrhundert enthält
    df_one_century = df_cent_country[df_cent_country["century"] == century]
    #Erstellung des Balkendiagramms
    one_century_bar = px.bar(df_one_century, 
                          x="country", 
                          y="count",
                          color = "country", 
                          color_discrete_sequence=colors_mixed)
    #Anzeigen der Grafik
    st.plotly_chart(one_century_bar, use_container_width=True)


#----------------JAHRHUNDERTE NACH EINEM LAND---------
#Überschrift
st.header("6. Verteilung der Objekte eines Herkunftslandes nach Jahrhunderten", divider="blue")
#Initialisierung der Varibale "countries_list", einer Liste von einzigartigen Ländern in der Spalte "country"
countries_list = df["country"].unique().tolist()
#Variable "country_chosen" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
country_chosen = st.menu_button("Land auswählen", options=countries_list)

#wenn die "country_chosen" Werte enthält
if country_chosen:
    #Initialisierung eines DataFrames "df_one_country", das auf dem DataFrame df_cent_country basiert und Werte für das ausgewählte Land enthält
    df_one_country = df_cent_country[df_cent_country["country"] == country_chosen]
    #Erstellung eines Balkendiagramms
    one_country_bar = px.bar(df_one_country, 
                              x="century", 
                              y="count",
                              color = "century", 
                              color_discrete_sequence=colors_mixed)
    #Anzeigen der Grafik
    st.plotly_chart(one_country_bar, use_container_width=True)


#-------------PRODUKTIONSORTE NACH LÄNDERN------------
#Überschrift
st.header("7. Verteilung der Herkunftsorte nach Ländern", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein Land. Nach der Auswahl erscheint ein Balkendiagramm, das die Verteilung der Objekte nach Produktionsorten in diesem Land abbildet. Beachten Sie, dass im Datensatz der exakte Ort nicht immer angegeben ist.")
#Initialisierung des DataFrames "df_country_place" mithilfe der Funktion  get_double_stat(), der Spalten "country" und "place" enthält
df_country_place = get_double_stat(df, "country", "place")
#Variable "country_button" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
country_button = st.menu_button("Land auswählen", options=countries_list, key="get_places")
#Wenn die "country_button" Werte enthält
if country_button:
    #Initialisierung eines DataFrames "df_dist_places", das auf dem DataFrame df_country_place basiert und Werte für das ausgewählte Land enthält
    df_dist_places = df_country_place[df_country_place["country"] == country_button]
    #Erstellung des Balkendiagramms
    dist_places_bar = px.bar(df_dist_places, 
                                  x="place", 
                                  y="count",
                                  color = "place", 
                                  color_discrete_sequence=colors_simple)
    #Anzeigen der Grafik 
    st.plotly_chart(dist_places_bar, use_container_width=True)


#------------------ANKAUFSDATEN(ALLGEMEIN)------------
#Überschrift
st.header("8.1. Verteilung der Objekte nach Ankaufsjahren", divider="blue")
#Neues DataFrame wird erstellt "df_accessionYear". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "accessionYear" berechnet.
df_accessionYear = df["accessionYear"].value_counts().reset_index()
#Umbenennen der Spalten in dem DataFrame
df_accessionYear.columns = ["accession", "count"]
#Erstellung des Balkendiagramms
accessionYear_bar = px.bar(df_accessionYear, 
                    width=1000,
                    height=1000,
                    x="count", 
                    y="accession",
                    orientation="h"
                    )
#Anzeigen der Grafik 
st.plotly_chart(accessionYear_bar, use_container_width=True)





#--------------ANKAUFSDATEN(NACH JAHRHUNDERTE)--------
#Überschrift
st.header("8.2. Verteilung der Objekte nach Ankaufsdatum (Jahrhundert)", divider="blue")

#=====================================================
#Erstellung der Spalte "accession_century" im DataFrame
#Liste von Bedinungen
conditions = [
    (df["accessionYear"] >= 1800) & (df["accessionYear"] < 1900),
    (df["accessionYear"] >= 1900) & (df["accessionYear"] < 2000),
    (df["accessionYear"] >= 2000)
]
#Liste von Folgen
choices = ["19", "20", "21"]
#Auf Basis von Bedinungen und Folgen werden Daten in der Spalte "accessionYear" einem bestimmten Jahrhundert zugeordnet
df["accession_century"] = np.select(conditions, choices, default="unknown")
#=====================================================

#Neues DataFrame wird erstellt "df_accession_centuty". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "accession_century" berechnet.
df_accession_centuty = df["accession_century"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_accession_centuty.columns = ["accession_century", "count"]

#Erstellung eines Balkendiagramms
accessionCent_bar = px.bar(df_accession_centuty, 
                    x="count", 
                    y="accession_century",
                    orientation="h"
                    )
#Anzeigen der Grafik
st.plotly_chart(accessionCent_bar, use_container_width=True)

#--------------ANKAUFSDATEN(NACH JAHRZEHNTE)--------

#Überschrift
st.header("8.3. Verteilung der Objekte nach Ankaufsdatum (Jahrzehnte)", divider="blue")

#=====================================================
#Erstellung der Spalte "decades" auf Basis von Daten in der Spalte "accessionYear". Der Zellinhalt wird zu einer Zeichenkette verarbeitet, in dem die erste drei Zeichen geholt werden und zu denen ein "0" hinzugefügt wird. Am Ende erstellt die Schreibweise wie "1890er"
df["decades"] = df["accessionYear"].apply(lambda x: str(int(x))[0:2]+ str(int(x))[-2] +"0er" if pd.notna(x) else "unknown")
#=====================================================

#Neues DataFrame wird erstellt "df_decades". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "decades" berechnet.
df_decades = df["decades"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_decades.columns = ["accession_decades", "count"]
#Da die Jahrzehnten-Daten vom Datentyp String ist, wird eine Liste mit richtiger Reihnfolge der Kategorien erstellt, damit sie aufsteigend im Balkendiagramm angezeigt werden
dec_list = ["1850er", 
            "1860er",
            "1870er",
            "1880er",
            "1890er",
            "1900er",
            "1910er",
            "1920er",
            "1930er",
            "1940er",
            "1950er",
            "1960er",
            "1970er",
            "1980er",
            "1990er",
            "2000er",
            "2010er",
            "2020er",
            "unknown"]
#Das DataFrame wird nach der Ordnung in der Liste "dec_list" sortiert
df_decades["accession_decades"] = pd.Categorical(
   df_decades["accession_decades"],
    categories=dec_list,
    ordered=True
)
df_decades = df_decades.sort_values(by="accession_decades")

#Erstellung eines Balkendiagramms
accessionDec_bar = px.bar(df_decades, 
                    width=1000,
                    height=1000,
                    x="count", 
                    y="accession_decades",
                    orientation="h"
                    )
#Anzeigen der Grafik      
st.plotly_chart(accessionDec_bar, use_container_width=True)



#-------ANKAUF NACH HERKUNFTSLÄNDERN (NACH JAHREN)----
#Überschrift
st.header("9.1. Ankauf nach Herkunftsländern", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein oder mehrere Länder. Danach erscheint ein Balkendiagramm, das die Ankaufsstatistik für die ausgewählten Länder nach Jahren anzeigt.")

#Variable "countries_accession_options" referenziert ein Multiselekt-Widget mit der Auswahl von Ländern aus dem "countries_list"
countries_accession_options = st.multiselect(
    "Welche Länder möchten Sie vergleichen?",
    countries_list,
    key="get_accesion"
)
#Wenn "countries_accession_options" Werte enthält:
if countries_accession_options:
    #Initialisierung des DataFrames "df_accession" mithilfe der Funktion  get_double_stat(), der Spalten "accessionYear" und "country" enthält
    df_accession = get_double_stat(df, "accessionYear", "country")
    #Initialisierung eines DataFrames "df_country_accession", das auf dem DataFrame "df_accession" basiert und Werte für ausgewählte Länder enthält
    df_country_accession = df_accession[df_accession["country"].isin(countries_accession_options)]
    #Erstellung des Balkendiagramms
    country_accession_bar = px.bar(df_country_accession, 
                                    width=1500,
                                    height=1500,
                                    x="count", 
                                    y="accessionYear",
                                    color = "country", 
                                    orientation="h",
                                    color_discrete_sequence=colors_mixed)
    #Anzeigen der Grafik
    st.plotly_chart(country_accession_bar, use_container_width=True)




#--ANKAUF NACH DEN LÄNDERN (NACH DEN JAHRZEHNTEN)-----

#Überschrift
st.header("9.2. Ankauf nach Herkunftsländern (nach Jahrzehnten)", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein oder mehrere Länder. Danach erscheint ein Balkendiagramm, das die Ankaufsstatistik für die ausgewählten Länder nach Jahrzehnten anzeigt.")
#Variable "countries_accession_options2" referenziert ein Multiselekt-Widget mit der Auswahl von Ländern aus dem "countries_list"
countries_accession_options2 = st.multiselect(
    "Welche Länder möchten Sie vergleichen?",
    countries_list,
    key="get_accesion_dec"
)
#Wenn "countries_accession_options2" Werte enthält:
if countries_accession_options2:
    #Initialisierung des DataFrames "df_accession_dec" mithilfe der Funktion  get_double_stat(), der Spalten "decades" und "country" enthält
    df_accession_dec = get_double_stat(df, "decades", "country")
    #Sortieren des DataFrames nach der Liste "dec_list"
    df_accession_dec["decades"] = pd.Categorical(
    df_accession_dec["decades"],
    categories=dec_list,
    ordered=True
    )
    df_accession_dec = df_accession_dec.sort_values(by="decades")
    #Initialisierung eines DataFrames "df_country_accession_dec", das auf dem DataFrame "df_accession_dec" und Werte für ausgewählte Länder enthält
    df_country_accession_dec = df_accession_dec[df_accession_dec["country"].isin(countries_accession_options2)]
    #Erstellung des Balkendiagramms
    country_accession_dec_bar = px.bar(df_country_accession_dec , 
                                    width=1500,
                                    height=1500,
                                    x="count", 
                                    y="decades",
                                    color = "country", 
                                    orientation="h",
                                    color_discrete_sequence=colors_mixed,
                                    category_orders={"decades": dec_list})
    #Anzeigen der Grafik
    st.plotly_chart(country_accession_dec_bar, use_container_width=True)




#--------ANKAUF NACH JAHRHUNDERTEN (NACH JAHREN)------
#Überschrift
st.header("9.3. Ankauf nach Herstellungsjahrhundert von Objekten", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein oder mehrere Jahrhunderte. Danach erscheint ein Balkendiagramm mit der Verteilung der Objekte nach Ankaufsjahren, die in den ausgewählten Jahrhunderten hergestellt wurden.")
#Initialisierung der Varibale "centuries_list", einer Liste von einzigartigen Jahrhunderten in der Spalte "century"
centuries_list = df["century"].dropna().unique().tolist()
centuries_list.sort()

#Variable "countries_acces_cent_options" referenziert ein Multiselekt-Widget mit der Auswahl von Ländern aus dem "countries_list"
countries_acces_cent_options = st.multiselect(
    "Welche Jahrhunderte möchten Sie vergleichen?",
    centuries_list,
    key="get_accesion_cent"
)
#Wenn "countries_acces_cent_options" Werte enthält:
if countries_acces_cent_options:
    #Initialisierung des DataFrames "df_acc_cent" mithilfe der Funktion  get_double_stat(), der Spalten "accessionYear" und "century" enthält
    df_acc_cent = get_double_stat(df, "accessionYear", "century")
    #Initialisierung eines DataFrames "df_cent_accession", das auf dem DataFrame "df_acc_cent" und Werte für ausgewählte Länder enthält
    df_cent_accession = df_acc_cent[df_acc_cent["century"].isin(countries_acces_cent_options)]
    #Damit im Balkendiagramm verschiedene Jahrhunderte in verschiedener Farbe erscheinen, werden diese in das Typ String umgewandelt
    df_cent_accession["century"] = df_cent_accession["century"].astype(str)
    #Erstellung des Balkendiagramms
    cent_accession_bar = px.bar(df_cent_accession, 
                                    width=1500,
                                    height=1500,
                                    x="count", 
                                    y="accessionYear",
                                    color = "century", 
                                    orientation="h",
                                    color_discrete_map={
                                        "7.0":  "#E9F5DB", 
                                        "9.0":  "#F5DD90", 
                                        "10.0": "#C8B6FF", 
                                        "11.0": "#bbe6e4", 
                                        "12.0": "#FFF3DC",
                                        "13.0": "#57DCF7",
                                        "14.0": "#B5C99A",
                                        "15.0": "#FFCFD2",
                                        "16.0": "#FFD6FF",
                                        "17.0": "#bbe6e4",
                                        "18.0": "#c1d3fe",
                                        "19.0": "#03045E",
                                        "20.0": "#025BD0",
                                        "21.0": "#237099"
                                    }, #Zuordnung der Farben zu Jahrhunderten
                                    category_orders={"century": ["7.0", 
                                                                 "9.0", 
                                                                 "10.0", 
                                                                 "11.0", 
                                                                 "12.0",
                                                                 "13.0",
                                                                 "14.0",
                                                                 "15.0",
                                                                 "16.0",
                                                                 "17.0",
                                                                 "18.0",
                                                                 "19.0",
                                                                 "20.0",
                                                                 "21.0"
                                                                 ]} #Festlegen der Reihnfolge für Jahrhunderte
                                     )
    #Anzeigen der Grafik
    st.plotly_chart(cent_accession_bar, use_container_width=True)




#---ANKAUF NACH JAHRHUNDERTEN (NACH JAHRZEHNTEN)------
#Überschrift
st.header("9.4. Ankauf nach Herstellungsjahrhundert von Objekten (nach Jahrzehnten)", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein oder mehrere Jahrhunderte. Danach erscheint ein Balkendiagramm mit der Verteilung der Objekte nach Ankaufsjahrzehnten, die in den ausgewählten Jahrhunderten hergestellt wurden.")
#Variable "countries_acces_cent_options2" referenziert ein Multiselekt-Widget mit der Auswahl von Ländern aus dem "countries_list"
countries_acces_cent_options2 = st.multiselect(
    "Welche Jahrhunderte möchten Sie vergleichen?",
    centuries_list,
    key="get_accesion_dec_cent"
)
#Wenn "countries_acces_cent_options2" Werte enthält:
if countries_acces_cent_options2:
    #Initialisierung des DataFrames "df_acc_dec_cent" mithilfe der Funktion  get_double_stat(), der Spalten "decades" und "century" enthält
    df_acc_dec_cent = get_double_stat(df, "decades", "century")
    #Initialisierung eines DataFrames "df_cent_accession_dec", das auf dem DataFrame "df_acc_dec_cent" und Werte für ausgewählte Länder enthält
    df_cent_accession_dec = df_acc_dec_cent[df_acc_dec_cent["century"].isin(countries_acces_cent_options2)]
    #Damit im Balkendiagramm verschiedene Jahrhunderte in verschiedener Farbe erscheinen, werden diese in das Typ String umgewandelt
    df_cent_accession_dec["century"] = df_cent_accession_dec["century"].astype(str)
    #Erstellung des Balkendiagramms
    cent_accession_dec_bar = px.bar(df_cent_accession_dec, 
                                    width=1500,
                                    height=1500,
                                    x="count", 
                                    y="decades",
                                    color = "century", 
                                    orientation="h",
                                    color_discrete_map={
                                        "7.0":  "#E9F5DB", 
                                        "9.0":  "#F5DD90", 
                                        "10.0": "#C8B6FF", 
                                        "11.0": "#bbe6e4", 
                                        "12.0": "#FFF3DC",
                                        "13.0": "#57DCF7",
                                        "14.0": "#B5C99A",
                                        "15.0": "#FFCFD2",
                                        "16.0": "#FFD6FF",
                                        "17.0": "#bbe6e4",
                                        "18.0": "#c1d3fe",
                                        "19.0": "#03045E",
                                        "20.0": "#025BD0",
                                        "21.0": "#237099"
                                    },
                                    category_orders={"century": ["7.0", 
                                                                 "9.0", 
                                                                 "10.0", 
                                                                 "11.0", 
                                                                 "12.0",
                                                                 "13.0",
                                                                 "14.0",
                                                                 "15.0",
                                                                 "16.0",
                                                                 "17.0",
                                                                 "18.0",
                                                                 "19.0",
                                                                 "20.0",
                                                                 "21.0"
                                                                 ],
                                                     "decades": dec_list}
                                     )
    #Anzeigen der Grafik      
    st.plotly_chart(cent_accession_dec_bar, use_container_width=True)


#-----PRODUKTIONSORTE EINES LANDES + JAHRHUNDERTE-----

#Überschrift
st.header("10.1. Verteilung der Objekte nach Herkunftsorten und Jahrhunderten", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein Land, für das Sie die zeitliche Verteilung der Objekte nach exakten Produktionsorten sehen möchten. Beim Doppelklick auf einen Ort in der Legende können Sie dessen Entwicklung gesondert anzeigen lassen.")
#Initialisierung des DataFrames "df_pl_co_ce" mithilfe der Funktion  get_triple_stat(), der Spalten "country", "place" und "century" enthält
df_pl_co_ce = get_triple_stat(df, "country", "place", "century")

countries_list = df["country"].unique().tolist()
#Variable "country_place_century_button" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
country_place_century_button = st.menu_button("Land auswählen", 
                                              options=countries_list,
                                              key="get_places_centuries")

#wenn die "country_place_century_button" Werte enthält
if country_place_century_button:
    #Initialisierung eines DataFrames "df_one_country2", das auf dem DataFrame df_country_place basiert und Werte für das ausgewählte Land enthält
    df_one_country2 = df_pl_co_ce[df_pl_co_ce["country"] == country_place_century_button]
    #Erstellung des Liniendiagramms
    pl_co_ce_bar = px.line(df_one_country2 , 
                              x="century", 
                              y="count",
                              color = "place", 
                              color_discrete_sequence=colors_mixed)
    #Anzeigen der Grafik
    st.plotly_chart(pl_co_ce_bar, use_container_width=True)





#-------PRODUKTIONSORTE EINES LANDES + ANKAUF---------
#Überschrift
st.header("10.2. Verteilung der Ankäufe nach Herkunftsorten", divider="blue")

st.write("Wählen Sie im Dropdown-Menü ein Land, für das Sie die Ankaufsstatistik der Objekte nach exakten Produktionsorten sehen möchten. Beim Doppelklick auf einen Ort in der Legende können Sie dessen Entwicklung gesondert anzeigen lassen.")
#Initialisierung des DataFrames "df_pl_co_acc" mithilfe der Funktion  get_triple_stat(), der Spalten "country", "place" und "accessionYear" enthält
df_pl_co_acc = get_triple_stat(df, "country", "place", "accessionYear")

countries_list = df["country"].unique().tolist()
#Variable "country_place_acc_button" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
country_place_acc_button = st.menu_button("Land auswählen", 
                                           options=countries_list,
                                           key="get_places_accession")

#wenn die "country_place_acc_button" Werte enthält
if country_place_acc_button:
    #Initialisierung eines DataFrames "df_one_country3", das auf dem DataFrame df_country_place basiert und Werte für das ausgewählte Land enthält
    df_one_country3 = df_pl_co_acc[df_pl_co_acc["country"] == country_place_acc_button]
    #Erstellung des Liniendiagramms
    pl_co_acc_bar = px.line(df_one_country3, 
                              x="accessionYear", 
                              y="count",
                              color = "place", 
                              color_discrete_sequence=colors_mixed)
    #Anzeigen der Grafik
    st.plotly_chart(pl_co_acc_bar, use_container_width=True)





#-------------------OBJEKTKATEGORIEN------------------
#Überschrift
st.header("11.1. Verteilung der Objekttypen", divider="blue")
#Neues DataFrame wird erstellt "df_type". Mittels der Funktion .value_counts() wird die die Frequenz der Kategorien in der Spalte "objectType" berechnet.
df_type = df["objectType"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_type.columns = ["objects", "count"]
#Erstellung eines Balkendiagramms
objects_distribution_bar = px.bar(df_type, 
                                  width=1000,
                                  height=2000,
                                  x="count", 
                                  y="objects",
                                  orientation="h",
                                  color_discrete_sequence=colors_mixed
                                )
#Anzeigen der Grafik         
st.plotly_chart(objects_distribution_bar, use_container_width=True)




#-------------OBJEKTKATEGORIEN + LÄNDER---------------
#Überschrift
st.header("11.2. Verteilung der Objekttypen nach Herkunftsländern", divider="blue")

st.write("Wählen Sie im Dropdown-Menü ein Land, für das Sie die Verteilung der Objektkategorien sehen möchten.")
#Initialisierung des DataFrames "df_type_country" mithilfe der Funktion  get_double_stat(), der Spalten "objectType" und "country" enthält
df_type_country = get_double_stat(df, "objectType", "country")
#Variable "type_country" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
type_country = st.menu_button("Land auswählen", options=countries_list, key="get_types_countries")
#wenn die "type_country" Werte enthält
if type_country:
    #Initialisierung eines DataFrames "df_type_one_c", das auf dem DataFrame df_country_place basiert und Werte für das ausgewählte Land enthält
    df_type_one_c = df_type_country[df_type_country["country"] == type_country]
    #Erstellung des Balkendiagramms
    type_country_bar = px.bar(df_type_one_c, 
                                  x="count", 
                                  y="objectType",
                                  orientation="h")
    #Anzeigen der Grafik 
    st.plotly_chart(type_country_bar, use_container_width=True)



#--------OBJEKTKATEGORIEN + JAHRHUNDERTE--------------
#Überschrift
st.header("11.3. Verteilung der Objekttypen nach Jahrhunderten", divider="blue")
#Initialisierung des DataFrames "df_type_cent" mithilfe der Funktion  get_double_stat(), der Spalten objectType" und "century" enthält
df_type_cent = get_double_stat(df, "objectType", "century")
#Initialisierung des DataFrames "df_type_cent_small", der nur die Daten enhthält, deren Frequenz mehr als 20 beträgt.
df_type_cent_small = df_type_cent[df_type_cent["count"] > 20]
#Erstellung des Liniendiagramms
type_cent_chart = px.line(df_type_cent_small, 
                        width=800,
                        height=800,
                        x="century", 
                        y="count",
                        color="objectType",
                        color_discrete_sequence=colors_mixed
                        )
#Anzeigen der Grafik           
st.plotly_chart(type_cent_chart, use_container_width=True)


#-----------------TECHNIKEN---------------------------
#Überschrift
st.header("12.1. Verteilung der Techniken", divider="blue")
#Neues DataFrame wird erstellt "df_tech". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "technique_filtered" berechnet.
df_tech = df["technique_filtered"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_tech.columns = ["technique", "count"]
#Erstellung eines Balkendiagramms
tech_distribution_bar = px.bar(df_tech, 
                               width=1000,
                               height=1000,
                               x="count", 
                               y="technique",
                               orientation="h",
                               )
#Anzeigen der Grafik      
st.plotly_chart(tech_distribution_bar, use_container_width=True)




#--------------TECHNIKEN + JAHRHUNDERTE---------------
#Überschrift
st.header("12.2. Verteilung der Techniken nach Jahrhunderten", divider="blue")
#Initialisierung des DataFrames "df_tech_cent" mithilfe der Funktion  get_double_stat(), der Spalten "technique_filtered" und "century" enthält
df_tech_cent = get_double_stat(df, "technique_filtered", "century")
df_tech_cent_small = df_tech_cent[df_tech_cent["count"] > 10]
#Erstellung des Liniendiagramms
tech_cent_chart = px.line(df_tech_cent_small, 
                        width=800,
                        height=800,
                        x="century", 
                        y="count",
                        color="technique_filtered",
                        color_discrete_sequence=colors_mixed
                        )
#Anzeigen der Grafik           
st.plotly_chart(tech_cent_chart, use_container_width=True)


#-----PRODUKTIONSORTE EINES LANDES + TECHNIKEN--------
#Überschrift
st.header("12.3. Verteilung der Techniken nach Herkunftsorten", divider="blue")
#Text
st.write("Wählen Sie im Dropdown-Menü ein Land, für das Sie die Verteilung der Techniken nach bestimmten Produktionsort sehen möchten.")
#Initialisierung des DataFrames "df_type_places" mithilfe der Funktion  get_triple_stat(), der Spalten "technique_filtered", "place" und "country" enthält
df_type_places = get_triple_stat(df, "technique_filtered", "country", "place")
#Variable "tech_country" referenziert ein Menü-Widget mit der Auswahl von Ländern aus dem "countries_list"
tech_country = st.menu_button("Land auswählen", options=countries_list, key="get_tech_countries")
#wenn die "tech_country" Werte enthält
if tech_country:
    #Initialisierung eines DataFrames "df_tech_one_c", das auf dem DataFrame df_country_place basiert und Werte für das ausgewählte Land enthält
    df_tech_one_c = df_type_places[df_type_places["country"] == tech_country]
    #Erstellung des Balkendiagramms
    tech_places_bar = px.bar(df_tech_one_c, 
                                  x="place", 
                                  y="count",
                                  color="technique_filtered",
                                  color_discrete_sequence=colors_mixed
                                  )
    #Anzeigen der Grafik   
    st.plotly_chart(tech_places_bar, use_container_width=True)


#---------------------KÜNSTLER------------------------
#Überschrift
st.header("13. Verteilung der Objekte nach Herstellern und ihrer Spezifikation", divider="blue")
#Initialisierung des DataFrames "df_artist" mithilfe der Funktion  get_double_stat(), der Spalten "_primaryMaker__name" und "_primaryMaker__association" enthält
df_artist = get_double_stat(df, "_primaryMaker__name", "_primaryMaker__association")
#Erstellung des Balkendiagramms
artist_bar = px.bar(df_artist, 
                    width=800,
                    height=1500,
                    x="count", 
                    y="_primaryMaker__name", 
                    color="_primaryMaker__association", 
                    orientation="h",
                    color_discrete_sequence=colors_mixed2)
#Anzeigen der Grafik
st.plotly_chart(artist_bar, use_container_width=True)


#--------------------MATERIAL-------------------------

#Überschrift
st.header("14. Verteilung der Objekte nach dem Material", divider="blue")
#Neues DataFrame wird erstellt "df_material". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "_sampleMaterial" berechnet.
df_material = df["_sampleMaterial"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_material.columns = ["material", "count"]
#Erstellung eines Balkendiagramms
material_bar = px.bar(df_material, 
                                    x="count", 
                                    y="material",
                                    orientation="h",
                                    )
#Anzeigen der Grafik           
st.plotly_chart(material_bar, use_container_width=True)


#--------------------STYLE----------------------------
#Überschrift
st.header("15. Verteilung der Objekte nach dem Stil", divider="blue")
#Neues DataFrame wird erstellt "df_style". Mittels der Funktion .value_counts() wird die Frequenz der Kategorien in der Spalte "_sampleStyle" berechnet.
df_style = df["_sampleStyle"].value_counts().reset_index()
#Umbenennung von Spalten in dem DataFrame
df_style.columns = ["style", "count"]
#Erstellung eines Balkendiagramms
style_bar = px.bar(df_style, 
                    width=1000,
                    height=1500,
                    x="count", 
                    y="style",
                    orientation="h",
                    )
#Anzeigen der Grafik          
st.plotly_chart(style_bar, use_container_width=True)


#--------------------STILE + LÄNDER--------------------
#Überschrift
st.header("16.1. Verteilung der Objekte nach dem Stil und Herkunftsländern", divider="blue")
#Initialisierung des DataFrames "df_co_style" mithilfe der Funktion  get_double_stat(), der Spalten "_sampleStyle" und "country" enthält
df_co_style = get_double_stat(df, "_sampleStyle", "country")
#Erstellung des Balkendiagramms
style_co_bar = px.bar(df_co_style, 
                    width=800,
                    height=1500,
                    x="count", 
                    y="country", 
                    color="_sampleStyle", 
                    orientation="h",
                    color_discrete_sequence=colors_mixed2)
#Anzeigen der Grafik
st.plotly_chart(style_co_bar, use_container_width=True)


#-----------------STILE + ANKAUF----------------------
#Überschrift
st.header("16.2. Verteilung der Stile nach Ankaufsjahrzehnten", divider="blue")
#Initialisierung des DataFrames "df_style_acc" mithilfe der Funktion  get_double_stat(), der Spalten "_sampleStyle" und "decades" enthält
df_style_acc = get_double_stat(df, "_sampleStyle", "decades")
#Erstellung des Balkendiagramms
style_acc_bar = px.bar(df_style_acc, 
                                  x="count", 
                                  y="decades",
                                  color="_sampleStyle",
                                  color_discrete_sequence=colors_mixed,
                                  category_orders={"decades": dec_list}
                                  )
#Anzeigen der Grafik   
st.plotly_chart(style_acc_bar, use_container_width=True)


#--------------------FOOTER---------------------------

st.subheader("Quelle für den Datensatz und Abbildungen:")
st.markdown("Victoria and Albert Museum (2021) _Victoria and Albert Museum Collections Data_ (data retrieved via [Victoria and Albert Museum Collections API](https://developers.vam.ac.uk)), https://collections.vam.ac.uk/")

st.caption("""Die Webseite entstand als Prüfungsleistung für das Seminar „Kulturgutdaten für Forschungsfragen“ unter der Leitung Dr. habil. Angela Dreßen im Sommersemester 2026 an der Technischen Universität Dresden und dient keinen kommerziellen Zwecken
""")


