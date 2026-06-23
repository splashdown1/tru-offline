#!/usr/bin/env python3
"""Append existential/doctrinal concept nodes to canonical brain.json."""
import json, os

BRAIN = "/home/workspace/Projects/TRU/current/brain.json"

nodes = [
 ("suffering","suffering entered the world through the fall. god permits it to refine faith, reveal glory, and produce endurance. christ suffered as our substitute, and our present sufferings are not worth comparing with the coming glory. (gen 3; rom 5:12; rom 8:18; 1 pet 4:12-13)"),
 ("evil","evil is rebellion against god's good order — moral evil (sin) and natural evil (corruption and death). it is not a substance but good twisted, a privation. god permits evil temporarily but defeated it at the cross and will end it at judgment. (gen 3; isa 5:20; rom 12:21; rev 21:4)"),
 ("purpose","human purpose is to glorify god and enjoy him forever — to image the creator in knowledge, righteousness, and holiness, exercising dominion over creation in love. (gen 1:26-28; eccl 12:13; 1 cor 10:31; rev 4:11)"),
 ("hope","hope is the confident expectation of god's promised future — not wishful thinking but an anchor for the soul, rooted in christ's resurrection and guaranteed by the spirit. (rom 8:24-25; heb 6:19; 1 pet 1:3)"),
 ("faith","faith is trusting god's word and character — the assurance of things hoped for, the conviction of things not seen. it is a gift that receives christ and produces obedience. (heb 11:1; eph 2:8-9; gal 2:20)"),
 ("doubt","doubt is wavering between faith and unbelief. honest doubt seeks truth and can lead to stronger faith, but unbelief refuses god's word. christ meets the doubting with grace: 'lord, i believe; help my unbelief.' (mark 9:24; james 1:6-8; john 20:27)"),
 ("judgment","judgment is god's righteous evaluation of all people through christ. the wicked face eternal separation; the righteous are justified in christ. judgment is according to truth and deeds, yet salvation is by grace through faith. (heb 9:27; rom 2:6; john 5:24; rev 20:12)"),
 ("salvation","salvation is god rescuing sinners from his wrath into eternal life — accomplished by christ's death and resurrection, applied by grace through faith, and consummated at his return. it is wholly god's work, not earned. (eph 2:8-9; rom 10:9; titus 3:5)"),
 ("forgiveness","forgiveness is god releasing the debt of sin for christ's sake, and our releasing those who wrong us. it is rooted in the cross, full and free, and calls us to forgive as we have been forgiven. (eph 1:7; col 1:14; matt 6:14-15)"),
 ("fear","fear of god is awe that produces wisdom and obedience, versus terror of judgment. 'the fear of the lord is the beginning of wisdom.' perfect love casts out slavish fear, for christ has borne our condemnation. (prov 9:10; 1 john 4:18; 2 tim 1:7)"),
 ("hell","hell is the final, just separation of the impenitent from god's grace — conscious, eternal punishment prepared for the devil and his angels. it is god's righteous 'no' to those who reject him. (matt 25:46; 2 thess 1:9; rev 20:14-15)"),
 ("heaven","heaven is the eternal dwelling of god's people with him — the new creation where every tear is wiped away, sin and death are no more, and god is all in all. (rev 21:1-4; john 14:2-3; 1 cor 15:28)"),
 ("trinity","the trinity is the one god eternally existing as three persons — father, son, and holy spirit — equal in essence, distinct in person, united in purpose. mystery revealed in scripture, not three gods. (matt 28:19; 2 cor 13:14; deut 6:4)"),
 ("grace","grace is god's unmerited favour — salvation given freely, not earned. it appears in christ, trains us to renounce ungodliness, and empowers holy living. where sin abounded, grace abounded more. (eph 2:8-9; titus 2:11; rom 5:20)"),
 ("sin","sin is any failure to conform to god's law in act, attitude, or nature — lawlessness rooted in unbelief. it entered through adam, infects all, and earns death; christ, the sinless one, bore it to free us. (1 john 3:4; rom 5:12; rom 6:23)"),
 ("death","death is the wages of sin — spiritual separation from god, physical decay, and apart from christ, eternal death. christ defeated death by his resurrection; in him, death becomes sleep and the gate to life. (rom 6:23; 1 cor 15:26; john 11:25-26)"),
 ("love","love is willing the good of the other for god's sake — god's essence and our calling. god so loved that he gave his son; we love because he first loved us, loving god and neighbour as self. (1 john 4:8; john 3:16; mark 12:30-31)"),
]

b = json.load(open(BRAIN, encoding="utf-8"))
existing = {n["k"] for n in b["nodes"]}
added = 0
for k, v in nodes:
    if k in existing:
        print(f"  skip dup: {k}")
        continue
    b["nodes"].append({"k": k, "v": v, "w": 1.0, "t": "doctrine", "source": "TRU_CANONICAL"})
    added += 1
b["exported"] = "2026-06-23_existential"

with open(BRAIN, "w", encoding="utf-8") as f:
    json.dump(b, f, ensure_ascii=False)

print(f"added {added} nodes. total now: {len(b['nodes'])}")
