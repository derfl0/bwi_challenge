# Code für die BWI Challenge
Dies ist meine Lösung für die BWI Coding Challenge https://www.get-in-it.de/coding-challenge

Ausführung des Codes mittels: python3 bwi.py

Der Code wurde getestet mit:
- Python 2.7.16 (Bei Problemen mit Unicode # -*- coding: utf-8 -*- in bwi.py voranstellen)
- Python 3.7.3
- Python 3.9.1

Bei Problemen mit dem CSV Reader kann der Branch "fallback" mit einer Hardcodierung verwendet werden.

**English version below**

## Algorithmus
Um einen möglichst effizienten Transport zu gewährleisten, suchen wir die effizienteste Methode, um die benötigte Hardware in den Transportern zu verstauen. Zur Realisierung wird ein (virtueller) Suchbaum erstellt, wobei jeder Knoten des Baums ein mögliches Auffüllen der Transporter symbolisiert. An der Wurzel befinden sich beide Transporter in leerem Zustand (Wert = 0).

Jede Ebene des Baums repräsentiert alle Optionen, die Transporter mit Hardware eines Typs zu füllen. Die Hardware der Ebenen ist absteigend nach dem Nutzwert pro Gramm der jeweiligen Hardware sortiert

Beispiel: In Ebene 1 werden alle Gegenstände mit dem höchsten pro Gramm Wert ("Mobiltelefon Outdoor") verwendert. Der Status der Transporter wird als x:y dargestellt, wobei x die Anzahl in Transporter 1 und y die Anzahl in Transporter 2 darstellt.

1. 157:0
2. 156:1
3. 156:0
4. 155:2
5. 155:1
6. 155:0

...

12402. 0:1
12403. 0:0

Da wir den zweiten Transporter nur mit der verbleibenden Anzahl an Hardware füllen können, können wir die theoretische Anzahl an Knoten pro Ebene mit der Gaussschen Summenformel errechnen. Die komplette Anzahl der Knoten erhalten wir durch die Muliplikation mit den darüberliegenden Knoten:

1. 12403
2. 301516930
3. 551775981900
4. 7,574228903541299 x 10^16

...

10. 6481238169803899674027040641700780536000000000000 ( = 205*206*420*421*450*451*60*61*157*158*220*221*620*621*250*251*540*541*370*371 / 2^10 )

Angenommen, wir können 1.000.000 Knoten pro Sekunde überprüfen, müssten wir immer noch 2.0 x 10^31 Jahre rechnen.

## Optimierungen

### Obere Grenze
Je weiter unten im Baum bleibt im Transporter weniger Platz, bis nicht mehr alle Gegenstände der aktuellen Ebene in den Transporter platziert werden können. Daher berechnen wir die maximale Anzahl von Gegenständen, die in jeden Transporter passen, und nehmen das Minimum an **erforderlich und passend**, um die Schleife zu initiieren. (Siehe Codezeile 83 - 87)

Da wir ungefähr 6,7 Tonnen Hardware haben, aber nur 2,0 Tonnen Last, spart dies eine Menge Knoten bereits ein.

### Potentiell verbleibende Punktzahl
Vor dem starten des Suchbaums stellen wir sicher, dass die Ebenen vom höchsten Wert pro Gramm zum niedrigsten geordnet sind (Codezeile 27). An jedem Knoten im Baum erreicht die potenzielle Punktzahl aller Knoten darunter einen Spitzenwert von **insgesamt verfügbarem Restplatz in Gramm * Wert pro Gramm der aktuellen Ebene**. Wenn die Summe des verfügbaren Werts in beiden Transportern und der potenziellen Punktzahl niedriger als der aktuelle Highscore ist, gibt es keine Möglichkeit, dass bei einer Kombination im Baum darunter ein neuer Highscore entsteht. Die Berechnung wird in einer höheren Ebene fortgesetzt. (Codezeile 79)

### Abbruchkriterium absoluter Highscore
Da wir bis zum erreichen des Endes des Suchbaums nie mit Sicherheit sagen können, ob noch eine effizientere Möglichkeit gefunden werden kann, können wir als Abbruchkriterium einen theoretischen Highscore berechnen, der erreichbar wäre, wenn die gesamte Kapazität in einem einzigen Transporter zur Verfügung stehen würde. Dies wird über die Funktion fill_single_transporter berechnet. Wird der dabei erzielte Highscore im Suchbaum erreicht, kann die Suche beendet werden, da ein höherer Nutzwert nicht mehr erreichbar ist.

### Code Optimierung
Derzeit kann der Code eine variable Anzahl von Hardware verarbeiten, die in nutzlast.csv angegeben ist. Es wäre auch möglich, eine variable Anzahl von Transportunternehmen bereitzustellen. Da dies den Code komplexer und langsamer machen würde, habe ich mich entschieden, dies vorerst nicht zu tun.

Gerne ein Pull-Request posten.

## Ergebnis

Erste gefundene Kombination mit einer Gesamtpunktzahl von 74660 (Restgewicht 29 Gramm):

| Hardware | In Transporter 1 | In Transporter 2 |
| ------ | ------ | ------ |
| Mobiltelefon Outdoor | 157 | 0
| Mobiltelefon Heavy Duty | 220 | 0
| Mobiltelefon Büro | 60 | 0
| Tablet outdoor groß | 272 | 98
| Tablet Büro klein | 16 | 579
| Tablet Büro groß | 0 | 0
| Tablet outdoor klein | 0 | 4
| Notebook outdoor | 0 | 0
| Notebook Büro 13" | 0 | 0
| Notebook Büro 14" | 0 | 0

Dies ist die höchste zu erreichende Punktzahl. Es gibt zudem jede Menge weiterer Möglichkeiten. Dazu muss die Höchstpunktzahlgrenze im Code deaktiviert werden. (Siehe Kommentare)
Wenn der Code für eine lange Zeit auf einem Server ausgeführt werden soll, empfehle ich:

nohup python3 -u bwi.py> out.txt &

# Code for BWI
This is my entry for the BWI Coding Challenge https://www.get-in-it.de/coding-challenge

The code was tested for
- Python 2.7.16 (When encountering problems with unicode use # -*- coding: utf-8 -*- at the top of the file)
- Python 3.7.3
- Python 3.9.1

Execute code: python3 bwi.py

When you run into trouble with the csv reader checkout the "fallback" branch with a hardcoding of the requirements.

## Prerequisites
Since in our case volume does not matter but weight does, when talking about available remaining weight the term "space" will be used.

## Algorithm
To solve this problem, we're looking for **the best** solution to arrange our items. To find this, we create a (virtual) search tree representing every single possiblity of stacking our transporters.

Every layer of the tree represents all positilites for 1 items.

Example: In layer 1 we deal with the best item per gram ("Mobiltelefon Outdoor"). We denominate the status of the transporters as x:y where x is the number of items in the first transporter and y is the number of items in the second. The nodes look like this:

1. 157:0
2. 156:1
3. 156:0
4. 155:2
5. 155:1
6. 155:0

...

12402. 0:1
12403. 0:0

Since for each amount of items in the first transporter we get n options for the second, where n is total number of items required - the items already in transporter 1, we can calculate the possibilities using gauss.

To determine the number of possibilities we can multiply the possibilites for each layer:
1. 12403
2. 301516930
3. 551775981900
4. 7,574228903541299 x 10^16

...

10. 6481238169803899674027040641700780536000000000000 ( = 205*206*420*421*450*451*60*61*157*158*220*221*620*621*250*251*540*541*370*371 / 2^10 )

Assuming we can check 1,000,000 Nodes per second we'd have to calculate about 2.0 x 10^31 years.

## Optimizations

### Upper boundary
When progressing down the tree there will be a smaller amount of space left in the transporter up until the point, where not all items of the current layer can be put in a transporter. Therefore we calculate the maximum amount of items that fit in each transporter and take the minimum of **required and fitting** to initiate the loop. (See code line 83 - 87 )

Since we have about 6.7 tons of items but only 2.0 tons of space this will save a ton of computation (pun intended).

### Potential remaining score
Before building the search tree, we make sure, that the layers are ordered from the highest value per gram to lowest. (Code Line 27) So at any node in the tree, the potential score of all nodes below peaks at **total available space in gram * value per gram**. If the sum of the available value in both transporters and the potential score is lower than the actual highscore, there is no way that with any combination in the tree below there will be a new highscore and the node is abandoned. (Code Line 79)

### Abort criterion absolute high score
Since we can never say with certainty whether a more efficient option can be found until the end of the search tree is reached, we can calculate a theoretical high score as a termination criterion that would be achievable if the entire capacity were available in a single transporter. This is calculated using the fill_single_transporter function. If the resulting high score is reached in the search tree, the search can be ended, since a higher utility value can no longer be achieved.

### Coding optimizations
Currently the code is able to deal with a variable amount of items given in nutzlast.csv. It would be possible as well to provide a variable amount of transporters. Since this would add more complexity to the code AND make it slower, i decided not to go for this.

Feel free to post a pull request.

## Result

First combination found with a total score of 74660 (remaining weight 29 grams):

| Item | Number in Transporter 1 | Number in Transporter 2 |
| ------ | ------ | ------ |
| Mobiltelefon Outdoor | 157 | 0
| Mobiltelefon Heavy Duty | 220 | 0
| Mobiltelefon Büro | 60 | 0
| Tablet outdoor groß | 272 | 98
| Tablet Büro klein | 16 | 579
| Tablet Büro groß | 0 | 0
| Tablet outdoor klein | 0 | 4
| Notebook outdoor | 0 | 0
| Notebook Büro 13" | 0 | 0
| Notebook Büro 14" | 0 | 0

This is the highest score that can be achieved. There are also plenty of other options to achieve the same score. To display more of them, the theoretical high score must be deactivated in the code. (See comments)
If you want the code to run on a server for a long time, I recommend:

nohup python3 -u bwi.py> out.txt &
