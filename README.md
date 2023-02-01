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
<TODO: beschrijvingen algoritmes kloppen nog niet>

<<<<<<< HEAD
Resultaten:
Resultaten voor de verschillende milestones van het vak zijn te vinden in de map 'milestones'
=======
<Random: Per huis kiezen we willekeurig een batterij en als die batterij vol zit dan blijven we willekeurig een batterij kiezen tot we een batterij vinden die nog niet vol is.Dit doen we totdat alle huizen verbonden zijn.
Het kan zijn dat we nog een of meerdere huizen moeten verbinden met een batterij terwijl alle batterijen al vol zitten en in dat geval verwerpen we de oplossing en herhalen het proces totdat we wel een geldige oplossing vinden. Dan hebben we een oplossing van huis batterij combinaties en moeten we nog de kabels leggen tussen de huizen en batterijen. In het geval van unieke kabels is de kortste route tussen een batterij en huis altijd optimaal voor de kosten,omdat onafhankelijk van welke combinatie huizen en batterijen alleen de lengte van een kabelverbinding bepalend is voor de kosten. dus hebben we als heuristiek gebruikt dat we altijd de korste route kiezen.> 
>>>>>>> 3c3701169b26dc286bea3b8fb5fc4afe46b355d1

<Greedy: bij dit algoritme leggen we de kabels nog steeds op dezelfde manier als het random algoritme alleen veranderen we de manier waarop we de huis batterij combinaties maken. Per huis kiezen we de dichtstbijzijnde batterij die nog niet vol is.
Dit doen we weer totdat alle huizen verbonden zijn. Net zoals bij het random algoritme kan het gebeuren dat voordat alle huizen verbonden zijn alle batterijen al vol zijn, in dit geval verwerpen we de oplossing niet maar gaan we het aanpassen totdat we wel een werkende oplossing krijgen. Dit doen we door random swaps te maken.
Om dit soepeler te laten verlopen hebben we helemaal aan het begin van het algoritme nog een heuristiek gebruikt, namelijk dat we de huizen sorteren op output van groot naar klein, het idee hier achter is dat aangezien we de laatste huizen steeds swappen door deze heuristiek ze makelijker te swappen zijn. >

<Hillclimber: Bij een hillclimber algoritme gebruik je een werkende oplossing en probeer je die te verbeteren door per iteratie
een aanpassing te maken en als die aanpassing een verbetering is ga je vanaf die oplossing weer verder totdat je dit een aantal iteraties gedaan hebt.
Het is het bepalend welke stap je gebruikt om aanpassingen te maken en in ons geval begin je zoals je zag in ons vorige algoritme met een oplossing waarin vast staat welk huis met welke batterij verbonden moet worden en
ook zijn er al kabelverbindingen tussen elk huis en batterij gemaakt. Nu behouden we steeds dezelfde huis batterij combinaties maar elke stap van de HillClimber
kiezen we willekeurig een huis en gaan we alle mogelijke bestaande kabels af en kijken we wat de kortste kabelverbinding voor dat huis naar de batterij is.
Ook moet je er rekening mee houden dat als je een kabelverbinding vervangt dat daardoor andere huizen hun verbinding kunnen kwijtraken, deze leg je dan opnieuw aan en als in totaal alle aanpassingen dan tot een verbetering leiden accepteer je deze veranderingen en anders ga je verder>

### Resultaten:

### Instructies:
<TODO: Het is na lezen van de README duidelijk hoe de resultaten te reproduceren zijn, via een interface (command line), argumenten die meegegeven kunnen worden voor de verschillende functionaliteiten/algoritmen, of bijvoorbeeld een duidelijke uitleg welke file te runnen om welk resultaat te krijgen.>
