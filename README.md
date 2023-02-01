# GridHub
## Minor programming - SmartGrid

### Introductie:
Veel huizen hebben tegenwoordig installaties om zelf energie mee te produceren, deze leveren vaak meer dan voor eigen consumptie nodig is.
Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en productie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen en 150 huizen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit. Exacte data kun je vinden in deze bestanden <LINK NAAR DATA TOEVOEGEN>. Er moeten kabels aangelegd worden tussen de huizen en batterijen. De kabels kosten 9 per grid segment en de batterijen kosten 5000 per stuk (De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de Manhattan distance). Het doel is door middel van algoritmes en heuristieken de kostenfunctie te optimaliseren (minimaliseren) en binnen de constraints een zo'n optimaal mogelijk resultaat te behalen.

### Constraints:
- Elk huis moet verbonden zijn met precies één batterij
- Batterijen mogen niet aan elkaar verbonden zijn. Ook niet via een huis.

De opdracht kan opgesplits worden in twee deelopdrachten met de volgende constraints:
1) Elk huis heeft een eigen unieke kabel nodig naar de batterij. Er mogen meerdere kabels over dezelfde gridsegmenten lopen. Het blijven echter wel unieke kabels en leveren geen kostenvermindering op.
2) Huizen mogen via eenzelfde kabel aan een batterij verbonden zijn. Ze mogen dus een kabel delen.

Verder hebben we nog aandacht besteed aan het oplossen van een van de extra opdrachten, namelijk:
Verplaats de batterijen, en probeer een beter resultaat te realiseren.

### Algoritmes en heuristieken:

<Random: Bij het random algoritme wordt per huis een willekeurige batterij gekozen. In het geval dat deze batterij vol zit wordt een willekeurige andere batterij gekozen totdat een batterij gevonden is die nog niet vol is. Dit gebeurt totdat alle huizen verbonden zijn.
Het kan zijn dat we nog een of meerdere huizen moeten verbinden met een batterij terwijl alle batterijen al vol zitten en in dat geval verwerpen we de oplossing en herhalen het proces totdat we wel een geldige oplossing vinden. Dan hebben we een oplossing van huis batterij combinaties en moeten we nog de kabels leggen tussen de huizen en batterijen. In het geval van unieke kabels is de kortste route tussen een batterij en huis altijd optimaal voor de kosten omdat, onafhankelijk van de combinatie huis-batterij, alleen de lengte van een kabelverbinding bepalend is voor de kosten. Daarom hebben we als heuristiek gebruikt dat we altijd de kortste route kiezen van huis naar batterij.>

<Greedy: Bij het greedy algoritme leggen we de kabels nog steeds op dezelfde manier als bij het random algoritme alleen worden de huis-batterij combinaties anders gemaakt. Per huis wordt steeds gekeken naar de dichtstbijzijnde batterij die nog niet vol is.
Net zoals bij het random algoritme kan het gebeuren dat voordat alle huizen verbonden zijn alle batterijen al vol zijn, in dit geval verwerpen we de oplossing niet maar gaan we het aanpassen totdat er een werkende oplossing ontstaat. Deze aanpassingen worden gemaakt door random swaps te initiëren waarin we de huis-batterij combinatie omwisselen met twee huizen. Uiteindelijk zijn alle huizen dus verbonden met als heuristiek dat de huizen verbonden zijn met de dichtsbijzijnde batterij die nog niet vol is.>

<HillClimber: Bij een hillclimber algoritme gebruik je een werkende oplossing en probeer je die te verbeteren door per iteratie
een (random) aanpassing te maken en deze aanpassing te behouden als dit voor een betere oplossing zorgt. 
Het is bepalend welke stap je gebruikt om aanpassingen in te maken en in ons geval begin je, zoals je zag in het greedy algoritme, met een oplossing waarin vast staat welk huis met welke batterij verbonden is (incl. de kabelligging). Voor de twee huidige HillClimber algoritmes die we toepassen worden de huis-batterij combinaties behouden echter de kabels verwijderd.
Voor de eerste HillClimber veranderen we per iteratie de locatie van de batterij en leggen we vervolgens opnieuw alle kabels neer volgens het greedy algoritme.
Voor de tweede HillClimber swappen we steeds 2 huizen van batterij en leggen we opnieuw de kabels neer volgens het greedy algoritme.
Bij beiden HillClimber algoritmes worden steeds alleen de aanpassingen overgenomen als het voor een verbeterde versie zorgt, in dit geval dus lagere kosten.>

### Resultaten:

### Instructies:
<TODO: Het is na lezen van de README duidelijk hoe de resultaten te reproduceren zijn, via een interface (command line), argumenten die meegegeven kunnen worden voor de verschillende functionaliteiten/algoritmen, of bijvoorbeeld een duidelijke uitleg welke file te runnen om welk resultaat te krijgen.>
< Hoe te gebruiken?
     python main.py [OPTION]
     Option 1 for random algorithm with unique cables
     Option 2 for greedy algorithm with unique cables
     Option 3 for random algorithm with shared cables
     Option 4 for greedy algorithm with shared cables
     Option 5 for greedy algorithm with variable batteries and shared cables
  Na het kiezen van één van deze 5 opties worden de algoritmes toegepast op de huidige data van de districten met de huizen en batterijen.
  In het geval van optie 4 en 5 worden de HillClimbers nog toegpast om de meest optimale resultaten te krijgen per district.
