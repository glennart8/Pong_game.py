## UTVECKLING
1 CHECK -   ADD A TIMER
2 CHECK -   ADD A BALL AFTER A CURTAIN AMOUNT OF TIME
3           MAKE "COINS/POINTS" SHOW UP IN THE MAP TO TRAIN MORE IN COLLISION
4 CHECK -   MAKE THE BALL CHANGE VELOCITY AFTER SOME TIME IF NO ONE SCORES, RESET AFTER GOAL
5 CHECK -   ADD A COOL BACK GROUND
6 CHECK -   MAKE A PADDLE SHOT REPTILES WHICH THE OTHER PLAYER SHOULD AVOID
7 CHECK -   ADD SOME RANDOMS, CHANGED SIZE,SPEED AND COLOR AT A 10 % CHANCE (SKIPPED ANGLE-CHANGE))
8           MAKE AN AI TO MOVE THE OTHER PLAYER
9 CHECK -   DECREACE THE SIZE OF THE PADDLE WHEN SOMEONE REACHES 4/5 GOALS
10          ADD A BOOST THAT CAN BE ACTIVATED A FEW TIMES
11 CHECK -  ADD BACKGROUND MUSIC
12 CHECK -  ADD SOUND EFFECTS FOR COLLISION, REPTILES, POINTS, SPECIAL BALLS

# Problem - Så fort en boll försvinner, kommer en ny. Detta ska inte ske. 
# HADE GLÖMT NOLLSTÄLLA TIDEN FÖR ATT INTE IFSATSEN ALLTID SKA VARA SANN


1. Installera nödvändigt bibliotek
Ladda ner och installera neat-python för att kunna använda NEAT-tekniken.

2. Definiera AI:ns input
Välj vilken data AI:n ska basera besluten på (t.ex. bollposition, paddelposition, hastighet).

3. Skapa konfigurationsfil för NEAT
Ange inställningar som populationstorlek, mutationshastighet och träningsmål i en textfil.

4. Designa belöningssystem
Bestäm hur AI:n belönas/straffas (t.ex. +10 poäng vid träff, -5 vid miss).

5. Koppla AI till spelkontrollerna
Ersätt tangentbordsinput för en paddle med AI:ns beslut (upp/ner).

6. Sätt upp träningsloop
Kör flera generationer av AI:er där varje "generation" testar och förbättrar sig.

7. Lägg till visualisering (valfritt)
Använd diagram för att se hur AI:ns prestation förbättras över generationerna.

8. Testa och justera parametrar
Experimentera med belöningar, input-data och träningshastighet för att optimera resultatet.

9. Spara den bästa AI:n
Exportera den mest framgångsrika AI-versionen när träningen är klar.

10. Analysera och iterera
Låt AI:n spela mot sig själv eller en mänsklig spelare för att identifiera förbättringsområden.

Tips: Börja med en enkel version och lägg till komplexitet gradvis! 🕹️
