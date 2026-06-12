#!/usr/bin/env python3
"""TRU Phase 26 — build from session.html"""
import base64, gzip, json, re, os

# ── KJV Bible (English NT lookup) ──────────────────────
kjv = json.load(open('/tmp/kjv.json', encoding='utf-8-sig'))
kjv_nt = {}
for book in kjv:
    for ci, ch in enumerate(book['chapters']):
        for vi, v in enumerate(ch):
            ref = f"{book['abbrev'].lower()} {ci+1}:{vi+1}"
            kjv_nt[ref] = v
print(f"KJV NT: {len(kjv_nt)} verses")

# ── OT from coil_ot.txt (gzip-b64) ────────────────────
with open('/home/workspace/Projects/TRU/data/coil_ot.txt') as f:
    ot_text = gzip.decompress(base64.b64decode(f.read().strip())).decode('utf-8', errors='replace')
OT = [l for l in ot_text.split('\n') if '||' in l]
print(f"OT: {len(OT)} verses")

# ── NT from sblgnt txt files ──────────────────────────
nt_lines = []
for fp in sorted(os.popen('find /tmp/package -name "*.txt"').read().strip().split('\n')):
    if not fp.endswith('.txt') or 'APP' in fp: continue
    with open(fp, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.replace('\r', '').rstrip()
            if not line.strip(): continue
            m = re.match(r'^(\w+)\s+(\d+:\d+)\t(.+)$', line)
            if not m: continue
            ab = m.group(1).lower().replace('jude', 'jd')
            greek = m.group(3).strip()
            ref = f"{ab} {m.group(2)}"
            english = kjv_nt.get(ref, greek)
            nt_lines.append(f"{ref}||{english}||{greek}")
NT = nt_lines
print(f"NT: {len(NT)} verses")

# ── Knowledge: garden + forage + survival ──────────────
KNOWLEDGE = [
    {"k":"forage_safety","v":"FORAGE RULE: if no 100% certain ID, do NOT eat. Carry a field guide. Leave 90% of what you find. Respect private land and protected areas.","w":0.99,"t":"rule"},
    {"k":"garden_soil_test","v":"DIY soil test: mix 2 tbsp soil in water, wait 24h. Cloudy=clay, clear=sand, slight=loam. pH test strips from any garden centre.","w":0.95,"t":"fact"},
    {"k":"garden_compost","v":"Compost: greens (kitchen scraps, grass) + browns (leaves, cardboard) in 1:2 ratio. Turn every 2 weeks. Ready in 3-6 months - dark, crumbly, earthy smell.","w":0.95,"t":"fact"},
    {"k":"garden_planting_calendar","v":"Planting: Tomatoes (indoors Feb-Mar, outside May), Lettuce (Mar-Sep, every 3 weeks), Carrots (Mar-Jul), Beans (Apr-Jun), Squash (May-Jun).","w":0.92,"t":"fact"},
    {"k":"garden_heavy_feeder","v":"Heavy feeders (need extra nitrogen): Tomatoes, Corn, Cabbage, Broccoli, Pumpkins. Rotate yearly to prevent soil depletion.","w":0.9,"t":"fact"},
    {"k":"garden_mulch","v":"Mulch: 5-10cm straw, woodchips or leaves around plants. Retains moisture, suppresses weeds, feeds soil microbes. Replenish every 6 months.","w":0.93,"t":"fact"},
    {"k":"garden_fava_beans","v":"Fava beans: plant Oct-Nov or Feb-Mar. Fix nitrogen in soil. Pick young (sweet, tender) or leave mature pods for dry beans (protein staple).","w":0.9,"t":"fact"},
    {"k":"garden_3_sisters","v":"3 Sisters: Corn (centre), Beans (climb corn, fix N), Squash (ground cover). Plant together in May after last frost.","w":0.91,"t":"fact"},
    {"k":"garden_no_dig","v":"No-dig: lay cardboard over grass, add 15cm compost on top. Plant straight into compost. No tilling - protects soil microbiome and earthworms.","w":0.93,"t":"fact"},
    {"k":"garden_drip_irrigation","v":"Drip irrigation: bury hose under mulch, slow gravity feed from water butt. Saves 60% water vs watering can. Timer + rainwater ideal.","w":0.87,"t":"fact"},
    {"k":"garden_seed_saving","v":"Seed saving: let 5-10 plants bolt and set seed. Dry 2 weeks on newspaper. Store in paper envelopes in cool dry dark place. Label with variety + year.","w":0.9,"t":"fact"},
    {"k":"garden_season_extend","v":"Extend season: cold frame = 4 weeks earlier/later. Row covers (fleece) = frost protection to -3C. Polytunnel for year-round growing.","w":0.86,"t":"fact"},
    {"k":"garden_carbon_farming","v":"Carbon farming: grow comfrey, clover, dynamic accumulators near trees. Chop-and-drop leaves annually. Builds soil carbon in 3-5 years.","w":0.88,"t":"fact"},
    {"k":"garden_food_forest","v":"Food forests: canopy (nut trees), understory (fruit), shrub (currants), herbaceous (comfrey), ground cover (clover), climbers (beans), roots (garlic).","w":0.87,"t":"fact"},
    {"k":"garden_permaculture_zones","v":"Permaculture zones: Z0=home, Z1=herbs/salads, Z2=fruit trees, Z3=nut trees, Z4=wildlife, Z5=nature. Place high-maintenance closest to home.","w":0.88,"t":"fact"},
    {"k":"garden_green_manure","v":"Green manure: sow clover, phacelia or mustard after harvest. Cut and dig in before flowering - adds nitrogen and organic matter.","w":0.85,"t":"fact"},
    {"k":"forage_spring_greens","v":"Spring greens: Wild garlic (ramsons) - crush leaf, garlic smell, white flowers. Nettles - sting confirmed. Dock - large ribbed leaf. All cooked 2 min before eating.","w":0.95,"t":"fact"},
    {"k":"forage_garlic_mustard","v":"Garlic mustard (Alliaria petiolata): kidney-shaped basal leaves, garlic smell when crushed, white 4-petalled flowers Apr-Jun. Good raw or cooked. High in vitamin C.","w":0.93,"t":"fact"},
    {"k":"forage_plantain","v":"Plantain (Plantago major/lanceolata): 5-7 parallel veins in leaf, ribbed. Young leaves edible raw or cooked. High in vitamins A and C. Good for wounds - chew and poultice.","w":0.95,"t":"fact"},
    {"k":"forage_chickweed","v":"Chickweed (Stellaria media): small white star-shaped flowers, line of hairs on one side of stem. Edible raw or cooked. Very mild flavour. Self-seeds prolifically.","w":0.93,"t":"fact"},
    {"k":"forage_mallow","v":"Mallow (Malva sylvestris): round kidney-shaped leaves with 5-7 lobes. Edible: young leaves (mild, mucilaginous), seed pods (pick cheese), flowers in salads.","w":0.91,"t":"fact"},
    {"k":"forage_rose","v":"Rose (Rosa canina/rugosa): hips (rich in vitamin C - best after frost, raw or syrup), petals (candied, tea, jam). Hips need processing - not raw in quantity.","w":0.93,"t":"fact"},
    {"k":"forage_elder","v":"Elder (Sambucus nigra): FLOWERS (cream, June) - fry in batter or cordial. BERRIES - cook 10 min before eating. NEVER eat raw berries or bark. Contraindicated with chemotherapy.","w":0.95,"t":"fact"},
    {"k":"forage_clamp","v":"Root clamp (winter storage): pit 30cm deep, layer roots in sand, cover with straw then soil. Stays fresh 2-4 months. Check monthly, remove rotten.","w":0.88,"t":"fact"},
    {"k":"forage_wild_garlic","v":"Wild garlic / ramsons (Allium ursinum): broad smooth leaves, white star flowers, ALL parts edible. Key ID: crush leaf = strong garlic smell. Grows in damp shade. WARNING: 100% ID needed - lily-of-the-valley and colchicum are toxic.","w":0.96,"t":"fact"},
    {"k":"forage_nettles","v":"Nettles (Urtica dioica): Young tops (spring) with gloves, cooking destroys sting. High protein, iron, vitamins A and C. Use as spinach, soup, tea, pesto.","w":0.95,"t":"fact"},
    {"k":"forage_dandelion","v":"Dandelion (Taraxacum officinale): ALL edible - leaves (young raw, older cooked), flowers (wine, fritters), roots (coffee substitute, roasted), seed heads (fluff - not eaten). High in vitamins A and C. Leaves best in spring before flowering.","w":0.95,"t":"fact"},
    {"k":"forage_cattail","v":"Cattail (Typha latifolia): young shoots (spring) - peel and eat raw or cooked. Young spike (green) - boil 10 min, eat like corn on cob. Rhizomes - starch source, peel and boil. WARNING: distinguish from toxic iris - iris has sword-shaped leaves, not cylindrical spikes.","w":0.89,"t":"fact"},
    {"k":"forage_acorn","v":"Acorn (Quercus): HIGH IN TANINS - must leach. Shell, chop, soak in running water 12-24h or boil 3x with water changes. Then roast or grind as flour. High protein and fat. Red oak (Q. rubra) leaches fastest.","w":0.91,"t":"fact"},
    {"k":"forage_oyster_mushroom","v":"Oyster mushroom: shelving fruiting body white to grey, tiered clusters on dead wood (willow, elm, beech). Spore print white. Eat caps only (stalks tough). Cook 5+ min high heat. WARNING: Hedgehog fungus has false gills underneath.","w":0.9,"t":"fact"},
    {"k":"forage_field_mushroom","v":"Field mushroom (Agaricus campestris): pink gills (aging to chocolate), white cap, NO ring, NO volva, smells mushroom. Grows in fields, not woods. Cook 5+ min. WARNING: Death cap (Amanita phalloides) has white gills, sack-like base, grows in woods. ALWAYS check gills and base.","w":0.88,"t":"fact"},
    {"k":"forage_elm_inner_bark","v":"Elm (Ulmus rubra): inner bark (slippery elm) edible boiled as porridge. Leaves edible when young and tender. DISTINGUISH from toxic Elder (Sambucus) which has serrated leaves and opposite branching.","w":0.88,"t":"fact"},
    {"k":"forage_robina","v":"Black locust (Robinia pseudoacacia): bark has raised diamond lenticels, compound leaves with 9-19 leaflets. FLOWERS (white, fragrant) edible - pancake batter, fritters. WARNING: SEEDS AND BARK HIGHLY TOXIC.","w":0.9,"t":"fact"},
    {"k":"forage_pine","v":"Pine (Pinus): needles (tea - boil 10 min, high in vitamin C, contraindicated in pregnancy). Young male cones (spring) - edible boiled or pickled. Seeds (stone pine) - raw or roasted. White pine inner bark (spring) - edible.","w":0.87,"t":"fact"},
    {"k":"forage_perennial_veg","v":"Perennial vegetables (harvest for years, no dig): Sea kale, Good King Henry, Turkish rocket, Caucasian spinach, Daylilies (petals only, raw or cooked).","w":0.9,"t":"fact"},
    {"k":"forage_wild_leeks","v":"Wild leeks / ramps (Allium tricoccum): smooth leafless stalk in spring, broad smooth leaves die back before bulb matures. CREST of leaf is smooth (vs lily-of-the-valley which has folded crease). Both leaves and bulbs edible.","w":0.92,"t":"fact"},
    {"k":"forage_mushroom_slippery_jack","v":"Slippery Jack (Suillus luteus): sticky tan/brown cap, grey pores underneath, ring on stem. ONLY from pine/larch. Peel skin, discard pores. Parboil 10 min then cook. WARNING: some people allergic - test small amount first. Do not eat raw.","w":0.82,"t":"fact"},
]

# ── 10 Core Doctrines ──────────────────────────────────
DOCTRINES = [
    {"k":"doctrine_trinity","v":"TRINITY: One God in three persons - Father, Son, Holy Spirit. Each fully God, distinct persons, co-equal, co-eternal. Not three gods. The Spirit of Wisdom is the third person of the Trinity.","w":0.9,"t":"doctrine"},
    {"k":"doctrine_incamation","v":"INCARNATION: The Son took on human flesh - fully God, fully human. Jesus is the Word made flesh (John 1:14). One person, two natures. The image in Jesus is the image of the invisible God.","w":0.9,"t":"doctrine"},
    {"k":"doctrine_grace","v":"GRACE: Unmerited favour - God acting for us that we cannot earn. Grace is not passive - it works through faith to transform human lives.","w":0.95,"t":"doctrine"},
    {"k":"doctrine_atonement","v":"ATONEMENT: Christ bore the penalty for sin through his death and resurrection. Substitutionary sacrifice - the just for the unjust. Christus Victor - Christ conquered the powers.","w":0.92,"t":"doctrine"},
    {"k":"doctrine_resurrection","v":"RESURRECTION: Christ bodily resurrection is the basis of Christian hope. Flesh and blood enters eternity. The same body that was crucified is raised imperishable. The turning point of all history.","w":0.93,"t":"doctrine"},
    {"k":"doctrine_scripture","v":"SCRIPTURE: God-breathed (theopneustos) - trustworthy in all matters of faith and practice. Scripture is the written Word through which the living Word (Christ) speaks.","w":0.91,"t":"doctrine"},
    {"k":"doctrine_covenant","v":"COVENANT: The narrative structure of Scripture. Two kinds: covenant of works (Adam) and covenant of grace (Christ). Old and New Covenant through Israel and the Church.","w":0.88,"t":"doctrine"},
    {"k":"doctrine_sovereignty","v":"SOVEREIGNTY: God is Lord over all - nothing happens outside his rule. His purposes are fixed. Human freedom is real but bounded.","w":0.89,"t":"doctrine"},
    {"k":"doctrine_sanctification","v":"SANCTIFICATION: Being made holy - set apart for God. Progressive (growing in holiness through the Spirit). Definitive (declared holy at conversion). Practical (works, discipline, community).","w":0.87,"t":"doctrine"},
    {"k":"doctrine_eschatology","v":"ESCHATOLOGY: The doctrine of last things - Christ return, the resurrection, judgement, and the new creation. The Kingdom of God is both now and not yet.","w":0.86,"t":"doctrine"},
]

BRAIN = KNOWLEDGE + DOCTRINES
print(f"BRAIN: {len(BRAIN)} nodes")

# ── Compress ────────────────────────────────────────────
def b64gzip(data_str):
    return base64.b64encode(gzip.compress(data_str.encode())).decode()

OT_STR = '\n'.join(OT)
NT_STR = '\n'.join(NT)
BRAIN_STR = json.dumps(BRAIN, ensure_ascii=False)
OT_B64 = b64gzip(OT_STR)
NT_B64 = b64gzip(NT_STR)
BRA_GZ = b64gzip(BRAIN_STR)
print(f"Payloads: brain={len(BRA_GZ)} ot={len(OT_B64)} nt={len(NT_B64)}")

# ── Read session.html ───────────────────────────────────
with open('/home/.z/chat-uploads/TRU_session_2026-05-14-a989f2ae5393.html') as f:
    html = f.read()
print(f"Session HTML: {len(html)} chars")

# ── Build injection script ────────────────────────────────
RED_WORDS = 'Lord,God,Christ,Jesus,grace,faith,love,spirit,truth,life,light,righteous,holiness,sanct,mercy,peace,joy,hope,love,salvation,redeem,glory,kingdom,eternal,blessed,bless,prayer,intercession,shepherd,law,covenant,prophet,priest,sacrifice,resurrection,king'.split(',')

INJECT = f'''
<script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
<script>
const RED = {json.dumps(RED_WORDS)};
const B64 = {json.dumps({'brain': BRA_GZ, 'ot': OT_B64, 'nt': NT_B64})};
let BRAIN=[],OT=[],NT=[];

async function init() {{
  try {{
    BRAIN = JSON.parse(pako.ungzip(base64.decode(B64.brain), {{to:'string'}}));
    OT = (await pako.ungzip(base64.decode(B64.ot), {{to:'string'}})).split('\\n').filter(l=>l&&l.includes('||'));
    NT = (await pako.ungzip(base64.decode(B64.nt), {{to:'string'}})).split('\\n').filter(l=>l&&l.includes('||'));
    const s = document.getElementById('status');
    if(s) {{ s.textContent = 'READY: '+BRAIN.length+' nodes | '+OT.length+' OT | '+NT.length+' NT'; s.className='ok'; }}
    showPanel();
  }} catch(e) {{ console.error(e); }}
}}

function showPanel() {{
  const c = document.getElementById('kp');
  if(!c) return;
  c.innerHTML = BRAIN.map(n=>'<div class="ki" onclick="q(\''+n.k+'\')"><span class="kt">['+n.t+']</span><span>'+(n.v.length>90?n.v.slice(0,90)+'...':n.v)+'</span></div>').join('');
}}

function q(k) {{
  const n = BRAIN.find(n=>n.k===k);
  if(!n) return;
  const i = document.getElementById('qinp');
  if(i) i.value = n.v;
  handleAsk(n.v);
}}

window.addEventListener('DOMContentLoaded', init);
</script>
<style>
#kp{{display:flex;flex-direction:column;gap:4px;max-height:260px;overflow-y:auto;padding:4px 0}}
.ki{{padding:5px 8px;background:var(--card);border:1px solid var(--border);border-radius:6px;cursor:pointer;font-size:.78rem;display:flex;gap:6px}}
.ki:hover{{border-color:var(--accent)}}
.kt{{font-weight:bold;color:var(--accent);min-width:68px}}
</style>
'''

# ── Inject knowledge panel after tribunal ──────────────
html = html.replace('<div id="tribunal"', '<div id="kp" style="padding:8px 0;border-bottom:1px solid var(--border)"></div>\n<div id="tribunal"')

# ── Inject before </body> ─────────────────────────────
html = html.replace('</body>', INJECT + '\n</body>')

# ── Fix status text ────────────────────────────────────
html = html.replace(
    'document.getElementById(\'status\').textContent = \'TRU loaded\';',
    'document.getElementById(\'status\').textContent = \'LOADING...\';'
)

out = '/home/workspace/Projects/TRU/TRU_session_enriched.html'
with open(out, 'w') as f:
    f.write(html)
size = os.path.getsize(out)
print(f"Saved: {out} ({size//1024}KB)")
print(f"Data overhead: {len(BRA_GZ)+len(OT_B64)+len(NT_B64)} chars of b64 (gzipped payload)")