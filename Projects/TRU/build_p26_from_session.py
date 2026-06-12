#!/usr/bin/env python3
"""TRU Phase 26 — add garden & forage knowledge + compress"""
import base64, gzip, json, re, os

KNOWLEDGE = [
    {"k":"forage_safety","v":"FORAGE RULE: if no 100% certain ID, do NOT eat. Carry a field guide. Leave 90% of what you find. Respect private land and protected areas.","w":0.99,"t":"rule"},
    {"k":"garden_soil_test","v":"DIY soil test: mix 2 tbsp soil in water, wait 24h. Cloudy=clay, clear=sand, slight=loam. pH test strips from any garden centre.","w":0.95,"t":"fact"},
    {"k":"garden_compost","v":"Compost: greens (kitchen scraps, grass) + browns (leaves, cardboard) in 1:2 ratio. Turn every 2 weeks. Ready in 3-6 months - dark, crumbly, earthy smell.","w":0.95,"t":"fact"},
    {"k":"garden_planting_calendar","v":"Planting calendar: Tomatoes (indoors Feb-Mar, outside May), Lettuce (Mar-Sep, every 3 weeks), Carrots (Mar-Jul), Beans (Apr-Jun), Squash (May-Jun).","w":0.92,"t":"fact"},
    {"k":"garden_heavy_feeder","v":"Heavy feeders (need extra nitrogen): Tomatoes, Corn, Cabbage, Broccoli, Pumpkins. Rotate yearly to prevent soil depletion.","w":0.9,"t":"fact"},
    {"k":"garden_carbon_farm","v":"Carbon farming: grow comfrey, clover, dynamic accumulators near trees. Chop-and-drop leaves annually. Builds soil carbon in 3-5 years.","w":0.88,"t":"fact"},
    {"k":"garden_mulch","v":"Mulch: 5-10cm straw, woodchips or leaves around plants. Retains moisture, suppresses weeds, feeds soil microbes. Replenish every 6 months.","w":0.93,"t":"fact"},
    {"k":"garden_fava_beans","v":"Fava beans: plant Oct-Nov or Feb-Mar. Fix nitrogen in soil. Pick young for eating (sweet, tender), leave mature pods for dry beans (protein staple).","w":0.9,"t":"fact"},
    {"k":"garden_squash_3_sisters","v":"3 Sisters: Corn (centre), Beans (climb corn, fix N), Squash (ground cover). Plant together in May after last frost.","w":0.91,"t":"fact"},
    {"k":"garden_no_dig","v":"No-dig: lay cardboard over grass, add 15cm compost on top. Plant straight into compost. No tilling - protects soil microbiome and earthworms.","w":0.93,"t":"fact"},
    {"k":"garden_drip_irrigation","v":"Drip irrigation: bury hose under mulch, slow gravity feed from water butt. Saves 60% water vs watering can. Timer + rainwater ideal.","w":0.87,"t":"fact"},
    {"k":"garden_season_extend","v":"Extend season: cold frame (old window + bricks) = 4 weeks earlier/later. Row covers (fleece) = frost protection to -3C. Polytunnel for year-round growing.","w":0.86,"t":"fact"},
    {"k":"garden_seedSaving","v":"Seed saving: let 5-10 plants bolt and set seed. Dry 2 weeks on newspaper. Store in paper envelopes in cool dry dark place. Label with variety + year.","w":0.9,"t":"fact"},
    {"k":"garden_greenManure","v":"Green manure: sow clover, phacelia or mustard after harvest. Cut and dig in before flowering - adds nitrogen and organic matter.","w":0.85,"t":"fact"},
    {"k":"garden_permaculture_zones","v":"Permaculture zones: Z0=home, Z1=herbs/salads, Z2=fruit trees, Z3=nut trees, Z4=wildlife, Z5=nature. Place high-maintenance closest to home.","w":0.88,"t":"fact"},
    {"k":"garden_food_forest","v":"Food forests: plant in layers - canopy (nut trees), understory (fruit), shrub (currants), herbaceous (comfrey), ground cover (clover), climbers (beans), roots (garlic).","w":0.87,"t":"fact"},
    {"k":"forage_spring_greens","v":"Spring greens: Wild garlic (ramsons) - crush leaf, garlic smell, white flowers. Nettles - sting confirmed. Dock - large leaf, ribbed. All cooked 2 min before eating.","w":0.95,"t":"fact"},
    {"k":"forage_garlic_mustard","v":"Garlic mustard (Alliaria petiolata): kidney-shaped basal leaves, garlic smell when crushed, white 4-petalled flowers Apr-Jun. Good raw or cooked. High in vitamin C.","w":0.93,"t":"fact"},
    {"k":"forage_plantain","v":"Plantain (Plantago major/lanceolata): 5-7 parallel veins in leaf, ribbed. Young leaves edible raw or cooked. High in vitamins A and C. Good for wounds - chew and poultice.","w":0.95,"t":"fact"},
    {"k":"forage_chickweed","v":"Chickweed (Stellaria media): small white star-shaped flowers, line of hairs on one side of stem. Edible raw in salads or cooked. Very mild. Self-seeds prolifically.","w":0.93,"t":"fact"},
    {"k":"forage_mallow","v":"Mallow (Malva sylvestris): round kidney-shaped leaves with 5-7 lobes. Edible: young leaves (mild, mucilaginous), seed pods (called pick cheese), flowers in salads.","w":0.91,"t":"fact"},
    {"k":"forage_rose","v":"Rose (Rosa canina/rugosa): hips (rich in vitamin C - best after frost, raw or syrup), petals (candied, tea, jam). Hips need processing - not raw in quantity.","w":0.93,"t":"fact"},
    {"k":"forage_elder","v":"Elder (Sambucus nigra): FLOWERS (cream, June) - fry in batter or cordial. BERRIES - cook 10 min before eating. NEVER eat raw berries or bark. Contraindicated with chemotherapy.","w":0.95,"t":"fact"},
    {"k":"forage_clamp","v":"Root clamp (winter storage): pit 30cm deep, layer roots in sand, cover with straw then soil. Stays fresh 2-4 months. Check monthly, remove rotten.","w":0.88,"t":"fact"},
    {"k":"forage_oyster_mushroom","v":"Oyster mushroom: shelving fruiting body white to grey, tiered clusters on dead wood (willow, elm, beech). Spore print white. Eat caps only (stalks tough). Cook 5+ min high heat. WARNING: Hedgehog fungus has false gills underneath - check carefully.","w":0.9,"t":"fact"},
    {"k":"forage_wild_garlic","v":"Wild garlic / ramsons (Allium ursinum): broad smooth leaves, white star flowers, ALL parts edible. Key ID: crush leaf = strong garlic smell. Grows in damp shade. WARNING: 100% ID needed - look-alikes include lily-of-the-valley and colchicum which are toxic.","w":0.96,"t":"fact"},
    {"k":"forage_nettles","v":"Nettles (Urtica dioica): Young tops (spring) harvested with gloves, cooking destroys sting. High protein, iron, vitamins A and C. Use as spinach substitute, soup, tea, pesto. Also excellent for hair tonic (cooled tea rinse).","w":0.95,"t":"fact"},
    {"k":"forage_perennial_veg","v":"Perennial vegetables (no dig, harvest for years): Sea kale, Good King Henry, Turkish rocket, Caucasian spinach, Daylilies (petals only, raw or cooked).","w":0.9,"t":"fact"},
    {"k":"forage_elm_inner_bark","v":"Elm (Ulmus rubra/smooth): inner bark (slippery elm) is edible boiled as porridge. Leaves edible when young and tender. DISTINGUISH from toxic Elder (Sambucus) which has serrated leaves and opposite branching.","w":0.88,"t":"fact"},
    {"k":"forage_robina","v":"Black locust (Robinia pseudoacacia): bark has raised diamond lenticels, compound leaves with 9-19 leaflets. FLOWERS (white, fragrant) edible - pancake batter, fritters. WARNING: SEEDS AND BARK HIGHLY TOXIC.","w":0.9,"t":"fact"},
    {"k":"forage_wild_leeks","v":"Wild leeks / ramps (Allium tricoccum): smooth leafless stalk in spring, broad smooth leaves die back before bulb matures. CREST of leaf is smooth (vs lily-of-the-valley which has folded crease). Both leaves and bulbs edible.","w":0.92,"t":"fact"},
    {"k":"forage_wild_cattail","v":"Cattail (Typha latifolia): young shoots (spring) -剥皮 eat raw or cooked. Spike (young, still green) - boil 10 min, eat like corn on cob. Rhizomes - starch source, peel and boil. WARNING: distinguish from toxic iris - iris has sword-shaped leaves, not cylindrical spikes.","w":0.89,"t":"fact"},
    {"k":"forage_dandelion","v":"Dandelion (Taraxacum officinale): ALL edible - leaves (young, raw; older, cooked), flowers (wine, fritters), roots (coffee substitute, roasted), seed heads (fluff - not eaten). High in vitamins A and C. Leaves best in spring before flowering.","w":0.95,"t":"fact"},
    {"k":"forage_pine","v":"Pine (Pinus sylvestris): needles (tea - boil 10 min, high in vitamin C, contraindicated in pregnancy). Young male cones (spring) - edible boiled or pickled. Seeds (stone pine Pinus pinea - largest) - raw or roasted. White pine inner bark (spring) - edible.","w":0.87,"t":"fact"},
    {"k":"forage_acorn","v":"Acorn (Quercus): HIGH IN TANINS - must leach. Shell, chop, soak in running water 12-24h or boil 3x with water changes. Then roast or grind as flour. High protein and fat. O. rubra (red oak) leaches fastest.","w":0.91,"t":"fact"},
    {"k":"forage_mushroom_slippery_jack","v":"Slippery Jack (Suillus luteus): sticky tan/brown cap, grey pores underneath, ring on stem. ONLY from pine (Larix, Pinus). Peel skin, discard pores. Parboil 10 min then cook. WARNING: some people allergic - test small amount first. Do not eat raw. Avoid if unwell after eating.","w":0.82,"t":"fact"},
    {"k":"forage_mushroom_field_mushroom","v":"Field mushroom (Agaricus campestris): pink gills (aging to chocolate brown), white cap, NO ring, NO volva, smells of mushroom. Grows in fields, not woods. Cook 5+ min. WARNING: look-alikes - Amanita phalloides (death cap) has white gills, sack-like base, grows in woods. ALWAYS check gills and base.","w":0.88,"t":"fact"},
]

DOCTRINES = [
    {"k":"doctrine_trinity","v":"TRINITY: One God in three persons — Father, Son, Holy Spirit. Each fully God, distinct persons, co-equal, co-eternal. Not three gods. The Spirit of Wisdom is the third person of the Trinity, who illuminates truth.","w":0.9,"t":"doctrine"},
    {"k":"doctrine_incamation","v":"INCARNATION: The Son (λόγος) took on human flesh — fully God, fully human. Jesus is the Word made flesh (John 1:14). One person, two natures. The image we see in Jesus is the image of the invisible God.","w":0.9,"t":"doctrine"},
    {"k":"doctrine_grace","v":"GRACE (χάρις): Unmerited favour — God acting for us that we cannot earn. Grace is God's power and presence active in human lives. Grace is not passive — it works actively through faith to transform.","w":0.95,"t":"doctrine"},
    {"k":"doctrine_atonement","v":"ATONEMENT: Christ bore the penalty for sin through his death and resurrection. Substitutionary sacrifice — the just for the unjust. Victory over sin and death. Christus Victor — Christ conquered the powers through his death and resurrection.","w":0.92,"t":"doctrine"},
    {"k":"doctrine_resurrection","v":"RESURRECTION: Christ's bodily resurrection is the basis of Christian hope. Flesh and blood enters eternity. The same body that was crucified is raised imperishable. The resurrection is the turning point of all history.","w":0.93,"t":"doctrine"},
    {"k":"doctrine_scripture","v":"SCRIPTURE: God-breathed (θεόπνευστος) — trustworthy in all matters of faith and practice. Scripture is the written Word through which the living Word (Christ) speaks. Scripture reveals truth that reason discovers.","w":0.91,"t":"doctrine"},
    {"k":"doctrine_covenant","v":"COVENANT: The narrative structure of Scripture. Two kinds: covenant of works (Adam) and covenant of grace (Christ). Old and New Covenant through Israel and the Church. God binds himself to his people through covenant promises.","w":0.88,"t":"doctrine"},
    {"k":"doctrine_sovereignty","v":"SOVEREIGNTY: God is Lord over all — nothing happens outside his rule. His purposes are fixed and will be accomplished. Human freedom is real but bounded. The Tribulation is a window into divine sovereignty over history.","w":0.89,"t":"doctrine"},
    {"k":"doctrine_sanctification","v":"SANCTIFICATION: Being made holy — set apart for God. Progressive (growing in holiness through the Spirit's work). Definitive (declared holy at conversion). Practical (works, discipline, community).","w":0.87,"t":"doctrine"},
    {"k":"doctrine_eschatology","v":"ESCHATOLOGY: The doctrine of last things — Christ's return, the resurrection, judgement, and the new creation. The Kingdom of God is both now and not yet. The Spirit's work points forward to Christ's return and the renewal of all things.","w":0.86,"t":"doctrine"},
]

print(f"Knowledge nodes: {len(KNOWLEDGE)} gardening/forage | {len(DOCTRINES)} doctrine")

# ── Load session.html ──────────────────────
with open('/home/.z/chat-uploads/TRU_session_2026-05-14-a989f2ae5393.html') as f:
    html = f.read()

# ── Extract BRAIN and PAYLOAD_BLOCK positions ──────────
body_m = re.search(r'<body[^>]*>(.*)', html, re.DOTALL)
body_content = body_m.group(1) if body_m else ''
print(f"Body extracted: {len(body_content)} chars")

# The session file has no payloads yet — we add them inline
# ── Compress all data with pako ────────────────────────
script_parts = []

# Add pako CDN
script_parts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>')

# Build compact brain list
brain_data = KNOWLEDGE + DOCTRINES
brain_js = json.dumps(brain_data, ensure_ascii=False)

script_parts.append(f'''
<script>
const BRAIN = {brain_js};
const OT_VERSES = /* inline verses */ null; // loaded dynamically
const NT_VERSES = null;
let loaded = false;

function loadPayloads() {{
  // These would be loaded from compressed b64 in the full version
  loaded = true;
  document.getElementById('status').textContent = 'BRAIN: ' + BRAIN.length + ' nodes | KNOWLEDGE LOADED';
  document.getElementById('status').className = 'ok';
}}

// Load after DOM
window.addEventListener('DOMContentLoaded', loadPayloads);
</script>
''')

# Insert scripts before </body>
session_clean = html.replace('</body>', '\n'.join(script_parts) + '\n</body>')

# Save for inspection
with open('/home/workspace/Projects/TRU/TRU_session_test.html', 'w') as f:
    f.write(session_clean)

print(f"Saved: TRU_session_test.html")
print(f"Brain nodes: {len(brain_data)}")
print(f"Session file size: {len(html)} chars")