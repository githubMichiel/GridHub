# GridHub
## Minor programming - SmartGrid

### Introductie:
Veel huizen hebben tegenwoordig installaties om zelf energie mee te produceren, deze leveren vaak meer dan voor eigen consumptie nodig is.
Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en productie te kunnen managen moeten er batterijen geplaatst worden.

Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen en 150 huizen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit. Exacte data kun je [hier](./data) vinden. Er moeten kabels aangelegd worden tussen de huizen en batterijen. De kabels kosten 9 per grid segment en de batterijen kosten 5000 per stuk (De kabels liggen op de gridlijnen, mogen ook gridpunten met een huis passeren, en de afstand van een huis tot een batterij wordt berekend volgens de Manhattan distance). Het doel is door middel van algoritmes en heuristieken de kostenfunctie te optimaliseren (minimaliseren) en binnen de constraints een zo'n optimaal mogelijk resultaat te behalen.

### Constraints:
- Elk huis moet verbonden zijn met precies één batterij
- Batterijen mogen niet aan elkaar verbonden zijn. Ook niet via een huis.

De opdracht kan opgesplits worden in twee deelopdrachten met de volgende constraints:
1) Elk huis heeft een eigen unieke kabel nodig naar de batterij. Er mogen meerdere kabels over dezelfde gridsegmenten lopen. Het blijven echter wel unieke kabels en leveren geen kostenvermindering op.
2) Huizen mogen via eenzelfde kabel aan een batterij verbonden zijn. Ze mogen dus een kabel delen.

Verder hebben we nog aandacht besteed aan het oplossen van een van de extra opdrachten, namelijk:
Verplaats de batterijen, en probeer een beter resultaat te realiseren.

### Algoritmes en heuristieken:

Random: Bij het random algoritme wordt per huis een willekeurige batterij gekozen. In het geval dat deze batterij vol zit wordt een willekeurige andere batterij gekozen totdat een batterij gevonden is die nog niet vol is. Dit gebeurt totdat alle huizen verbonden zijn.
Het kan zijn dat we nog een of meerdere huizen moeten verbinden met een batterij terwijl alle batterijen al vol zitten en in dat geval verwerpen we de oplossing en herhalen het proces totdat we wel een geldige oplossing vinden. Dan hebben we een oplossing van huis batterij combinaties en moeten we nog de kabels leggen tussen de huizen en batterijen. In het geval van unieke kabels is de kortste route tussen een batterij en huis altijd optimaal voor de kosten omdat, onafhankelijk van de combinatie huis-batterij, alleen de lengte van een kabelverbinding bepalend is voor de kosten. Daarom hebben we als heuristiek gebruikt dat we altijd een kortste route kiezen van huis naar batterij. In het geval van gedeelde kabels sorteren we per batterij alle huizen die bij die batterij horen op korste afstand naar de batterij, daarna leggen we per huis kabels aan tussen de batterij of bestaande kabels die al verbonden zijn met de batterij (altijd de kortst mogelijke optie)

Greedy: Bij het greedy algoritme leggen we de kabels nog steeds op dezelfde manier als bij het random algoritme alleen worden de huis-batterij combinaties anders gemaakt. Per huis wordt steeds gekeken naar de dichtstbijzijnde batterij die nog niet vol is.
Net zoals bij het random algoritme kan het gebeuren dat voordat alle huizen verbonden zijn alle batterijen al vol zijn, in dit geval verwerpen we de oplossing niet maar gaan we het aanpassen totdat er een werkende oplossing ontstaat. Deze aanpassingen worden gemaakt door random swaps te initiëren waarin we de huis-batterij combinatie omwisselen met twee huizen. Uiteindelijk zijn alle huizen dus verbonden met als heuristiek dat de huizen verbonden zijn met de dichtsbijzijnde batterij die nog niet vol is.

HillClimber:
De Hillclimber gaat verder vanaf de werkende oplossing die we gevonden hadden met ons greedy algoritme voor gedeelde kabels (hierin staat al vast welk huis met welke batterij verbonden is inclusief de kabelligging). Wij hebben de hillclimber op 2 manieren geimplementeerd, namelijk:
In de eerste HillClimber ziet een iteratie er als volgt uit: eerst kiezen we willekeurig één batterij, dan kiezen we willekeurig één richting waarin deze 1 coordinaat verschoven wordt (zolang dit binnen het grid is en er op die locatie niet al een ander huis of batterij staat). Daarna leggen we opnieuw alle kabels aan zoals beschreven staat bij het greedy algoritme met gedeelde kabels.
Voor de tweede HillClimber swappen we steeds 2 huizen van batterij en leggen we opnieuw de kabels neer volgens het greedy algoritme.
Bij beiden HillClimber algoritmes worden steeds alleen de aanpassingen van één iteratie overgenomen als het voor een verbeterde versie zorgt, in dit geval dus lagere kosten.

### Resultaten:
Onze best gevonden oplossingen voor elk district:

![District 1](https://github.com/githubMichiel/GridHub/blob/main/visualisations/districts/district_1_optimal_100000.png)

District 1: the lowest found cost: 31732

![District 2](https://github.com/githubMichiel/GridHub/blob/main/visualisations/districts/district_2_optimal_100000.png)

District 2: the lowest found cost: 30490

![District 3](https://github.com/githubMichiel/GridHub/blob/main/visualisations/districts/district_3_optimal_100000.png)

District 3: the lowest found cost: 30904

Zie [hier](https://github.com/githubMichiel/GridHub/tree/main/visualisations) onze andere behaalde resultaten

### Instructies:

Run via een command line interface main.py op de volgende manier:

python main.py [OPTIE]

Hierbij is [OPTIE] een integer tussen de 1 en de 5, namelijk: 
     
Optie 1 voor het random algoritme met unieke kabels
     
Optie 2 voor het greedy algoritme met gedeelde kabels
     
Optie 3 voor het random algoritme met unieke kabels
     
Optie 4 voor het greedy algoritme met gedeelde kabels
     
Optie 5 voor het greedy algoritme met gedeelde kabels waarin de locatie van de batterijen aangepast is.
     
Na het kiezen van één van deze 5 opties worden de algoritmes toegepast op de huidige data van de districten met de huizen en batterijen.
In het geval van optie 4 en 5 worden de HillClimbers nog toegepast om de resultaten te verbeteren per district.
