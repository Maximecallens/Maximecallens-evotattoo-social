"""Génère les visuels LinkedIn EvoTattoo (1200x1200 PNG) à partir de gabarits HTML.

Usage : python3 build_cards.py  -> écrit out/*.png
Charte : bleu #0A63A8, bleu foncé #034C86, texte #1B2129, Montserrat (titres) + Inter (texte).
"""
import base64
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
FONTS = ROOT / "node_modules/@fontsource"


def font_face(family, path, weight):
    data = base64.b64encode((FONTS / path).read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")


FACES = "".join([
    font_face("Montserrat", "montserrat/files/montserrat-latin-700-normal.woff2", 700),
    font_face("Montserrat", "montserrat/files/montserrat-latin-800-normal.woff2", 800),
    font_face("Inter", "inter/files/inter-latin-400-normal.woff2", 400),
    font_face("Inter", "inter/files/inter-latin-500-normal.woff2", 500),
    font_face("Inter", "inter/files/inter-latin-600-normal.woff2", 600),
])
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo.png").read_bytes()).decode()

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--blue:#0A63A8;--navy:#034C86;--ink:#1B2129;--muted:#5B6673;--soft:#EEF4FA;--line:#D6E2EE}
body{width:1200px;height:1200px;font-family:Inter,sans-serif;color:var(--ink);background:#fff;
 display:flex;flex-direction:column;overflow:hidden}
header{display:flex;justify-content:space-between;align-items:center;padding:56px 72px 0}
header img{height:150px}
.pill{font:600 22px Inter;color:var(--navy);background:var(--soft);border:2px solid var(--line);
 padding:14px 26px;border-radius:999px;letter-spacing:.2px}
main{flex:1;padding:36px 72px 48px;display:flex;flex-direction:column;justify-content:center;min-height:0}
h1{font:800 76px/1.06 Montserrat,sans-serif;letter-spacing:-1.5px}
h1 em{font-style:normal;color:var(--blue)}
.sub{font:500 30px/1.35 Inter;color:var(--muted);margin-top:22px}
footer{flex:none;background:var(--navy);color:#fff;display:flex;justify-content:space-between;align-items:center;
 padding:34px 72px;font:600 26px Inter}
footer b{font:800 32px Montserrat;letter-spacing:.3px}
.badge{display:inline-block;font:700 22px Montserrat;color:#fff;background:var(--blue);
 padding:10px 20px;border-radius:10px;letter-spacing:.5px;text-transform:uppercase}
"""


def page(body, extra_css=""):
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{FACES}{BASE_CSS}{extra_css}"
            f"</style></head><body>{body}</body></html>")


HEADER = f'<header><img src="{LOGO}" alt=""><span class="pill">Certification RS6681 · Qualiopi</span></header>'
FOOTER = '<footer><b>evotattoo.fr</b><span>École de tatouage certifiée · Piolenc (84)</span></footer>'


def sessions_card():
    css = """
    .row{display:flex;gap:32px;margin-top:40px}
    .col{flex:1;border:2px solid var(--line);border-radius:22px;padding:34px 34px 30px;background:#fff}
    .col h2{font:800 40px Montserrat;color:var(--navy)}
    .meta{font:500 23px/1.35 Inter;color:var(--muted);margin:8px 0 22px}
    .s{display:flex;align-items:center;gap:16px;font:600 28px Inter;padding:15px 0;border-top:2px solid var(--soft)}
    .s i{width:14px;height:14px;border-radius:50%;background:var(--blue);flex:none}
    .top{display:flex;gap:16px;align-items:center;margin-bottom:26px}
    .done{font:700 22px Montserrat;color:var(--muted);border:2px solid var(--line);padding:8px 18px;border-radius:10px;text-transform:uppercase;letter-spacing:.5px}
    """
    body = f"""{HEADER}<main>
    <div class="top"><span class="badge">Inscriptions ouvertes</span><span class="done">2026 : complet</span></div>
    <h1>Sessions <em>2027</em><br>MasterClass &amp; BootCamp</h1>
    <div class="row">
      <div class="col"><h2>MasterClass</h2><div class="meta">80 h à distance · 4 semaines<br>Examen final à Piolenc</div>
        <div class="s"><i></i>18 janv. → 12 févr.</div>
        <div class="s"><i></i>1er mars → 26 mars</div>
        <div class="s"><i></i>12 avr. → 7 mai</div></div>
      <div class="col"><h2>BootCamp</h2><div class="meta">42 h en présentiel · 6 jours<br>À Piolenc, examen le vendredi</div>
        <div class="s"><i></i>15 → 20 févr.</div>
        <div class="s"><i></i>29 mars → 3 avr.</div>
        <div class="s"><i></i>10 → 15 mai</div></div>
    </div></main>{FOOTER}"""
    return page(body, css)


def financement_card():
    css = """
    h1{font-size:68px}
    .sub{font-size:27px;margin-top:16px}
    .tiles{display:flex;flex-direction:column;gap:16px;margin-top:30px}
    .t{display:flex;align-items:center;gap:30px;background:var(--soft);border-radius:22px;padding:22px 32px}
    .n{font:800 30px Montserrat;color:#fff;background:var(--blue);width:64px;height:64px;border-radius:16px;
       display:flex;align-items:center;justify-content:center;flex:none}
    .t h3{font:800 34px Montserrat;color:var(--navy)}
    .t p{font:500 25px/1.35 Inter;color:var(--muted);margin-top:4px}
    .prices{display:flex;gap:16px;margin-top:24px;font:600 26px Inter;color:var(--ink)}
    .prices span{border:2px solid var(--line);border-radius:12px;padding:12px 20px}
    """
    body = f"""{HEADER}<main>
    <h1>Financez votre formation <em>certifiante</em></h1>
    <p class="sub">Session en janvier ou février ? Comptez 3 semaines à 2 mois pour obtenir un accord.</p>
    <div class="tiles">
      <div class="t"><div class="n">1</div><div><h3>CPF, sous conditions</h3><p>Jusqu'à 1 500 € de droits pour une certification RS<br>Participation forfaitaire de 150 € (sauf exonération)</p></div></div>
      <div class="t"><div class="n">2</div><div><h3>France Travail</h3><p>Demandeurs d'emploi : aides via votre conseiller</p></div></div>
      <div class="t"><div class="n">3</div><div><h3>4 fois sans frais</h3><p>Paiement échelonné via PayPal</p></div></div>
    </div>
    <div class="prices"><span>MasterClass · 1 900 €</span><span>BootCamp · 2 000 €</span></div>
    </main>{FOOTER}"""
    return page(body, css)


def parcours_card():
    css = """
    .list{display:flex;flex-direction:column;gap:22px;margin-top:40px}
    .p{display:grid;grid-template-columns:200px 1fr;align-items:center;gap:30px;border:2px solid var(--line);
       border-radius:22px;padding:28px 34px}
    .h{font:800 54px Montserrat;color:var(--blue);line-height:1}
    .h small{display:block;font:600 21px Inter;color:var(--muted);margin-top:8px;letter-spacing:0}
    .p h3{font:800 36px Montserrat;color:var(--navy)}
    .p p{font:500 25px/1.35 Inter;color:var(--ink);margin-top:6px}
    .note{font:500 23px Inter;color:var(--muted);margin-top:26px}
    """
    body = f"""{HEADER}<main>
    <h1>Quel parcours <em>pour vous ?</em></h1>
    <div class="list">
      <div class="p"><div class="h">185 h<small>8 semaines</small></div><div><h3>Tatoueur Artistique</h3><p>Vous partez de zéro et visez le métier complet</p></div></div>
      <div class="p"><div class="h">80 h<small>4 semaines</small></div><div><h3>MasterClass</h3><p>Vous débutez et voulez vous certifier</p></div></div>
      <div class="p"><div class="h">42 h<small>6 jours</small></div><div><h3>BootCamp</h3><p>Vous tatouez déjà et visez la certification</p></div></div>
    </div>
    <p class="note">MasterClass et BootCamp mènent à la certification RS6681.</p>
    </main>{FOOTER}"""
    return page(body, css)


LIST_CSS = """
.items{display:flex;flex-direction:column;gap:18px;margin-top:36px}
.it{display:flex;align-items:center;gap:28px;background:var(--soft);border-radius:22px;padding:24px 32px}
.ic{font:800 28px Montserrat;color:#fff;background:var(--blue);min-width:64px;height:64px;border-radius:16px;
    display:flex;align-items:center;justify-content:center;flex:none;padding:0 14px}
.it h3{font:800 32px Montserrat;color:var(--navy)}
.it p{font:500 24px/1.35 Inter;color:var(--muted);margin-top:4px}
.note{font:500 23px Inter;color:var(--muted);margin-top:24px}
"""


def items(rows):
    return '<div class="items">' + "".join(
        f'<div class="it"><div class="ic">{ic}</div><div><h3>{h}</h3><p>{p}</p></div></div>'
        for ic, h, p in rows) + "</div>"


def certification_card():
    body = f"""{HEADER}<main>
    <span class="badge" style="align-self:flex-start;margin-bottom:24px">Reconnue par l'État</span>
    <h1>Certification <em>RS6681</em></h1>
    <p class="sub">« Création et réalisation de tatouages artistiques complexes » · France Compétences, 27/06/2024</p>
    {items([("6 h", "Épreuve pratique", "Tatouage sur peau synthétique, de 10h à 17h"),
            ("1 j", "En présentiel à Piolenc", "Une journée d'examen dans notre centre (84)"),
            ("72 h", "Jury de tatoueurs professionnels", "Résultats communiqués sous 72 heures")])}
    <p class="note">Préparée par la MasterClass et le BootCamp · même examen, même jury.</p>
    </main>{FOOTER}"""
    return page(body, LIST_CSS)


def prerequis_card():
    body = f"""{HEADER}<main>
    <h1>Candidater : <em>la check-list</em></h1>
    <p class="sub">MasterClass &amp; BootCamp, sessions 2027</p>
    {items([("1", "Hygiène &amp; salubrité", "Formation obligatoire de 21 h"),
            ("2", "Votre book", "Vos dessins · et vos tatouages pour le BootCamp"),
            ("3", "Justificatif d'activité", "Kbis, URSSAF ou SIRET · déclaration en cours acceptée en MasterClass")])}
    <p class="note">Évaluation gratuite de votre niveau via le formulaire de contact.</p>
    </main>{FOOTER}"""
    return page(body, LIST_CSS)


def formateur_card():
    css = LIST_CSS + """
    .big{display:flex;gap:28px;margin-top:36px}
    .k{flex:1;border:2px solid var(--line);border-radius:22px;padding:30px 30px 26px}
    .k b{display:block;font:800 64px Montserrat;color:var(--blue);line-height:1}
    .k span{display:block;font:600 24px/1.3 Inter;color:var(--ink);margin-top:12px}
    """
    body = f"""{HEADER}<main>
    <h1>Formé par <em>Med</em>,<br>tatoueur depuis 1998</h1>
    <p class="sub">Fondateur d'EvoTattoo · MedTattoo, Piolenc</p>
    <div class="big">
      <div class="k"><b>28 ans</b><span>de pratique du tatouage</span></div>
      <div class="k"><b>20+</b><span>styles maîtrisés</span></div>
      <div class="k"><b>300+</b><span>élèves formés</span></div>
    </div>
    {items([("5j/7", "Suivi individuel", "Tchat, classes virtuelles et corrections vidéo de vos TP"),
            ("6 mois", "Suivi après la formation", "Pour continuer à progresser")])}
    </main>{FOOTER}"""
    return page(body, css)


def avis_card():
    css = """
    .stars{font:800 120px Montserrat;color:var(--blue);line-height:1;margin-top:28px}
    .stars small{font:700 34px Montserrat;color:var(--muted);margin-left:14px}
    .q{margin-top:30px;border-left:8px solid var(--blue);padding:8px 0 8px 32px}
    .q p{font:500 34px/1.4 Inter;color:var(--ink)}
    .q span{display:block;font:600 24px Inter;color:var(--muted);margin-top:12px}
    .kpis{display:flex;gap:16px;margin-top:34px;font:600 25px Inter}
    .kpis span{border:2px solid var(--line);border-radius:12px;padding:12px 20px}
    """
    body = f"""{HEADER}<main>
    <h1>Ce que disent <em>nos élèves</em></h1>
    <div class="stars">5/5<small>Google · 76 avis</small></div>
    <div class="q"><p>« Totalement débutant au départ de la formation, j'ai aujourd'hui l'impression d'avoir un vrai bagage pour démarrer dans le tatouage. »</p><span>Maxime, élève MasterClass</span></div>
    <div class="kpis"><span>+300 élèves formés</span><span>9,5/10 satisfaction</span><span>Qualiopi depuis 2020</span></div>
    </main>{FOOTER}"""
    return page(body, css)


def depart_card():
    css = """
    .hero{display:flex;align-items:center;gap:36px;margin-top:34px;background:var(--navy);color:#fff;border-radius:26px;padding:36px 40px}
    .hero b{font:800 120px Montserrat;line-height:.9}
    .hero span{font:700 34px/1.25 Montserrat}
    .hero small{display:block;font:500 24px Inter;opacity:.85;margin-top:8px}
    .steps{display:flex;flex-direction:column;gap:14px;margin-top:30px}
    .st{display:flex;gap:20px;align-items:center;font:600 28px Inter}
    .st i{font-style:normal;font:800 24px Montserrat;color:#fff;background:var(--blue);width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;flex:none}
    """
    body = f"""{HEADER}<main>
    <h1>MasterClass 2027&nbsp;:<br><em>c'est maintenant</em></h1>
    <div class="hero"><b>18</b><span>janvier 2027<small>Départ de la session 1 · examen le 19 février à Piolenc</small></span></div>
    <div class="steps">
      <div class="st"><i>1</i>Montez le financement : 3 semaines à 2 mois de délai</div>
      <div class="st"><i>2</i>Réunissez hygiène 21 h, book et justificatif</div>
      <div class="st"><i>3</i>Candidatez via le formulaire de contact</div>
    </div>
    </main>{FOOTER}"""
    return page(body, css)


# (dossier de sortie, nom de fichier) -> gabarit
CARDS = {
    ("2026-10", "evotattoo-sessions-2027"): sessions_card,
    ("2026-10", "evotattoo-financement"): financement_card,
    ("2026-10", "evotattoo-3-parcours"): parcours_card,
    ("2026-10", "evotattoo-certification-rs6681"): certification_card,
    ("2026-11", "evotattoo-prerequis"): prerequis_card,
    ("2026-11", "evotattoo-formateur-med"): formateur_card,
    ("2026-11", "evotattoo-avis-eleves"): avis_card,
    ("2026-11", "evotattoo-masterclass-janvier"): depart_card,
}

SOCIAL = ROOT.parent.parent / "social"

if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])  # noms de dossiers à (re)générer, ex. 2026-11 ; vide = tout
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=1)
        for (folder, name), fn in CARDS.items():
            if only and folder not in only:
                continue
            dest = SOCIAL / folder
            dest.mkdir(parents=True, exist_ok=True)
            pg.set_content(fn())
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(dest / f"{name}.png"), full_page=False)
            print("ok", folder, name)
        browser.close()
