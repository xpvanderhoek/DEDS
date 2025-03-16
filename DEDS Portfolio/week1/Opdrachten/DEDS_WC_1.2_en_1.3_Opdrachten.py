#%% md
# # Werkcollege-opdrachten Week 1.3
#%% md
# ## Dependencies importeren
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# Zet eventuele warnings uit.
#%%
import warnings
import sqlite3
import pandas as pd
warnings.simplefilter('ignore')
#%% md
# Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map
#%% md
# ## Databasetabellen inlezen
#%% md
# Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.
#%%
conn = sqlite3.connect("../Data/go_sales_train.sqlite")
sales_conn = conn.cursor()
#%% md
# Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
# - product
# - product_type
# - product_line
# - sales_staff
# - sales_branch
# - retailer_site
# - country
# - order_header
# - order_details
# - returned_item
# - return_reason
#%%
product = pd.read_sql_query("SELECT * FROM product", conn)
product_type = pd.read_sql_query("SELECT * FROM product_type", conn)
product_line = pd.read_sql_query("SELECT * FROM product_line", conn)
sales_staff = pd.read_sql_query("SELECT * FROM sales_staff", conn)
sales_branch = pd.read_sql_query("SELECT * FROM sales_branch", conn)
retailer_site = pd.read_sql_query("SELECT * FROM retailer_site", conn)
country = pd.read_sql_query("SELECT * FROM country", conn)
order_header = pd.read_sql_query("SELECT * FROM order_header", conn)
order_details = pd.read_sql_query("SELECT * FROM order_details", conn)
returned_item = pd.read_sql_query("SELECT * FROM returned_item", conn)
return_reason = pd.read_sql_query("SELECT * FROM return_reason", conn)
#%% md
# Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.
#%% md
# Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:
#%%
sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#Vul dit codeblok verder in
pd.read_sql(sql_query, conn)
#Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.
#%% md
# erachter 
#%% md
# Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>
#%% md
# ## Selecties op één tabel zonder functies
#%% md
# Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)
#%%
producteis = (product['PRODUCTION_COST'] > 50) & (product['PRODUCTION_COST'] < 100)

product.loc[producteis, ("PRODUCT_NAME", 'PRODUCTION_COST')]
#%% md
# Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 
#%%
producteise = (product["MARGIN"] < 0.2) | (product["MARGIN"] > 0.6)
product.loc[(producteise), ("PRODUCT_NAME", 'MARGIN')]
#%% md
# Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)
#%%
currencyeis = (country['CURRENCY_NAME'] == 'francs')

country.loc[currencyeis, ("COUNTRY")]

#%% md
# Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 
#%%
producteis = (product["MARGIN"] > 0.5)
product.loc[(producteis), ("INTRODUCTION_DATE")].drop_duplicates()
#%% md
# Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)
def vraag5():
    eis = (sales_branch['ADDRESS2'].notna()) & (sales_branch['REGION'].notna())
    sales_branch.loc[eis, ["ADDRESS1", "CITY"]]
#%% md
# Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 
#%%
def vraag6():
    eis = (country['CURRENCY_NAME'] == 'dollars') | (country['CURRENCY_NAME'] == 'new dollar')
    country.loc[eis, ("COUNTRY")]
#%% md
# Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 
def vraag7():
    eis = (retailer_site['POSTAL_ZONE'].str[0] == "D") & (retailer_site['ADDRESS2'].notna())

    retailer_site.loc[eis, ["ADDRESS1", "ADDRESS2", "CITY"]]
#%% md
# ## Selecties op één tabel met functies
#%% md
# Geef het totaal aantal producten dat is teruggebracht (1 waarde) 
#%%
def vraag8():
    returned_item.loc[:, ["RETURN_QUANTITY"]].sum()
#%% md
# Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)
#%%
def vraag9():
    sales_branch.loc[:, ["REGION"]].drop_duplicates().shape[0]
#%% md
# Maak 3 variabelen:
# - Een met de laagste
# - Een met de hoogste
# - Een met de gemiddelde (afgerond op 2 decimalen)
# 
# marge van producten (3 kolommen, 1 rij) 
#%%
laagste = product["MARGIN"].min()
hoogste = product["MARGIN"].max()
gemiddelde = product["MARGIN"].mean()

resultaat = pd.DataFrame({
    "Laagste": [laagste],
    "Hoogste": [hoogste],
    "Gemiddelde": [gemiddelde]
})
resultaat.round(2)
#%% md
# Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)
#%%
eis = (retailer_site["ADDRESS2"].isna())
retailer_site.loc[eis, ["RETAILER_SITE_CODE"]].count()
#%% md
# Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 
#%%
korting = order_details['UNIT_SALE_PRICE'] < order_details['UNIT_PRICE']

order_details.loc[korting, ["UNIT_COST"]].mean()
#%% md
# Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 
#%%
sales_staff.groupby("POSITION_EN").size()
#%% md
# Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 
#%%
sales_staff_2 = sales_staff["WORK_PHONE"].value_counts()
resultaat = sales_staff_2[sales_staff_2 > 4]
resultaat
#%% md
# ## Selecties op meerdere tabellen zonder functies
#%% md
# Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 
#%%
land = pd.merge(country, retailer_site, left_on="COUNTRY_CODE", how="inner", right_on="COUNTRY_CODE")
eis = land["COUNTRY"] == "Netherlands"
land.loc[eis, ["ADDRESS1", "CITY"]]
#%% md
# Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen) 
#%%
productje = pd.merge(product_type, product, on="PRODUCT_TYPE_CODE", how="inner")
eis = (productje["PRODUCT_TYPE_EN"] == "Eyewear")
productje.loc[eis, ["PRODUCT_NAME"]]


#%% md
# Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 
#%%
verkochten = pd.merge(sales_staff, order_header, on="SALES_STAFF_CODE")
goede = pd.merge(verkochten, retailer_site, on="RETAILER_SITE_CODE")
eis = (goede["POSITION_EN"] == "Branch Manager")
goede.loc[eis, ["ADDRESS1", "FIRST_NAME", "LAST_NAME"]].drop_duplicates()

#%% md
# Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 
#%%
verkochten = pd.merge(order_header, sales_staff, left_on="SALES_STAFF_CODE", how="right", right_on="SALES_STAFF_CODE")

eis = (verkochten["POSITION_EN"].str.contains("Manager"))
verkochten.loc[eis, ["POSITION_EN", "ORDER_DATE"]].drop_duplicates()


#%% md
# Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 
#%%
productnaam = pd.merge(product, order_details, on="PRODUCT_NUMBER", how="inner")
productcode = pd.merge(productnaam, product_type, on="PRODUCT_TYPE_CODE", how="inner")
eis = (productcode["QUANTITY"] > 750)
productcode.loc[eis, ["PRODUCT_NAME", "PRODUCT_TYPE_EN"]].drop_duplicates()
#%% md
# Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 
#%%
productnaam = pd.merge(order_details, product, on="PRODUCT_NUMBER", how="inner")
eis = ((productnaam["UNIT_PRICE"] - productnaam["UNIT_SALE_PRICE"]) / productnaam["UNIT_PRICE"]) > 0.4
productnaam.loc[eis, ["PRODUCT_NAME"]].drop_duplicates()
#%% md
# Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 
#%%
returnproduct = pd.merge(returned_item, order_details, on="ORDER_DETAIL_CODE", how="inner")
returnreden = pd.merge(returnproduct, return_reason, on="RETURN_REASON_CODE", how="inner")
eis = (returnreden["RETURN_QUANTITY"] / returnreden["QUANTITY"]) > 0.90
returnreden.loc[eis, ["RETURN_DESCRIPTION_EN"]].drop_duplicates()
#%% md
# ## Selecties op meerdere tabellen met functies
#%% md
# Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 
#%%
producttype = product_type.merge(product, on="PRODUCT_TYPE_CODE", how="inner")
productaantal = producttype.groupby("PRODUCT_TYPE_EN").size().reset_index(name="Aantal producten")
productaantal
#%% md
# Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 
#%%
klant = pd.merge(retailer_site, country, on="COUNTRY_CODE", how="inner")
klantperland = klant.groupby("COUNTRY").size().reset_index(name="Aantal vestigingen")
klantperland
#%% md
# Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen) 
#%%
productje = product_type.merge(product, on="PRODUCT_TYPE_CODE", how="inner")
productjes = productje.merge(order_details, on="PRODUCT_NUMBER", how="inner")
producttype = productjes["PRODUCT_TYPE_EN"] == "Cooking Gear"
producttypeje = productjes.loc[producttype]
producttypejes = producttypeje.groupby("PRODUCT_NAME").agg(Aantal_verkocht=("QUANTITY", "sum"), Gemiddelde_prijs=("UNIT_PRICE", "mean"))
gesorteerd = producttypejes.sort_values("Aantal_verkocht", ascending=True)
gesorteerd
#%% md
# Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 
#%%
land = country.merge(sales_branch, on="COUNTRY_CODE", how="inner").rename({"CITY": "VERKOPER"}, axis=1)
klant = country.merge(retailer_site, on="COUNTRY_CODE", how="inner")
eind = klant.groupby("COUNTRY").agg(Aantal_klanten=("RETAILER_SITE_CODE", "nunique")).reset_index()
andereeind = land[['COUNTRY', 'VERKOPER']].drop_duplicates()
allerlaatste = pd.merge(andereeind, eind, on="COUNTRY", how="left")
allerlaatste
#%% md
# ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops
#%% md
# Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 
#%%
medewerkers = sales_staff.merge(order_header, on="SALES_STAFF_CODE", how="left")
nietgekocht = medewerkers["ORDER_NUMBER"].isna()
medewerkers.loc[nietgekocht, ["FIRST_NAME", "LAST_NAME"]]
#%% md
# Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 
#%%
gemiddelde = product["MARGIN"].mean()
lager = product["MARGIN"] < gemiddelde
rijen = product.loc[lager, ["MARGIN"]]
daarvangemiddelde = rijen["MARGIN"].mean()
alleproducten = rijen["MARGIN"].count()
daarvangemiddelde
alleproducten
laatste = pd.DataFrame({"": [daarvangemiddelde, alleproducten]}, index=["Gemiddelde margin", "Gemiddeld aantal producten"])
laatste
#%% md
# Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 
#%%
orderzondernaam = order_details.merge(returned_item, on="ORDER_DETAIL_CODE", how="left")
order = orderzondernaam.merge(product, on="PRODUCT_NUMBER", how="inner")
nietterug = (order["RETURN_CODE"].isna()) & (order["UNIT_PRICE"] > 500)
order.loc[nietterug, ["PRODUCT_NAME"]].drop_duplicates()

#%% md
# Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
# Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).
#%%
medewerkers = sales_staff[["LAST_NAME", "POSITION_EN"]]
for index, medewerker in medewerkers.iterrows():
    Manager = medewerkers.at[index, "POSITION_EN"]
    if "Manager" in Manager:
        medewerkers.at[index, "MANAGER"] = "Ja"
    else:
        medewerkers.at[index, "MANAGER"] = "Nee"
medewerkers = medewerkers.drop("POSITION_EN", axis=1)
medewerkers
#%% md
# Met de onderstaande code laat je Python het huidige jaar uitrekenen.
#%%
from datetime import date
date.today().year
#%% md
# Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.
#%%
from datetime import datetime

date_str = '16-8-2013'
date_format = '%d-%m-%Y'
date_obj = datetime.strptime(date_str, date_format)

date_obj.year
#%% md
# Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
# (2 kolommen, 102 rijen) 
#%%
medewerkers = sales_staff[["LAST_NAME", "DATE_HIRED"]]
ditjaar = date.today().year
medewerkers
for index, medewerker in medewerkers.iterrows():
    date_str = medewerker["DATE_HIRED"]
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, date_format)
    if (ditjaar - date_obj.year) >= 25:
        medewerker["DATE_HIRED"] = "Lang in dienst"
    else:
        medewerker["DATE_HIRED"] = "Kort in dienst"
medewerkers

#%% md
# ## Van Jupyter Notebook naar Pythonproject
#%% md
# 1. Richt de map waarin jullie tot nu toe hebben gewerkt in volgens de mappenstructuur uit de slides.
# 2. Maak van de ontstane mappenstructuur een Pythonproject dat uitvoerbaar is vanuit de terminal. Maak daarin een .py-bestand dat minstens 5 antwoorden uit dit notebook (in de vorm van een DataFrame) exporteert naar Excelbestanden. Alle notebooks mogen als notebook blijven bestaan.
# 3. Zorg ervoor dat dit Pythonproject zijn eigen repo heeft op Github. Let op: je virtual environment moet <b><u>niet</u></b> meegaan naar Github.
# 
# Je mag tijdens dit proces je uit stap 1 ontstane mappenstructuur aanpassen, zolang je bij het beoordelingsmoment kan verantwoorden wat de motivatie hierachter is. De slides verplichten je dus nergens toe.