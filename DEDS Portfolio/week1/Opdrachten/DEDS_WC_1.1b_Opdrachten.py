#%% md
# # Werkcollege-opdrachten Week 1.2
#%% md
# ## Voorbereiding
#%% md
# Importeer in het codeblok hieronder de packages die worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
# N.B.: de 2 reeds geschreven coderegels zorgen ervoor dat eventuele warnings, die code-outputs lelijker maken, uitgezet worden.
#%%

import warnings
import sqlite3
import pandas as pd
warnings.simplefilter('ignore')
#%% md
# Zet de volgende bestanden in een makkelijk terug te vinden map:
# - go_sales_train.sqlite
# - go_crm_train.sqlite
# - go_staff_train.sqlite
#%% md
# Bestudeer de bovenste 3 bestanden in DB Browser (SQLite), <a href="https://sqlitebrowser.org/dl/">hier</a> te downloaden. Wat valt je op qua datatypen?<br>
#%% md
# ## Databasetabel inlezen
#%% md
# Creëer een databaseconnectie met het bestand go_sales_train.sqlite.
#%%
conn = sqlite3.connect("../Data/go_sales_train.sqlite")
sales_conn = conn.cursor()
#%% md
# <b>Let goed op:</b><br>
# Als je per ongeluk een verkeerde bestandsnaam ingeeft, maakt Python zélf een leeg databasebestand aan! Er ontstaat dan dus een nieuwe .sqlite, en dat is nadrukkelijk <u>niet de bedoeling.</u>
#%% md
# Gebruik de onderstaande sql_query om te achterhalen welke databasetabellen in go_sales_train zitten.
#%%
sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
sales_conn.execute(sql_query)
tables = sales_conn.fetchall()

for table in tables:
    print(table[0])

#%% md
# Krijg je lege output? Dan heb je per ongeluk een leeg  databasebestand (.sqlite) aangemaakt.<br>
# Lees de informatie onder het kopje <u>Let goed op:</u> hierboven nog eens goed door.
#%% md
# Gebruik de gecreëerde databaseconnectie om de resultaten van de volgende query in een DataFrame te zetten:<br>
# *SELECT * FROM sales_staff* 
#%%
sales_staff = pd.read_sql("SELECT * FROM sales_staff", conn)
sales_staff
#%% md
# ## Datumkolommen
#%% md
# Zoals je misschien al hebt gezien in DB Browser, zijn datums als TEXT opgeslagen, en niet als DATE, DATETIME o.i.d. Hier moeten we dus nog even "typische datumkolommen" van maken. Dat doen we met de volgende code:
#%%
sales_staff['DATE_HIRED'] = pd.to_datetime(sales_staff['DATE_HIRED'])
sales_staff.dtypes
#%% md
# Als we hier het jaar uit willen halen, schrijven we:
#%%
pd.DatetimeIndex(sales_staff['DATE_HIRED']).quarter
#%% md
# Deze zelfde syntax is te gebruiken voor het extraheren van kwartalen, maanden, weken en dagen. Probeer het maar eens!
#%% md
# ## DataFrames uitsplitsen en opbouwen met Series
#%% md
# De volgende 5 kolommen hebben betrekking op de contactdetails van elke medewerker in dit DataFrame:
# - SALES_STAFF_CODE
# - WORK_PHONE
# - EXTENSION
# - FAX
# - EMAIL
# 
# Maak van elk van deze 5 kolommen een serie.
#%%
a = pd.Series(sales_staff["SALES_STAFF_CODE"])
b = pd.Series(sales_staff["WORK_PHONE"])
c = pd.Series(sales_staff["EXTENSION"])
d = pd.Series(sales_staff["FAX"])
e = pd.Series(sales_staff["EMAIL"])
print(a)
print(b)
print(c)
print(d)
print(e)

#%% md
# Zet allevijf gecreëerde series als kolommen naast elkaar in een DataFrame (*contact_details*). Gebruik pd.concat(...)<br>
# Hulpvraag: welke waarde geef je aan de axis-parameter?
#%%
contact_details = pd.concat([a, b, c, d, e], axis=1)
#%% md
# ## Series en DataFrames maken vanuit lists en dictionaries
#%% md
# Met .head(*getal*) kan je de bovenste *getal* rijen van een tabel selecteren.<br>
# Selecteer op deze manier de bovenste 5 rijen van *contact_details*.<br>
# Sla dit resultaat op in een nieuw DataFrame.
#%%
naam = contact_details.head(5)
naam


#%% md
# Aan deze 10 rijen met contactdetails willen we 3 kolommen toevoegen: 'FIRST_LANGUAGE', 'SECOND_LANGUAGE' & 'THIRD_LANGUAGE'.<br>
# Iedereens 'First Language' is Engels, afgekort 'EN'. Maak een lijst waarin 5x 'EN' staat.<br>
# Converteer deze lijst vervolgens naar een serie en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.
#%%
FIRST_LANGUAGE = ('EN','EN','EN','EN','EN')
naam["FIRST_LANGUAGE"] = pd.Series(FIRST_LANGUAGE)
naam
#%% md
# Maak nu de tweede kolom ('SECOND_LANGUAGE'). Maak daarvoor een dictionary, met daarin...
# - Als keys: alle indexen uit het resultaat van het vorige codeblok.
# - Als values: bij de eerste 3 elementen 'FR' (Frankrijk), bij de laatste 2 'DE' (Duitsland).
# 
# Maak vervolgens ook hier weer een serie van en voeg ook deze weer horizontaal samen met het rsultaat van de vorige opdracht.<br>
# Vergeet niet een passende naam te geven aan de nieuw ontstane kolom.
#%%
SECOND_LANGUAGE = ('FR','FR','FR','FR','FR')
naam["SECOND_LANGUAGE"] = pd.Series(SECOND_LANGUAGE)
naam
#%% md
# Maak ten slotte de derde kolom ('THIRD_LANGUAGE') door een dictionary te maken met daarin...
# - Als key: de naam van de nieuwe kolom. Zie je het verschil qua keys met de vorige opdracht?
# - Als waarde: een lijst met daarin 'NL', 'NL', 'JPN', 'JPN', 'KOR'.
# 
# Converteer deze dictionary nu naar een DataFrame en voeg deze horizontaal samen met het resultaat van de vorige opdracht.<br>
# Waarom hoef je hierna de nieuw ontstane kolom geen passende naam meer te geven?
#%%
THIRD_LANGUAGE = ('DE','DE','DE','DE','DE')
naam["THIRD_LANGUAGE"] = pd.Series(THIRD_LANGUAGE)
naam
sales_staff
#%% md
# ## Data toevoegen
#%% md
# ### Rijen
#%% md
# Gebruik de originele databasetabel *sales_staff*.<br>
# Voeg een extra rij toe met eigen invulling. Zorg ervoor dat de index netjes doorloopt.<br>
# Hulpvraag: welke waarde geef je nu aan axis?
#%%
nieuwe_rij = {'SALES_STAFF_CODE':20,'FIRST_NAME': 'Xander', 'LAST_NAME': 'van der Hoek', 'POSITION': 'VALUE Manager', 'WORK_PHONE': '06 13990925', 'EXTENSION': 410, 'FAX': '+33 1 68 94 56 60', 'EMAIL': 'xandervanderhoek@gmail.com', 'DATE_HIRED': '2006-10-04', 'SALES_BRANCH_CODE': 14}
sales_staff_tabel = pd.DataFrame([nieuwe_rij])
totale = pd.concat([sales_staff_tabel, sales_staff], axis=0)
totale
#%% md
# ### Kolommen
#%% md
# Voeg een kolom *FULL_NAME* toe die de waarden van *FIRST_NAME* en *LAST_NAME* achter elkaar zet, gescheiden door een spatie.
#%%
sales_staff["FULL_NAME"] = sales_staff["FIRST_NAME"] + " " + sales_staff["LAST_NAME"]
sales_staff
#%% md
# ## Data wijzigen
#%% md
# ### Datatypen
#%% md
# Door het attribuut .dtypes van een DataFrame op te vragen krijg je een serie die per kolom het datatype weergeeft. Doe dit bij de originele databasetabel *sales_staff*
#%%
sales_staff.dtypes
#%% md
# Hier valt op dat elke kolom het datatype 'object' heeft: Python leest dus alles als string. Wiskundige operaties zijn hierdoor niet mogelijk.<br>
# We kunnen proberen om kolommen met getallen, bijvoorbeeld de 'extension', te converteren naar een int. Zie onderstaande code.
#%%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(int)

#%% md
# Dit lukt echter niet, omdat er in de kolom 'EXTENSION' lege waarden zitten die niet geconverteerd kunnen worden naar een int.<br>
# Wél kan je deze naar een float converteren, zie onderstaande code:
#%%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(float)
sales_staff.dtypes
#%% md
# Als we in de rij van 'EXTENSION' kijken zien we dat de conversie van het datatype nu is gelukt.<br>
# Dit is <b>randvoorwaardelijk</b> voor het uitvoeren van wiskundige operaties.<br>
#%% md
# ### Rijen
#%% md
# Zorg er nu voor dat bij alle extensions 1 wordt opgeteld.
#%%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'] + 1
sales_staff
#%% md
# Elke 'Branch Manager' wordt nu 'General Manager'. Schrijf code zodat deze wijziging doorgevoerd wordt in het DataFrame.
#%%
sales_staff = pd.DataFrame(sales_staff).replace('Branch Manager', 'General Manager')
#%% md
# ### Kolommen
#%% md
# Verander de kolomnaam 'POSITION_EN' naar 'POSITION'.
#%%
sales_staff = pd.DataFrame(sales_staff).rename({'POSITION_EN': 'POSITION'}, axis = 1)
sales_staff
#%% md
# ## Data verwijderen
#%% md
# ### Rijen
#%% md
# De medewerkers op indexen 99, 100 en 101 hebben helaas ontslag genomen.<br>
# Verwijder de bijbehorende rijen uit het DataFrame. Gebruik slechts één keer de .drop()-methode.
#%%
sales_staff = pd.DataFrame(sales_staff).drop([99,100,101], axis = 0)
#%% md
# ### Kolommen
#%% md
# Faxen zijn inmiddels ouderwets: niemand gebruikt zijn/haar faxnummer nog.<br>
# Verwijder de bijbehorende kolom uit het DataFrame.
#%%
sales_staff = pd.DataFrame(sales_staff).drop('FAX', axis = 1)