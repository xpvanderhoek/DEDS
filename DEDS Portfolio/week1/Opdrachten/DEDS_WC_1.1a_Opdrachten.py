#%% md
# # Werkcollege-opdrachten Week 1.1
#%% md
# ## Maak een virtual environment
#%% md
# Zorg dat je met behulp van de handleiding *Bouw en gebruik van virtual environments - Handleiding* een virtual environment hebt gemaakt, dat jou en je duopartner garandeert altijd dezelfde versie van geïmporteerde dependencies te gebruiken.<br>
# Voeg hier vervolgens met *poetry add pandas* de pandas-dependency aan toe.<br>
# Als je dit allemaal goed hebt gedaan moet de onderstaande code bij jullie allebei succesvol runnen:
#%%
import pandas as pd
#%% md
# Zorg er daarnaast voor dat je...
# - Het bestand Waarheidstabel.png in dezelfde map als dit notebook hebt staan.
# - Het bestand Prinstabel.png in dezelfde map als dit notebook hebt staan.
# - Alle informatie onder het kopje *Basisoperaties* van de cheatsheet *Van Java naar Python - Cheatsheet* (zie Brightspace) bij de hand hebt.
#%% md
# ## 1.1: Output, variabelen en input
#%% md
# Geef code waarmee het volgende op het scherm komt te staan:<br>
# geef me je geld <br>
# of ik gebruik geweld, <br>
# toen kwam de controle aangesneld
#%%

#%% md
# Declareer 2 variabelen zodat de volgende tekst geprint wordt:<br>
# Apenhoofd<br>
# Paardenstaart
#%%

#%% md
# Voeg code toe zodat het programma het volgende doet:<br>
# 1): Op het scherm komt A, B, C, D, ..., F, G te staan<br>
# 2): De gebruiker voert een letter in<br>
# 3): Op het scherm komt te staan:<br>
# Het is inderdaad:<br>
# *ingevoerde letter*
#%%

#%% md
# ## 1.2: Stringconcatenatie en Rekenen
#%% md
# Schrijf code dat een inkomen inleest en het volgende uitprint:<br>
# Uw inkomen (*ingelezen inkomen*) is zeer acceptabel.
#%%

#%% md
# De oppervlakte van een driehoek is 1/2 * hoogte * basis<br>
# Schrijf code zodat het programma het volgende doet:<br>
# 1): Op het scherm komt Wat is de basis? te staan<br>
# 2): De gebruiker voert een basis in<br>
# 3): Op het scherm komt Wat is de hoogte? te staan<br>
# 4): De gebruiker voert een hoogte in<br>
# 5): Op het scherm komt: De oppervlakte van de driehoek is *berekende oppervlakte* te staan
#%%

#%% md
# ## 1.3: if() en booleans
#%% md
# Schrijf code dat het volgende doet:<br>
# 1): De gebruiker voert in hoe oud iemand is<br>
# 2): De gebruiker voert in of de ouders meegekomen zijn (input is J of N)<br><br>
# 
# Als...
# - Jonger dan 6, wel ouders: op het scherm staat Je mag het zwembad in
# - Jonger dan 6, geen ouders: op het scherm staat Je mag het niet zwembad in
# - Leeftijd vanaf 6, geen ouders: op het scherm staat Je mag het zwembad in als je een diploma hebt
# - Leeftijd vanaf 6, wel ouders: op het scherm staat Waarom neem je nog je ouders mee?
#%%

#%% md
# Schrijf code zodat de boolean-variabelen een en twee aangemaakt worden en waarmee de juiste waarde in de boolean-variabele uitkomst komt te staan. In de waarheidstabel hieronder staat wat de waarde van uitkomst is bij de verschillende mogelijke combinaties van een en twee.<br><br>
# <img src="Waarheidstabel.png">
#%%

#%% md
# ## 1.4: Methoden
#%% md
# Schrijf een methode wachtwoord die als parameters twee woorden meekrijgt en het volgende controleert:
# - Als de woorden gelijk zijn, print het programma gelijk.
# - Als de woorden ongelijk zijn print het programma ongelijk.
# 
# Vergeet niet dat je de methode niet alleen aan moet maken, maar ook aan moet roepen om output te krijgen.
#%%

#%% md
# Schrijf de methode zoekPrins die als parameter een prinses meekrijgt en vervolgens de bijbehorende prins teruggeeft, volgens de volgende tabel:<br><br>
# <img src="Prinstabel.png"><br>
# Als de naam van de prinses niet in de tabel staat wordt het volgende door de methode teruggegeven: naamloos.<br>
# Roep ten slotte de gemaakte methode ook daadwerkelijk aan met een zelfgekozen prinsessennaam.
#%%

#%% md
# ## 1.5: While
#%% md
# Schrijf de inhoud van de methode wachtwoord. Deze heeft geen parameters en laat de gebruiker twee wachtwoorden invoeren, waarna hij bekijkt of deze gelijk zijn. Zolang dat niet het geval is wordt er eerst Fout, probeer het opnieuw! uitgeprint en moet de gebruiker het opnieuw proberen.<br>Als de gebruiker het goed doet, komt er Succes! op het scherm te staan.
#%%
goed = False
while goed == False:
    wachtwoord = input("Voer wachtwoord in: ")
    herhaal = input("Herhaal wachtwoord")
    if wachtwoord == herhaal:
        print("Succes!")
        goed = True
    else: 
        print("Fout, probeer opnieuw!")
#%% md
# Schrijf de inhoud van de methode tafels. De methode print alle tafels vanaf 1 (dus inclusief de tafel van 1) tot en met de tafel van het meegekregen getal (dus inclusief de tafel van getal).  Zet een witregel tussen alle tafels in. <br>
# Let op:
# - Gebruik een while-loop
# - Gebruik de reeds geschreven methode tafel om een tafel uit te printen
#%%
def tafel(getal: int):
    teller: int = 1

    while(teller <= 10):
        print(f'{teller} x {getal} = {teller * getal}')
        teller += 1

def tafels(getal: int):
    i = 1
    while i <= getal:
        tafel(i)
        i += 1
        print("")

x: int = int(input())
tafels(x)
#%% md
# ## For-loop
#%% md
# Vervang de while-loop door een werkende for-loop. De uitkomst van het programma mag daarbij niet veranderen.
#%%
def loopje():
    aantal = 0

    for aantal in range(1, 11, 1):
        print(f"huidige getal: {aantal}")
        aantal += 1

loopje()
#%% md
# Schrijf de methode checkEven die achtereenvolgens 12 getallen inleest en afdrukt hoe vaak het ingevoerde getal even was.
#%%
def checkEven():
    aantal = 0
    x = 0
    for x in range(1, 13, 1):
        
        if x % 2:
            aantal += 1
    print(aantal)


checkEven()

#%% md
# ## Objectoriëntatie
#%% md
# Maak een minisysteem voor een kledingwinkel. Maak verschillende klassen voor verschillende soorten kledingstukken, waarbij sommige klassen geërfd worden van andere klassen.
# - Maak een klasse Kledingstuk aan, waarin door de constructor een merk, een maat en een prijs geïnitialiseerd worden.
# - Maak een klasse Broek en een klasse Shirt, beide erven van de klasse Kledingstuk. Voeg aan Broek een broek_type, en aan Shirt een shirt_type toe (d.m.v. constructorgebruik).
# - Maak een klasse Spijkerbroek die erft van broek en een klasse Poloshirt die erft van shirt. Voeg aan Spijkerbroek een blauwtint toe, en aan Poloshirt een kraagsoort (d.m.v. constructorgebruik).
# - Implementeer in elke klasse een beschrijf-methode, waarmee alle informatie over het betreffende kledingstuk wordt afgedrukt.
# - Maak van elke klasse een object aan en roep de beschrijfmethode aan. Controleer nauwkeurig of alles naar behoren werkt.
#%%
class Kledingstuk:
    
    def __init__(self, merk, maat, prijs):
        self.merk = merk
        self.maat = maat
        self.prijs = prijs
    def __str__(self):
        return f"{self.merk}({self.maat}) voor {self.prijs}"
    

class Broek(Kledingstuk):
    def __init__(self, merk, maat, prijs, broek_type):
        super().__init__(merk, maat, prijs)
        self.broek_type = broek_type

    def __str__(self):
        return f"{self.merk}({self.maat}) van het type {self.broek_type} voor {self.prijs}"

class Shirt(Kledingstuk):
    def __init__(self, merk, maat, prijs, shirt_type):
        super().__init__(merk, maat, prijs)
        self.shirt_type = shirt_type
    def __str__(self):
        return f"{self.merk}({self.maat}) van het type {self.shirt_type} voor {self.prijs}"

class Spijkerbroek(Broek):
    def __init__(self, merk, maat, prijs, broek_type, blauwtint):
        super().__init__(merk, maat, prijs, broek_type)
        self.blauwtint = blauwtint
    def __str__(self):
        return f"{self.merk}({self.maat}) van het type {self.broek_type} en met de blauwtint {self.blauwtint} voor {self.prijs}"

class Poloshirt(Shirt):
    def __init__(self, merk, maat, prijs, shirt_type, kraagsoort):
        super().__init__(merk, maat, prijs, shirt_type)
        self.kraagsoort = kraagsoort
    def __str__(self):
        return f"{self.merk}({self.maat}) van het type {self.shirt_type} en met de soort kraag {self.kraagsoort} voor {self.prijs}"

k1 = Kledingstuk("asdf", 5666, "veel")
k2 = Broek("asdf", 5666, "veel", "Cool")
k3 = Shirt("asdf", 5666, "veel", "hot")
k4 = Spijkerbroek("asdf", 5666, "veel", "Cool", "licht")
k5 = Poloshirt("asdf", 5666, "veel", "hot", "Hoekig")
print(k1)
print(k2)
print(k3)
print(k4)
print(k5)
    
        
#%% md
# Opmerking: in themaweken 2 t/m 8 ga je objectoriëntatie waarschijnlijk veel minder vaak gebruiken dan de andere boven- en ondergenoemde programmeertechnieken.<br>
# Maar let op: in themaweken 9 en 10 komt objectoriëntatie <b><u>uitvoerig</u></b> aan de orde. Zorg dus dat je deze kennis niet vergeet!
#%% md
# ## Verzamelingen
#%% md
# Kijk nu naar alle info onder het kopje *Verzamelingen* van de cheatsheet *Van Java naar Python - Cheatsheet*.
#%% md
# Initialiseer een lijst met de naam mijn_lijst met de volgende waarden:<br>
# Jelle, Marleen, Henk, Fatima, Jelle, Henk
#%%
mijn_lijst = ["Jelle", "Marleen", "Henk", "Fatima", "Jelle", "Henk"]
#%% md
# Probeer nu de eerste waarde uit te lijst te veranderen in een naam naar keuze. Lukt dat?
#%%
mijn_lijst = ["Jelle", "Marleen", "Henk", "Fatima", "Jelle", "Henk"]
mijn_lijst[4] = "De goede Jelle"
print(mijn_lijst)
#%% md
# Maak van bovengenoemde lijst nu een tupel, genaamd: mijn_tupel.
#%%
mijn_tupel = ("Jelle", "Marleen", "Henk", "Fatima", "Jelle", "Henk")
#%% md
# Probeer nu de eerste waarde uit te tupel te veranderen in een naam naar keuze. Lukt dat?
#%%
mijn_tupel = ("Jelle", "Marleen", "Henk", "Fatima", "Jelle", "Henk")
mijn_tupel = ("De goede Jelle",) + mijn_tupel[1:]
print(mijn_tupel)
#%% md
# Initialiseer een dictionary met de volgende key-value-combinaties:
# - naam: "Jelle"
# - leeftijd: 28
# - beroep: "Docent"
# - hobby: "Volleybal"
#%%
thisdict = {
    "naam": "Jelle",
    "leeftijd": 28,
    "beroep": "Docent",
    "hobby": "Volleybal"
}
#%% md
# Probeer nu de naam te veranderen naar een naam naar keuze. Lukt dat?
#%%
thisdict["naam"] = "Jelle Krupe"
print(thisdict)