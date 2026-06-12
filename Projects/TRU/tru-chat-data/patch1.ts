import type { Context } from "hono";
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const BRAIN_PATH = "/home/workspace/Projects/TRU/current/brain.json";
const KJV_PATH = "/home/workspace/Projects/TRU/data/kjv_full.json";
const SEC_DIR = "/home/workspace/primaries/sec";
const TEMPLE_FILE = "/home/workspace/primaries/temple/temple_posts.json";
const ARXIV_DIR = "/home/workspace/primaries/arxiv";
const EVENTS_PATH = "/home/workspace/primaries/current_events/current_events.json";

const STOP = new Set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split(" "));
const TRUTH_WORDS = ["fact","facts","true","truth","real","actual","verify","verified","prove","evidence","source","sources","primary","primaries","corroborate","corroboration"];

const BOOK_LONG: Record<string, string> = {
  gen:"genesis",gn:"genesis",genesis:"genesis",
  ex:"exodus",exo:"exodus",exodus:"exodus",
  lv:"leviticus",lev:"leviticus",le:"leviticus",leviticus:"leviticus",
  nu:"numbers",num:"numbers",nb:"numbers",numbers:"numbers",
  dt:"deuteronomy",deut:"deuteronomy",deu:"deuteronomy",deuteronomy:"deuteronomy",
  josh:"joshua",joshua:"joshua",
  jdg:"judges",judg:"judges",judges:"judges",
  ru:"ruth",rut:"ruth",ruth:"ruth",
  "1sa":"1 samuel","1samuel":"1 samuel",
  "2sa":"2 samuel","2samuel":"2 samuel",
  "1ki":"1 kings","1kings":"1 kings",
  "2ki":"2 kings","2kings":"2 kings",
  "1ch":"1 chronicles","1chronicles":"1 chronicles",
  "2ch":"2 chronicles","2chronicles":"2 chronicles",
  ezr:"ezra",ezra:"ezra",
  neh:"nehemiah",nehemiah:"nehemiah",
  est:"esther",esther:"esther",
  job:"job",jb:"job",
  ps:"psalms",psa:"psalms",psalm:"psalms",psalms:"psalms",
  prov:"proverbs",pro:"proverbs",pr:"proverbs",proverbs:"proverbs",
  ec:"ecclesiastes",ecc:"ecclesiastes",eccl:"ecclesiastes",ecclesiastes:"ecclesiastes",
  sng:"song of solomon",song:"song of solomon","song of solomon":"song of solomon",
  isa:"isaiah",is:"isaiah",isaiah:"isaiah",
  jer:"jeremiah",jr:"jeremiah",jeremiah:"jeremiah",
  lam:"lamentations",lamentations:"lamentations",
  ezk:"ezekiel",ezek:"ezekiel",eze:"ezekiel",ezekiel:"ezekiel",
  dan:"daniel",dn:"daniel",daniel:"daniel",
  hos:"hosea",hosea:"hosea",
  joel:"joel",amo:"amos",amos:"amos",oba:"obadiah",obadiah:"obadiah",
  jon:"jonah",jonah:"jonah",mic:"micah",micah:"micah",nam:"nahum",nahum:"nahum",
  hab:"habakkuk",habakkuk:"habakkuk",
  zep:"zephaniah",zephaniah:"zephaniah",hag:"haggai",haggai:"haggai",
  zec:"zechariah",zechariah:"zechariah",mal:"malachi",malachi:"malachi",
  mt:"matthew",matt:"matthew",mat:"matthew",matthew:"matthew",
  mk:"mark",mar:"mark",mr:"mark",mark:"mark",
  lk:"luke",lu:"luke",luke:"luke",
  jn:"john",jhn:"john",john:"john",
  ac:"acts",acts:"acts",act:"acts",
  rom:"romans",rm:"romans",romans:"romans",
  "1co":"1 corinthians","1cor":"1 corinthians","1corinthians":"1 corinthians","corinthians":"1 corinthians",
  "2co":"2 corinthians","2cor":"2 corinthians","2corinthians":"2 corinthians",
  gal:"galatians",ga:"galatians",galatians:"galatians",
  eph:"ephesians",ephesians:"ephesians",
  phil:"philippians",php:"philippians",philippians:"philippians",
  col:"colossians",colossians:"colossians",
  "1th":"1 thessalonians","1thes":"1 thessalonians","1thessalonians":"1 thessalonians","thessalonians":"1 thessalonians",
  "2th":"2 thessalonians","2thes":"2 thessalonians","2thessalonians":"2 thessalonians",
  "1ti":"1 timothy","1tim":"1 timothy","1timothy":"1 timothy","timothy":"1 timothy",
  "2ti":"2 timothy","2tim":"2 timothy","2timothy":"2 timothy",
  tit:"titus",titus:"titus",
  phm:"philemon",philemon:"philemon",
  heb:"hebrews",hebrews:"hebrews",
  jas:"james",jam:"james",james:"james",
  "1pe":"1 peter","1pet":"1 peter","1peter":"1 peter","peter":"1 peter",
  "2pe":"2 peter","2pet":"2 peter","2peter":"2 peter",
  "1jn":"1 john","1john":"1 john","1jhn":"1 john",
  "2jn":"2 john","2john":"2 john","2jhn":"2 john",
  "3jn":"3 john","3john":"3 john","3jhn":"3 john",
  jud:"jude",jude:"jude",
  rev:"revelation",revelation:"revelation",
};
