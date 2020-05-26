# Inštalačný manuál
V prvom rade je potrebné nahrať najnovší obraz operačného systému *Raspbian* na SD kartu s veľkosťou aspoň 16 GB. Najvhodnejší operačný systém je ***Raspbian Buster Lite***, ktorý je dostupný na oficiálnej stránke raspberrypi.org: https://www.raspberrypi.org/downloads/raspbian/. Slovo *Lite* v názve naznačuje, že sa jedná o verziu bez pracovnej plochy, teda poskytuje iba príkazový riadok. Verzia s pracovnou plochou (*desktop* version) by pri prevádzke len zbytočne zaťažovala počítač.
* vložíme SD kartu do počítača (resp. čítačky kariet)
* stiahneme: https://downloads.raspberrypi.org/raspbian_lite_latest
(možné preskočiť tento krok ak použijeme ***Raspberry Pi Imager***)

Aby sme nahrali stiahnutý obraz na SD kartu, potrebujeme program na nahrávanie obrazov. Odporúčam použiť Raspberry Pi Imager od spoločnosti raspberry.org, ktorý je dostupný pre Windows ako aj Linux a MacOS. Dostupný je na stránke: https://www.raspberrypi.org/downloads/. Ak použijeme ***Raspberry Pi Imager***, nemusíme manuálne sťahovať spomínaný odporúčaný operačný systém, pretože aplikácia nám umožňuje zvoliť si operačný systém, a teda stiahne ho automaticky.
* stiahneme: https://downloads.raspberrypi.org/imager/imager.exe 
* spustíme aplikáciu ***Raspberry Pi Imager v1.2*** (imager.exe)
* CHOOSE OS → Raspbian (other) → Raspbian Lite
* CHOOSE SD → zvolíme kartu, na ktorú chceme nahrať operačný systém (zvyčajne by mala byť na výber iba jedna SD karta)
* klikneme WRITE

Užívatelia využívajúci platformu **UNIX** alebo **UNIX-like** môžu alternatívne vyžiť základný príkaz *dd*. V tomto prípade odporúčam postupovať podľa návodu na oficiálnej stránke raspberrypi.org: https://www.raspberrypi.org/documentation/installation/installing-images/linux.md 

Ďalšiu prácu s mikropočítačom budeme realizovať prostredníctvom SSH protokolu, preto po úspešnom ukončení nahrávania obrazu musíme umožniť SSH komunikáciu. 
* otvoríme boot partíciu (Tento počítač → Zariadenia a jednotky → boot)
* vytvoríme nový súbor **bez prípony** s názvom **ssh**.
* vložíme SD kartu do Raspberry Pi
* zapneme mikropočítač Raspberry Pi
* Chvíľu počkáme a pripojíme sa prostredníctvom SSH protokolu
> (do príkazového riadku napíšeme: ssh pi@raspberrypi)

Po úspešnej inicializácii musíme zadať heslo, ktoré je pri základnom nastavení dané raspberry. Je nevyhnutné, aby sme zmenili toto heslo! Základné meno je pi, ktoré nesmieme zmeniť, pretože by to narušilo správnu prevádzku zariadenia. Pre zmenenie hesla zadáme do príkazového riadka príkaz:
```
sudo passwd root
sudo passwd pi
```
Počas procesu zmeny hesla sme vyzvaní zadať nové heslo a potvrdiť nové heslo.
Na záver stiahneme inštalačný skript spolu s ostatnými skriptmi a potrebnými súbormi zo stránky: https://github.com/straker741/DABreceiver. Následne spustíme inštalačný skript, ktorý keď sa úspešne ukončí, považujeme celý proces inštalácie za ukončený. Pre úplnosť inštalácie postupujte podľa nasledovných príkazov:
```
sudo apt-get update && sudo apt-get install -y git
git clone https://github.com/straker741/DABreceiver
chmod +x DABreceiver/setup.sh
./DABreceiver/setup.sh
```
Inštalácia bude prebiehať približne **30 minút**, pričom na začiatku je potrebné, aby sme zadali IPv4 adresu riadiacej jednotky SNMP protokolu a krátky popis, kde sa zariadenie fyzicky nachádza (bude nachádzať).



# Manuál k obsluhe
Zariadenie môže operovať v dvoch módoch. Prvým z nich je mód ***explore***. Podstata módu ***explore*** je, aby užívateľ bol schopný umiestniť anténu na správne miesto podľa toho ako vyzerá rozloženie výkonu vo frekvenčnom spektre, pričom v tomto móde ešte nedochádza k meraniu a vyhodnocovaniu, teda zasielaniu SNMP trapov. Rozloženie výkonu vo frekvenčnom spektre sa periodicky vypočítavá a vyobrazuje na http stránke zariadenia. Druhým módom je mód monitor. Tento mód, ako sme už naznačili, spúšťa nami upravené welle.io a SNMPhandler.py, ktoré majú za úlohu pozorovať parametre DAB+ vysielania, vyhodnotiť ich a podľa výsledku rozhodnúť, či sa má zaslať SNMP trap na užívateľom zadanú IPv4 adresu.

## Konfigurácia
Konfiguráciu zariadenia je možné vykonať prostredníctvom http stránky, kde môžeme meniť nosnú frekvenciu a pracovný mód. Nosné frekvencie je možné meniť len na presné hodnoty definované pre DAB+ vysielanie v pásme veľmi krátkych vĺn (Band III). Frekvencie s prislúchajúcimi označeniami, ktoré môžeme zvoliť sú uvedené v Tab. 2.

Tab. 2: Nosné frekvencie definované pre DAB+ v pásme Band III

| **Frekvencia [kHz]** | **Kanál** |
|:----------------:|:-----:|
| 174928           | 5A    |
| 176640           | 5B    |
| 178352           | 5C    |
| 180064           | 5D    |
| 181936           | 6A    |
| 183648           | 6B    |
| 185360           | 6C    |
| 187072           | 6D    |
| 188928           | 7A    |
| 190640           | 7B    |
| 192352           | 7C    |
| 194064           | 7D    |
| 195936           | 8A    |
| 197648           | 8B    |
| 199360           | 8C    |
| 201072           | 8D    |
| 202928           | 9A    |
| 204640           | 9B    |
| 206352           | 9C    |
| 208064           | 9D    |
| 209936           | 10A   |
| 211648           | 10B   |
| 213360           | 10C   |
| 215072           | 10D   |
| 216928           | 11A   |
| 218640           | 11B   |
| 220352           | 11C   |
| 222064           | 11D   |
| 223936           | 12A   |
| 225648           | 12B   |
| 227360           | 12C   |
| 229072           | 12D   |
| 230784           | 13A   |
| 232496           | 13B   |
| 234208           | 13C   |
| 235776           | 13D   |
| 237488           | 13E   |
| 239200           | 13F   |
 
Pre vysielač Kamzík platí, že DAB+ je vysielané na frekvencií 227360 kHz, čomu odpovedá kanál 12C.

Ak sa nám už podarilo nájsť správne miesto pre anténu, kde sa rozloženie výkonu vo frekvenčnom spektre podobá teoretickému rozloženiu, tak môžeme prostredníctvom http stránky zmeniť pracovný mód na monitor. Táto zmena naštartuje python skript, ktorý zaručí správne spustenie celého meracieho systému.

Ak chceme zmeniť konfiguráciu nosnej frekvencie alebo pracovného módu priamo v súbore, tak súbor sa nachádza vo */var/www/html/config.txt*. 

V súvislosti so SNMP protokolom môžeme zmeniť IP adresu riadiacej jednotky a stručný popis, kde sa zariadenie fyzicky nachádza. Konfiguračný súbor, ktorým ovládame konfiguráciu SNMP trapov nájdeme v */home/pi/DABreceiver/trapConfig.txt*.
