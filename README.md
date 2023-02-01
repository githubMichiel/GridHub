# GridHub
### Minor programming - SmartGrid

- Introductie:
Veel huizen hebben tegenwoordig installaties om zelf energie mee te produceren, deze leveren vaak meer dan voor eigen consumptie nodig is.
Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en productie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen en 150 huizen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit. Exacte data kun je vinden in deze bestanden <LINK NAAR DATA TOEVOEGEN>. Er moeten kabels aangelegd worden tussen de huizen en batterijen. De kabels kosten 9 per grid segment en de batterijen kosten 5000 per stuk (De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de Manhattan distance). Het doel is door middel van algoritmes en heuristieken de kostenfunctie te optimaliseren (minimaliseren) en binnen de constraints een zo'n optimaal mogelijk resultaat te behalen.

De opdracht heeft de volgende constraints:
- Elk huis moet verbonden zijn met precies één batterij
- Batterijen mogen niet aan elkaar verbonden zijn. Ook niet via een huis.

De opdracht kan opgesplits worden in twee deelopdrachten met de volgende constraints:
1) Elk huis heeft een eigen unieke kabel nodig naar de batterij. Er mogen meerdere kabels over dezelfde gridsegmenten lopen. Het blijven echter wel unieke kabels en leveren geen kostenvermindering op.
2) Huizen mogen via eenzelfde kabel aan een batterij verbonden zijn. Ze mogen dus een kabel delen.

Verder hebben we nog aandacht besteed aan het oplossen van een van de extra opdrachten, namelijk:
Verplaats de batterijen, en probeer een beter resultaat te realiseren.

Algoritmes en heuristieken:

Resultaten:
Resultaten voor de verschillende milestones van het vak zijn te vinden in de map 'milestones'

Instructions:
<TODO: Het is na lezen van de README duidelijk hoe de resultaten te reproduceren zijn, via een interface (command line), argumenten die meegegeven kunnen worden voor de verschillende functionaliteiten/algoritmen, of bijvoorbeeld een duidelijke uitleg welke file te runnen om welk resultaat te krijgen.>
