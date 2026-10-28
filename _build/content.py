# -*- coding: utf-8 -*-
"""Inhoud van Tandartspraktijk Slotplantsoen (Nederlands).

Teksten zijn herschreven op basis van de oude website en aangevuld voor
vindbaarheid. Feiten (team, tijden, telefoonnummers) komen van praktijkslotplantsoen.nl.
"""

TEAM = {
    "safae":    ("Safae Serghini", "Tandarts, esthetische tandheelkunde", "tandarts"),
    "alvaro":   ("Alvaro Soler", "Tandarts-implantoloog", "tandarts"),
    "mauricio": ("Mauricio Rosenfeld Bochicchio", "Tandarts", "tandarts"),
    "kinan":    ("Kinan Khalil", "Tandarts", "tandarts"),
    "anna":     ("Anna Egea Hugué", "Tandarts orthodontie", "tandarts"),
    "ina":      ("Ina", "Paro-preventieassistente", "mondzorg"),
    "marloes":  ("Marloes", "Tandarts-, preventie- en orthoassistente", "mondzorg"),
    "naima":    ("Naïma", "Tandarts- en preventieassistente", "mondzorg"),
    "elisa":    ("Elisa", "Tandarts- en preventieassistente", "mondzorg"),
    "hanita":   ("Hanita", "Tandartsassistente", "mondzorg"),
    "freek":    ("Freek Zieck", "Tandprotheticus", "prothetiek"),
    "sanae":    ("Sanae Uahhoudi", "Tandprotheticus", "prothetiek"),
    "ferdy":    ("Ferdi Lippolt", "Tandtechnieker", "prothetiek"),
    "brigitte": ("Brigitte Hendriks", "Praktijkmanager", "management"),
}

# slug, menunaam, korte omschrijving, icoon
TREATMENTS = [
    ("esthetische-behandelingen", "Esthetisch", "Facings, witte vullingen en kronen voor een mooiere glimlach.", "esthetisch"),
    ("bleken", "Bleken", "Veilig enkele tinten witter, onder begeleiding van de tandarts.", "bleken"),
    ("implantaten", "Implantaten", "Kroon, brug of klikgebit op implantaten, met CBCT in huis.", "implantaten"),
    ("kronen-en-bruggen", "Kronen en bruggen", "Op maat gemaakt in ons eigen tandtechnisch laboratorium.", "kronen"),
    ("protheses", "Protheses", "Kunstgebit, klikgebit of frame door onze tandprothetici.", "protheses"),
    ("othodontie-en-invisalign", "Orthodontie & Invisalign", "Rechte tanden met onzichtbare, uitneembare aligners.", "orthodontie"),
    ("vullingen", "Vullingen", "Tandkleurige composietvullingen, verdoving als u dat wilt.", "vullingen"),
    ("extractie-trekken", "Extractie (trekken)", "Rustig en goed verdoofd, met duidelijke nazorg.", "extractie"),
    ("wortelkanaalbehandeling", "Wortelkanaalbehandeling", "Ontsteking weg, eigen tand behouden.", "wortelkanaal"),
    ("preventie-en-mondhygiene", "Preventie en mondhygiëne", "Gezond tandvlees en minder gaatjes, met persoonlijk advies.", "preventie"),
]

T = {}

T["esthetische-behandelingen"] = dict(
    title="Esthetische tandheelkunde Meppel | Facings, kronen & bleken",
    desc="Mooiere tanden in Meppel met facings, witte vullingen, kronen of bleken. Eerst uw wensen, dan een helder plan met begroting. Tandartspraktijk Slotplantsoen.",
    h1='Esthetische tandheelkunde in <em class="g">Meppel</em>',
    lead="Een mooiere glimlach die wel natuurlijk oogt. Met facings, tandkleurige vullingen, kronen of bleken verbeteren we de kleur, vorm of stand van uw tanden, op basis van uw wensen en een heldere begroting.",
    img="bleken.webp", img_alt="Close-up van een stralende, natuurlijk witte glimlach",
    procedure="Esthetische tandheelkunde",
    who=["safae"],
    body="""
<h2>Wat kan er met esthetische tandheelkunde?</h2>
<p>Steeds meer mensen kiezen voor een behandeling die hun gebit mooier maakt. Denk aan een verkleurde voortand, een afgebroken hoekje, een opening tussen de tanden of oude, grijze vullingen die u liever kwijt bent. Bij Tandartspraktijk Slotplantsoen kijken we eerst naar de gezondheid van uw gebit en pas daarna naar het uiterlijk: een mooi resultaat moet ook lang meegaan.</p>
<ul class="types">
  <li><b>Facings</b><span>Dunne schaaltjes van keramiek of composiet op de voorkant van de tand. Ideaal bij verkleuring, kleine scheefstand of slijtage.</span></li>
  <li><b>Tandkleurige vullingen</b><span>Oude amalgaam- of verkleurde vullingen vervangen door composiet in de kleur van uw tand.</span></li>
  <li><b>Kronen en bruggen</b><span>Voor zwaar beschadigde of ontbrekende tanden, natuurgetrouw van keramiek.</span></li>
  <li><b>Bleken</b><span>Uw eigen tanden enkele tinten lichter, veilig onder begeleiding van de tandarts.</span></li>
</ul>
<h2>Zo verloopt een esthetische behandeling</h2>
<ol>
  <li><b>Kennismaking.</b> U vertelt wat u zou willen veranderen. De tandarts onderzoekt uw gebit en tandvlees en legt uit wat mogelijk is.</li>
  <li><b>Plan en begroting.</b> U krijgt een behandelplan dat past bij uw wensen én uw budget, met vooraf een duidelijke begroting.</li>
  <li><b>Behandeling.</b> Facings, kronen en bruggen worden op maat gemaakt in ons eigen tandtechnisch laboratorium, zodat kleur en vorm precies aansluiten.</li>
  <li><b>Nazorg.</b> U krijgt tips om het resultaat mooi te houden en we controleren het bij uw halfjaarlijkse controle.</li>
</ol>
<div class="note"><p><b>Vergoeding.</b> Esthetische behandelingen voor volwassenen vallen meestal niet onder de basisverzekering. Een aanvullende tandartsverzekering vergoedt soms een deel. Lees meer over <a href="{u:homepage/betalen-en-vergoedingen/}">verzekering en vergoedingen</a>.</p></div>
""",
    faq=[
        ("Wat is het verschil tussen een facing en een kroon?", "Een facing is een dun schaaltje dat op de voorkant van de tand wordt geplakt; er hoeft weinig van de tand te worden weggeslepen. Een kroon omsluit de hele tand en is bedoeld voor tanden die verzwakt of zwaar beschadigd zijn."),
        ("Verkleuren facings door koffie of thee?", "Keramische facings verkleuren niet door koffie, thee of wijn. Composiet facings zijn voordeliger, maar kunnen na verloop van tijd wat verkleuren en vragen af en toe onderhoud."),
        ("Krijg ik vooraf te horen wat het kost?", "Ja. U krijgt altijd eerst een behandelplan met begroting. Bij behandelingen boven de € 250 kunt u om een schriftelijke begroting vragen."),
    ],
    related=["bleken", "kronen-en-bruggen", "othodontie-en-invisalign"],
)

T["bleken"] = dict(
    title="Tanden bleken Meppel | Veilig bij de tandarts | Slotplantsoen",
    desc="Tanden laten bleken in Meppel? Bij Tandartspraktijk Slotplantsoen bleekt u veilig onder begeleiding van de tandarts, enkele tinten witter. Lees hoe het werkt.",
    h1='Tanden <em class="g">bleken</em> bij de tandarts',
    lead="Tanden worden in de loop der jaren vanzelf donkerder. Met een veilige bleekbehandeling onder begeleiding van de tandarts wordt uw gebit enkele tinten lichter, met een resultaat dat natuurlijk blijft.",
    img="bleken.webp", img_alt="Glimlach met natuurlijk witte tanden na een bleekbehandeling",
    procedure="Tanden bleken",
    who=["safae"],
    body="""
<h2>Waarom worden tanden donkerder?</h2>
<p>Een wit gebit is populair en de vraag naar bleken neemt toe. Dat tanden verkleuren is heel normaal. Met het ouder worden ontstaan kleine scheurtjes in het glazuur, waardoor kleurstoffen makkelijker in de tand trekken. Roken en kleurrijke dranken en voeding, koffie, thee, rode wijn, frisdrank, versterken dat effect.</p>
<h2>Eerst een controle</h2>
<p>Bleken is niet altijd mogelijk of verstandig. Daarom kijkt de tandarts eerst naar uw gebit: zijn er gaatjes, is het tandvlees gezond en waar zitten vullingen of kronen? Vullingen, kronen en facings bleken namelijk niet mee. Daarna bespreken we welke aanpak bij u past, bijvoorbeeld thuis bleken met een bleekhoes op maat, of het bleken van één verkleurde tand.</p>
<div class="note"><p><b>Waarom via de tandarts?</b> Bleekmiddelen met een werkzame concentratie mogen in Nederland alleen door of onder toezicht van een tandarts worden gebruikt. Zo weet u zeker dat het veilig gebeurt en dat uw glazuur en tandvlees worden ontzien.</p></div>
<h2>Na het bleken</h2>
<ul>
  <li>Uw tanden kunnen een paar dagen gevoeliger zijn voor warm en koud. Dat trekt vanzelf weg.</li>
  <li>Vermijd de eerste dagen koffie, thee, rode wijn en roken: dan blijft het resultaat het mooist.</li>
  <li>Goed poetsen en regelmatig <a href="{u:behandelingen/preventie-en-mondhygiene/}">gebitsreiniging</a> helpen om verkleuring langer weg te houden.</li>
</ul>
""",
    faq=[
        ("Is bleken schadelijk voor mijn tanden?", "Bij een behandeling onder begeleiding van de tandarts niet. De tandarts controleert vooraf of uw gebit gezond is en kiest een veilige concentratie. Tijdelijke gevoeligheid kan voorkomen."),
        ("Hoe lang blijven mijn tanden wit?", "Dat verschilt per persoon. Wie weinig koffie, thee of wijn drinkt en niet rookt, houdt het resultaat het langst. Soms is na een tijd een korte opfrisbehandeling prettig."),
        ("Worden mijn vullingen en kronen ook witter?", "Nee, alleen natuurlijk tandweefsel bleekt. Zitten er vullingen of kronen in het zicht, dan bespreken we of die na het bleken vervangen moeten worden zodat de kleur weer aansluit."),
        ("Wordt bleken vergoed?", "Bleken is een cosmetische behandeling en wordt meestal niet vergoed door de zorgverzekeraar. U krijgt vooraf een begroting."),
    ],
    related=["esthetische-behandelingen", "preventie-en-mondhygiene", "kronen-en-bruggen"],
)

T["implantaten"] = dict(
    title="Tandimplantaten Meppel | Implantoloog & 3D CBCT-scan in huis",
    desc="Implantaat nodig in Meppel? Kroon, brug of klikgebit op implantaten door onze implantoloog, gepland met een eigen CBCT-scan. Gratis intake klikgebit.",
    h1='Tandimplantaten in <em class="g">Meppel</em>',
    lead="Een implantaat is een kunstwortel van titanium die in de kaak wordt geplaatst. Daarop komt een kroon, een brug of een klikgebit. Met een implantoloog, een CBCT-scanner en tandprothetici in de praktijk regelen we het hele traject onder één dak.",
    img="team/alvaro.webp", img_alt="Alvaro Soler, tandarts-implantoloog bij Tandartspraktijk Slotplantsoen",
    procedure="Tandimplantaat",
    who=["alvaro", "sanae"],
    body="""
<h2>Wanneer kiest u voor een implantaat?</h2>
<p>Implantologie is het vervangen van één of meer tanden met implantaten: kunstmatige titanium wortels die stevig in het kaakbot vastgroeien. Een implantaat voelt en werkt als een eigen tand, en de buurtanden hoeven niet te worden beslepen.</p>
<ul class="types">
  <li><b>Kroon op implantaat</b><span>Mist u één tand of kies? Op het implantaat komt een vastgeschroefde of vastgelijmde kroon.</span></li>
  <li><b>Brug op implantaten</b><span>Bij meerdere ontbrekende tanden. Een driedelige brug kan soms al op twee implantaten.</span></li>
  <li><b>Klikgebit</b><span>Zit uw kunstgebit los? Met drukknoppen of een staaf op implantaten klikt het vast. Meer houvast, meer gemak.</span></li>
</ul>
<h2>Nauwkeurig gepland met een 3D-scan</h2>
<p>Onze praktijk heeft een eigen <a href="{u:cbct-rontgen/}">Cone Beam CT-scanner</a>. Daarmee ziet de implantoloog in 3D hoeveel kaakbot er is en waar zenuwen en bijholtes liggen. Zo plannen we elk implantaat precies, zonder dat u daarvoor naar een ziekenhuis hoeft.</p>
<h2>Het traject stap voor stap</h2>
<ol>
  <li><b>Intake en onderzoek.</b> Gesprek over uw wensen, onderzoek van mond en kaak en zo nodig een CBCT-scan.</li>
  <li><b>Behandelplan en begroting.</b> U weet vooraf wat er gaat gebeuren en wat het kost.</li>
  <li><b>Plaatsen van het implantaat.</b> Onder plaatselijke verdoving; de meeste mensen vinden het meevallen.</li>
  <li><b>Ingroeien.</b> Het implantaat groeit in een aantal maanden vast in het bot. Zo nodig krijgt u in die tijd een tijdelijke voorziening.</li>
  <li><b>Kroon, brug of prothese.</b> Gemaakt door onze tandtechnieker of tandprothetici en precies op het implantaat afgestemd.</li>
</ol>
<div class="note" id="intake"><p><b>Gratis intake gebitsprothese of klikgebit.</b> Twijfelt u of een klikgebit iets voor u is? Plan een vrijblijvende intake. <a href="{u:afspraak-maken/}?soort=intake-prothese">Intake aanvragen</a></p></div>
<p>Een klikgebit wordt grotendeels vergoed uit de basisverzekering (met een eigen bijdrage en uw eigen risico). Een kroon of brug op implantaten valt voor volwassenen meestal niet onder de basisverzekering. Lees meer over <a href="{u:homepage/betalen-en-vergoedingen/}">vergoedingen</a>.</p>
""",
    faq=[
        ("Doet het plaatsen van een implantaat pijn?", "Het plaatsen gebeurt onder plaatselijke verdoving, dus u voelt tijdens de behandeling geen pijn. De dagen erna kan het wat gevoelig of gezwollen zijn; een gewone pijnstiller is dan meestal voldoende."),
        ("Ben ik geschikt voor een implantaat?", "Dat hangt onder meer af van de hoeveelheid kaakbot, uw algemene gezondheid en bijvoorbeeld roken. Met onze CBCT-scan kan de implantoloog dat nauwkeurig beoordelen."),
        ("Hoe lang gaat een implantaat mee?", "Bij een goede mondhygiëne en regelmatige controles gaat een implantaat vele jaren mee. Net als eigen tanden vraagt het om dagelijkse verzorging."),
        ("Wordt een klikgebit vergoed?", "Een klikgebit (implantaatgedragen prothese) wordt grotendeels vergoed uit de basisverzekering. U betaalt een wettelijke eigen bijdrage en eventueel uw eigen risico."),
    ],
    related=["protheses", "kronen-en-bruggen", "extractie-trekken"],
)

T["kronen-en-bruggen"] = dict(
    title="Kronen en bruggen Meppel | Eigen tandtechnisch lab",
    desc="Kroon of brug nodig? Tandartspraktijk Slotplantsoen in Meppel maakt kronen, bruggen, inlays en facings op maat in een eigen tandtechnisch laboratorium.",
    h1='Kronen en <em class="g">bruggen</em>',
    lead="Is een tand of kies zwaar beschadigd, of ontbreekt er een tand? Een kroon of brug herstelt vorm, functie en uiterlijk, op maat gemaakt in ons eigen tandtechnisch laboratorium.",
    img="team/ferdy.webp", img_alt="Ferdi Lippolt, tandtechnieker van Tandartspraktijk Slotplantsoen",
    procedure="Kroon- en brugwerk",
    who=["ferdy", "mauricio"],
    body="""
<h2>Kroon of brug: wat is het verschil?</h2>
<p>Kronen en bruggen vervangen tanden of kiezen die niet meer goed functioneren. Een <b>kroon</b> is een kapje over een afgeslepen tand of kies, dat er weer uitziet als een gave tand. Een <b>brug</b> vervangt één of meer ontbrekende tanden en wordt vastgezet op de tanden ernaast (de pijlers). Ontbreken die pijlers, dan kan een <a href="{u:behandelingen/implantaten/}">brug op implantaten</a> een oplossing zijn.</p>
<h2>Hoe verloopt de behandeling?</h2>
<p>Meestal heeft u drie afspraken nodig:</p>
<ol>
  <li><b>Voorbereiden.</b> De tand wordt onder verdoving afgeslepen en er wordt een afdruk gemaakt. U gaat naar huis met een tijdelijke kroon.</li>
  <li><b>Passen.</b> Ons tandtechnisch laboratorium maakt de kroon of brug; we passen en controleren kleur en beet.</li>
  <li><b>Plaatsen.</b> De kroon of brug wordt definitief vastgezet.</li>
</ol>
<p>Omdat ons laboratorium in de praktijk zit, overleggen tandarts en tandtechnieker direct met elkaar. Dat merkt u aan de pasvorm en de kleur.</p>
<h2>Welke materialen zijn er?</h2>
<ul class="types">
  <li><b>Keramiek</b><span>Tandkleurig en natuurgetrouw. De mooiste keuze voor zichtbare tanden.</span></li>
  <li><b>Goud-keramiek</b><span>Een sterke goudbasis met een tandkleurige laag erover.</span></li>
  <li><b>Goud</b><span>Zeer sterk en slijtvast; door de kleur vooral voor kiezen achter in de mond.</span></li>
  <li><b>Inlay of onlay</b><span>Een gedeeltelijke kroon als een groot deel van de kies nog gezond is. Van keramiek, goud of composiet.</span></li>
  <li><b>Facing</b><span>Dun schaaltje voor een mooiere voorkant van de tand; verkleurt niet door koffie of thee.</span></li>
  <li><b>Opbouw met stift</b><span>Extra steun voor de kroon als er weinig tand over is, verankerd in het wortelkanaal.</span></li>
</ul>
""",
    faq=[
        ("Hoe lang duurt het voordat mijn kroon klaar is?", "Meestal zijn er drie afspraken nodig: voorbereiden, passen en plaatsen. In de tussentijd heeft u een tijdelijke kroon, zodat u gewoon kunt eten en lachen."),
        ("Wat kost een kroon of brug?", "De tarieven zijn vastgesteld door de Nederlandse Zorgautoriteit (NZa); daarnaast zijn er techniekkosten voor het laboratorium. U krijgt vooraf een begroting, bij bedragen boven de € 250 ook schriftelijk."),
        ("Wordt een kroon vergoed?", "Voor volwassenen niet uit de basisverzekering, wel vaak deels uit een aanvullende tandartsverzekering. Ook voor kinderen tot 18 jaar vallen kronen en bruggen buiten de basisverzekering."),
    ],
    related=["implantaten", "esthetische-behandelingen", "wortelkanaalbehandeling"],
)

T["protheses"] = dict(
    title="Kunstgebit & klikgebit Meppel | Tandprotheticus Slotplantsoen",
    desc="Nieuw kunstgebit, klikgebit of frameprothese in Meppel? Onze tandprothetici maken het op maat; reparaties in eigen lab, vaak dezelfde dag. Gratis intake.",
    h1='Kunstgebit en <em class="g">klikgebit</em>',
    lead="Heeft u geen of bijna geen eigen tanden meer? Onze tandprothetici maken een prothese die goed past, er natuurlijk uitziet en waarmee u weer zorgeloos eet en lacht. Reparaties doen we in ons eigen laboratorium.",
    img="team/freek.webp", img_alt="Freek Zieck, tandprotheticus bij Tandartspraktijk Slotplantsoen",
    procedure="Gebitsprothese",
    who=["freek", "sanae"],
    body="""
<h2>Welke prothese past bij u?</h2>
<p>Wie geen, of bijna geen, eigen tanden meer heeft, komt in aanmerking voor een prothese. Er zijn volledige protheses (het kunstgebit) en gedeeltelijke of partiële protheses. Welke het beste past, bespreken we tijdens een gratis intake.</p>
<ul class="types">
  <li><b>Volledig kunstgebit</b><span>Een uitneembare prothese voor boven- en/of onderkaak, met aandacht voor een natuurlijke lach.</span></li>
  <li><b>Klikgebit</b><span>Het kunstgebit klikt vast op <a href="{u:behandelingen/implantaten/}">implantaten</a>. Veel steviger, vooral in de onderkaak.</span></li>
  <li><b>Frameprothese</b><span>Een dun, sterk metalen frame met haakjes om uw eigen tanden. Klein en comfortabel.</span></li>
  <li><b>Kunststof plaatje</b><span>Voordeliger en vaak tijdelijk, bijvoorbeeld als er nog tanden getrokken moeten worden.</span></li>
  <li><b>Immediaatprothese</b><span>Direct geplaatst na het trekken, zodat u nooit zonder tanden zit. Na genezing wordt hij opgevuld of vervangen.</span></li>
</ul>
<div class="note" id="intake"><p><b>Gratis intake gebitsprothese of klikgebit.</b> Kennismaken met de tandprotheticus, uw mond laten bekijken en horen wat er mogelijk is, vrijblijvend. <a href="{u:afspraak-maken/}?soort=intake-prothese">Intake aanvragen</a></p></div>
<h2>Reparatie in eigen laboratorium</h2>
<p>Is uw prothese gebroken of moet er iets aan gebeuren? Reparaties doen we in ons eigen laboratorium, meestal dezelfde dag:</p>
<ul>
  <li><b>Maandag t/m woensdag:</b> brengen vóór 09:30 uur, ophalen om 12:00 uur.</li>
  <li><b>Donderdag:</b> brengen vanaf 13:30 uur, ophalen om 16:00 uur.</li>
  <li><b>Vrijdag:</b> geen reparaties mogelijk.</li>
</ul>
<p>Bel bij voorkeur even van tevoren: <a href="tel:+31522247436">0522-247436</a>.</p>
""",
    faq=[
        ("Wat is het verschil tussen een kunstgebit en een klikgebit?", "Een gewoon kunstgebit blijft zitten door zuigkracht en de vorm van de kaak. Een klikgebit klikt vast op implantaten in de kaak en zit daardoor veel steviger, vooral in de onderkaak."),
        ("Mijn prothese zit los. Wat kan ik doen?", "Door slinking van het kaakbot kan een prothese na verloop van tijd los gaan zitten. Vaak helpt opvullen (rebasen). Is dat niet genoeg, dan kan een klikgebit uitkomst bieden. Kom gerust langs voor advies."),
        ("Wordt een kunstgebit vergoed?", "Volledige kunstgebitten en klikgebitten worden grotendeels vergoed uit de basisverzekering, met een wettelijke eigen bijdrage. Het eigen risico kan van toepassing zijn."),
        ("Hoe lang duurt het wennen aan een nieuwe prothese?", "Meestal een paar weken. Praten en eten gaat steeds makkelijker. Eventuele drukplekjes passen we bij tijdens de nacontrole."),
    ],
    related=["implantaten", "extractie-trekken", "kronen-en-bruggen"],
)

T["othodontie-en-invisalign"] = dict(
    title="Invisalign Meppel | Orthodontie met gratis intake",
    desc="Rechte tanden met Invisalign in Meppel: onzichtbare, uitneembare aligners via onze tandarts voor orthodontie. Vraag een gratis intake aan bij Slotplantsoen.",
    h1='Orthodontie en <em class="g">Invisalign</em>',
    lead="Rechte tanden zonder opvallende beugel. Met Invisalign verschuiven doorzichtige, uitneembare aligners uw tanden stap voor stap naar de juiste plek. Plan een gratis intake bij onze tandarts voor orthodontie.",
    img="team/anna.webp", img_alt="Anna Egea Hugué, tandarts voor orthodontie",
    procedure="Orthodontische behandeling met Invisalign",
    who=["anna", "marloes"],
    body="""
<h2>Wat is Invisalign?</h2>
<p>Invisalign is een onzichtbare beugel: een reeks doorzichtige, uitneembare aligners die speciaal voor uw gebit worden gemaakt. Elke week wisselt u naar een nieuwe set, die uw tanden en kiezen een klein stukje verder in de juiste stand brengt.</p>
<ul class="types">
  <li><b>Onopvallend</b><span>De aligners zijn transparant. De meeste mensen zien niet dat u een beugel draagt.</span></li>
  <li><b>Comfortabel</b><span>Geen metalen brackets of draden, dus minder kans op irritatie in de mond.</span></li>
  <li><b>Flexibel</b><span>Uitnemen bij eten, drinken, poetsen en flossen, of even voor een belangrijke afspraak.</span></li>
</ul>
<figure><img src="{a:assets/img/invisalign.webp}" alt="Doorzichtige Invisalign-aligner wordt op de tanden geplaatst" width="900" height="588" loading="lazy" decoding="async"><figcaption>De aligners worden op maat gemaakt en zijn nauwelijks zichtbaar.</figcaption></figure>
<h2>Hoe verloopt een behandeling?</h2>
<ol>
  <li><b>Gratis intake.</b> Onze tandarts voor orthodontie bekijkt uw gebit en bespreekt uw wensen en de mogelijkheden.</li>
  <li><b>Behandelplan.</b> Op basis van onderzoek en afdrukken of een scan ziet u vooraf hoe uw tanden stap voor stap verschuiven.</li>
  <li><b>Aligners dragen.</b> U draagt de aligners het grootste deel van de dag en komt tussendoor op controle.</li>
  <li><b>Resultaat vasthouden.</b> Na afloop zorgt een retainer ervoor dat uw tanden mooi recht blijven.</li>
</ol>
<div class="note"><p><b>Gratis intake orthodontie.</b> Benieuwd of Invisalign bij u past? <a href="{u:afspraak-maken/}?soort=intake-orthodontie">Vraag een vrijblijvende intake aan</a>.</p></div>
""",
    faq=[
        ("Hoeveel uur per dag moet ik de aligners dragen?", "Voor het beste resultaat draagt u de aligners zo’n 20 tot 22 uur per dag. U neemt ze alleen uit om te eten, te drinken (behalve water) en te poetsen."),
        ("Hoe lang duurt een behandeling met Invisalign?", "Dat hangt af van uw situatie. Kleine correcties zijn soms binnen enkele maanden klaar; bij grotere verschuivingen duurt het langer. Tijdens de intake krijgt u een inschatting."),
        ("Doet Invisalign pijn?", "Bij een nieuwe set aligners kunt u een dag of twee wat druk voelen. Dat is een teken dat de tanden verschuiven en trekt snel weg."),
        ("Wordt een beugel vergoed?", "Beugels vallen ook voor kinderen tot 18 jaar buiten de basisverzekering. Sommige aanvullende verzekeringen vergoeden een deel, soms pas na een wachttijd."),
    ],
    related=["esthetische-behandelingen", "preventie-en-mondhygiene", "bleken"],
)

T["vullingen"] = dict(
    title="Witte vullingen (composiet) | Tandarts Meppel",
    desc="Gaatje laten vullen in Meppel? Wij werken met tandkleurig composiet dat direct hard is. U kiest zelf of u verdoving wilt. Tandartspraktijk Slotplantsoen.",
    h1='Witte <em class="g">vullingen</em>',
    lead="Een gaatje laten vullen hoeft niet spannend te zijn. We werken met tandkleurig composiet dat direct hard wordt en nauwelijks opvalt, en u bepaalt zelf of u verdoving wilt.",
    img="ontspannen.webp", img_alt="Tevreden patiënte in de tandartsstoel",
    procedure="Tandvulling",
    who=["kinan", "mauricio"],
    body="""
<h2>Hoe gaat het vullen van een gaatje?</h2>
<ol>
  <li><b>Verdoving, als u dat wilt.</b> U kiest zelf of de tand of kies verdoofd wordt.</li>
  <li><b>Schoonmaken.</b> Het aangetaste deel wordt weggeboord. Tijdens het boren komt water vrij dat de kies koelt en het slijpsel afvoert; de assistente zuigt het direct weg.</li>
  <li><b>Opbouwen.</b> Met een vormpje om de kies brengt de tandarts het composiet in laagjes aan.</li>
  <li><b>Uitharden en polijsten.</b> Een blauwe (koude) lamp hardt elke laag direct uit. Daarna wordt de vulling op uw beet afgestemd en gepolijst.</li>
</ol>
<h2>Composiet in plaats van amalgaam</h2>
<p>Vroeger werden vrijwel alleen amalgaamvullingen gebruikt. Tegenwoordig vullen we met wit composiet: het hecht aan de tand, er hoeft minder gezond tandweefsel weg en de vulling is nauwelijks te zien. Sinds 2025 wordt amalgaam in de Europese Unie in principe niet meer toegepast.</p>
<h2>Na de behandeling</h2>
<p>Na een witte vulling kan de tand een tijdje gevoelig zijn voor koud en warm, soms zelfs wat pijnlijk. Meestal gaat dat vanzelf over. Houdt de pijn aan of twijfelt u? Wacht dan niet te lang en <a href="tel:+31522247436">bel ons</a>.</p>
""",
    faq=[
        ("Doet een vulling pijn?", "Met verdoving voelt u tijdens het boren niets. Ook zonder verdoving is een kleine vulling voor veel mensen goed te doen. U bepaalt het zelf."),
        ("Moet ik mijn oude amalgaamvullingen laten vervangen?", "Niet als ze nog goed zijn. Is een amalgaamvulling lek of beschadigd, of stoort u zich aan de kleur, dan kan hij worden vervangen door composiet."),
        ("Is gevoeligheid na een vulling normaal?", "Ja, een paar dagen tot weken gevoeligheid voor koud en warm komt voor. Wordt het erger of blijft het kloppen, neem dan contact met ons op."),
    ],
    related=["wortelkanaalbehandeling", "preventie-en-mondhygiene", "esthetische-behandelingen"],
)

T["extractie-trekken"] = dict(
    title="Tand of kies trekken in Meppel | Extractie en nazorg",
    desc="Moet er een tand of kies getrokken worden? Lees hoe een extractie bij Tandartspraktijk Slotplantsoen in Meppel verloopt en wat u na afloop wel en niet mag.",
    h1='Een tand of kies <em class="g">trekken</em>',
    lead="Soms is een tand of kies niet meer te redden. Een extractie gebeurt onder goede verdoving en met rustige uitleg. Hier leest u hoe het gaat en wat u na afloop het beste kunt doen.",
    img="hero-kinan.webp", img_alt="Tandarts Kinan Khalil in de behandelkamer",
    procedure="Tandextractie",
    who=["kinan", "alvaro"],
    body="""
<h2>Voor de behandeling</h2>
<ul>
  <li>Eet gewoon goed voordat u komt.</li>
  <li>Vertel de tandarts of u <b>bloedverdunners</b> gebruikt, een <b>kunstmatige hartklep</b> heeft of in de afgelopen zes maanden een <b>vaatoperatie</b> heeft gehad.</li>
</ul>
<h2>De behandeling</h2>
<p>De tand of kies wordt eerst verdoofd; de verdoving heeft even tijd nodig om in te werken. Daarna wordt de tand losgemaakt en eruit gehaald. Dat doet geen pijn, al kan het drukken of geluid voor sommigen onprettig zijn. Soms wordt de wond gehecht, meestal met hechtdraad die vanzelf oplost.</p>
<h2>Nazorg: wat mag wel en niet?</h2>
<ul>
  <li>Bijt <b>30 minuten</b> stevig op het steriele gaasje.</li>
  <li>U mag eten en drinken, maar <b>spoel de eerste dag niet</b>: het bloedstolsel in de wond moet blijven zitten.</li>
  <li>Pas op met hete dranken en bijten op uw wang zolang de verdoving werkt.</li>
  <li>Geen zwaar lichamelijk werk, geen alcohol en <b>niet roken</b> op de dag van de behandeling.</li>
  <li>Koel uw wang, neem geen warm bad of hete douche en ga niet plat liggen.</li>
  <li>Tegen pijn kunt u paracetamol of ibuprofen nemen. Ga nooit boven de maximale dosering.</li>
</ul>
<div class="note"><p><b>Neem contact op</b> als de wond na twee uur nog bloedt, als u koorts krijgt van 39 °C of hoger, of als de pijn na een paar dagen erger wordt of u een vieze smaak in de mond krijgt. Dat kan wijzen op een wondontsteking. Bel <a href="tel:+31522247436">0522-247436</a>; buiten openingstijden kunt u terecht bij de <a href="{u:homepage/spoedgevallen-en-weekenddienst/}">dienstdoende tandarts</a>.</p></div>
<h2>En daarna?</h2>
<p>Ontstaat er een zichtbare opening, dan zijn er goede oplossingen: een <a href="{u:behandelingen/implantaten/}">implantaat</a>, een <a href="{u:behandelingen/kronen-en-bruggen/}">brug</a> of een <a href="{u:behandelingen/protheses/}">prothese</a>. We bespreken het graag met u.</p>
""",
    faq=[
        ("Doet het trekken van een kies pijn?", "Nee, de tand of kies wordt goed verdoofd. U voelt wel druk. Na afloop kan het een paar dagen gevoelig zijn; een gewone pijnstiller helpt meestal goed."),
        ("Mag ik na het trekken eten?", "Ja, maar kauw bij voorkeur aan de andere kant en wacht met hete dranken tot de verdoving is uitgewerkt. Spoel de eerste dag niet."),
        ("Wanneer moet ik bellen?", "Als de wond na twee uur nog bloedt, bij koorts vanaf 39 °C, of als de pijn na een paar dagen toeneemt of u een vieze smaak krijgt."),
    ],
    related=["implantaten", "protheses", "wortelkanaalbehandeling"],
)

T["wortelkanaalbehandeling"] = dict(
    title="Wortelkanaalbehandeling Meppel | Eigen tand behouden",
    desc="Ontstoken zenuw of kiespijn? Met een wortelkanaalbehandeling bij Tandartspraktijk Slotplantsoen in Meppel behoudt u vaak uw eigen tand. Lees hoe het werkt.",
    h1='Wortelkanaalbehandeling: uw eigen tand <em class="g">behouden</em>',
    lead="Een ontstoken of afgestorven zenuw kan flink pijn doen. Met een wortelkanaalbehandeling nemen we de oorzaak weg, zodat u uw eigen tand of kies vaak kunt behouden.",
    img="team/mauricio.webp", img_alt="Tandarts Mauricio Rosenfeld Bochicchio",
    procedure="Wortelkanaalbehandeling",
    who=["mauricio", "kinan"],
    body="""
<h2>Wat is een wortelkanaalbehandeling?</h2>
<p>In elke tand en kies lopen zenuwen en bloedvaten, via het wortelkanaal naar de zenuwkamer. Bij een wortelkanaalbehandeling worden de zenuwkamer en de wortelkanalen gereinigd, ontsmet en daarna opgevuld met een speciaal materiaal.</p>
<h2>Waarom is het nodig?</h2>
<p>Een ernstig ontstoken of afgestorven zenuw kan veel pijn geven en het kaakbot rond de wortel aantasten. Daardoor kan de tand los gaan zitten en uiteindelijk verloren gaan. De behandeling neemt de oorzaak van de ontsteking weg: de pijn verdwijnt en de tand blijft behouden.</p>
<p>Een zenuw raakt ontstoken of sterft af door langdurige of plotselinge irritatie, bijvoorbeeld door:</p>
<ul>
  <li>een diep gaatje (cariës);</li>
  <li>een harde klap of val;</li>
  <li>een barst of breuk in de tand;</li>
  <li>ernstige slijtage of erosie.</li>
</ul>
<h2>Doet het pijn?</h2>
<p>De tand of kies is meestal goed te verdoven, zodat de behandeling zelf niet pijnlijk is. Is een zenuw moeilijk te verdoven, dan kan de tandarts extra verdoven, waardoor het toch vrijwel altijd pijnloos verloopt. De eerste dagen erna kan de tand wat gevoelig tot pijnlijk zijn.</p>
<h2>Na de behandeling</h2>
<p>Een tand zonder zenuw wordt brozer. Vaak adviseren we daarom een <a href="{u:behandelingen/kronen-en-bruggen/}">kroon</a> om de tand te beschermen. Bij twijfel over de ligging van wortelkanalen of een ontsteking kan een <a href="{u:cbct-rontgen/}">3D CBCT-scan</a> extra duidelijkheid geven.</p>
""",
    faq=[
        ("Doet een wortelkanaalbehandeling pijn?", "Tijdens de behandeling bent u verdoofd. Daarna kan de tand een paar dagen gevoelig zijn. De hevige pijn van een ontstoken zenuw is na de behandeling meestal juist weg."),
        ("Hoeveel afspraken zijn er nodig?", "Dat hangt af van de tand en de ontsteking. Vaak zijn één of twee afspraken voldoende."),
        ("Wat gebeurt er als ik niets doe?", "De ontsteking kan zich uitbreiden naar het kaakbot. Dat kan leiden tot een abces, botverlies en uiteindelijk het verlies van de tand."),
    ],
    related=["vullingen", "kronen-en-bruggen", "extractie-trekken"],
)

T["preventie-en-mondhygiene"] = dict(
    title="Mondhygiëne en preventie Meppel | Gebitsreiniging",
    desc="Bloedend tandvlees, tandsteen of slechte adem? Onze preventieassistenten in Meppel reinigen uw gebit grondig en geven persoonlijk advies. Maak een afspraak.",
    h1='Preventie en <em class="g">mondhygiëne</em>',
    lead="Voorkomen is beter dan boren. Onze (paro-)preventieassistenten helpen u om tandvleesproblemen, gaatjes en slechte adem voor te zijn, met een grondige reiniging en advies dat bij u past.",
    img="preventie.webp", img_alt="Preventieassistente behandelt een patiënte in de stoel",
    procedure="Gebitsreiniging en mondhygiëne",
    who=["ina", "naima", "elisa"],
    body="""
<h2>Waarom preventie?</h2>
<p>Dagelijks poetsen en de halfjaarlijkse controle zijn belangrijk, maar niet altijd genoeg om uw gebit een leven lang gezond te houden. Tandsteen en bacteriën op plekken die u zelf moeilijk bereikt, veroorzaken tandvleesontsteking (gingivitis) en uiteindelijk parodontitis, waarbij het kaakbot wordt afgebroken.</p>
<h2>Wanneer naar de preventieassistente?</h2>
<ul>
  <li>uw tandvlees bloedt bij poetsen of eten;</li>
  <li>uw tandvlees is rood, gezwollen of slap, of trekt zich terug;</li>
  <li>tanden of kiezen staan los;</li>
  <li>u krijgt regelmatig gaatjes;</li>
  <li>u heeft veel tandsteen of aanslag;</li>
  <li>u heeft een vieze smaak in de mond of een slechte adem.</li>
</ul>
<h2>Slechte adem</h2>
<p>Bij een slechte adem (halitose) ligt de oorzaak in ongeveer 80% van de gevallen in de mond: bacteriën tussen de tanden, in tandvleespockets of op de achterkant van de tong. Maskeren met snoepjes of mondspray helpt niet. Laat uw gebit controleren en reinig dagelijks tussen uw tanden met tandenstokers, floss of ragers.</p>
<h2>Terugtrekkend tandvlees</h2>
<p>Te hard poetsen of een harde tandenborstel kan het tandvlees beschadigen; kies een zachte borstel en weinig druk. Ook ontsteking laat het tandvlees terugtrekken. Na een parodontologische behandeling trekt het tandvlees soms iets terug, dat is juist gezond, omdat de pocket kleiner wordt. Stel zo’n behandeling dus niet uit.</p>
<h2>Hoe ziet gezond tandvlees eruit?</h2>
<ul class="types">
  <li><b>Roze en stevig</b><span>Het tandvlees zit strak om de tanden en bloedt niet bij poetsen.</span></li>
  <li><b>Ondiepe pockets</b><span>De ruimte tussen tand en tandvlees is minder dan 4 mm diep.</span></li>
  <li><b>Sinaasappelhuid</b><span>Kleine putjes in het tandvlees zijn een gezond teken.</span></li>
</ul>
""",
    faq=[
        ("Hoe vaak moet ik naar de preventieassistente?", "Dat verschilt per persoon. Bij een gezond gebit is één of twee keer per jaar vaak genoeg; bij tandvleesproblemen adviseren we soms een vaker schema."),
        ("Is bloedend tandvlees normaal?", "Nee. Bloedend tandvlees is meestal een teken van ontsteking. Met een goede reiniging en de juiste poetstechniek is dat vaak snel verholpen."),
        ("Wordt een gebitsreiniging vergoed?", "Voor kinderen tot 18 jaar valt het onder de basisverzekering. Voor volwassenen vergoedt een aanvullende tandartsverzekering het vaak (deels)."),
    ],
    related=["vullingen", "bleken", "esthetische-behandelingen"],
)
