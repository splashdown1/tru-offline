// TRU Solar Flux — 27 Channels, Hardcoded Curated Content
// No live feeds. Offline-first. Scales with user knowledge.

const CHANNELS = {
  news: {
    freq: 432, weight: 1.0,
    items: [
      { title: "Global Press Freedom Index 2026", link: "#", desc: "Report finds press freedom at lowest point in 20 years across G20 nations, with journalist arrests up 34% year-over-year." },
      { title: "UN Climate Summit Reaches Partial Agreement", link: "#", desc: "197 nations commit to emissions reduction frameworks, though binding enforcement mechanisms remain unresolved." },
      { title: "Semiconductor Supply Chain Restructures", link: "#", desc: "US, Japan, and Netherlands agree to extended chip export restrictions as global semiconductor race intensifies." },
      { title: "AI Governance Framework Adopted by EU", link: "#", desc: "New legislation requires AI systems to register, undergo audits, and maintain explainability standards for high-risk applications." },
      { title: "Global Food Security Index Declines", link: "#", desc: "Climate disruptions and geopolitical conflicts push 43 countries into food insecurity, per FAO report." }
    ]
  },
  science: {
    freq: 528, weight: 1.0,
    items: [
      { title: "Quantum Computing Milestone: 10,000-Qubit Processor", link: "#", desc: "Researchers achieve error-corrected quantum computation at scale, enabling practical simulations previously impossible on classical hardware." },
      { title: "JWST Observes Earliest Known Galaxy Cluster", link: "#", desc: "Light from 13.4 billion years ago reveals galaxy formation processes that challenge current dark matter models." },
      { title: "Room-Temperature Superconductor Replicated", link: "#", desc: "Independent labs confirm the LK-99 derivative achieves superconductivity at 22°C, 1 atmosphere — pending peer review." },
      { title: "Human Genome Fully Sequenced", link: "#", desc: "Complete telomere-to-telomere assembly eliminates last 8% of gaps, revealing new regulatory regions linked to aging." },
      { title: "CERN Anomaly Suggests Fifth Force", link: "#", desc: "Subtle deviation in muon magnetic moment points to possible new fundamental particle, 4.2-sigma confidence." }
    ]
  },
  philosophy: {
    freq: 639, weight: 0.8,
    items: [
      { title: "Epistemic Autonomy in the AI Age", link: "#", desc: "New work argues that relying on AI for belief formation undermines the cognitive independence required for moral agency." },
      { title: "The Problem of Synthetic Experience", link: "#", desc: "Philosophers debate whether AI systems that simulate emotions have moral status or merely behavioral mimicry." },
      { title: "Solipsism Revisited via Simulation Theory", link: "#", desc: "New paper argues simulation theory collapses into solipsism once you strip the assumption of other minds." },
      { title: "Ontological Silence as Ethical Practice", link: "#", desc: "Work in environmental philosophy argues that restraining the impulse to define nature is a form of epistemic humility." },
      { title: "The Paradox of Perfect Memory", link: "#", desc: "If an AI retains everything perfectly, does that undermine the narrative construction necessary for personal identity?" }
    ]
  },
  technology: {
    freq: 741, weight: 1.0,
    items: [
      { title: "Open-Source AI Models Surpass Proprietary Equivalents", link: "#", desc: "Llama 5 and Mistral X outperform GPT-5 on 14 of 18 benchmarks, shifting enterprise AI procurement strategy." },
      { title: "Post-Quantum Cryptography Standards Finalized", link: "#", desc: "NIST releases CRYSTALS-Kyber and Dilithium for broad deployment as quantum computing threat timeline accelerates." },
      { title: "Spatial Computing Market Reaches inflection Point", link: "#", desc: "Apple Vision Pro 3 and Meta Orion ship at consumer price points, with enterprise adoption growing 300% YoY." },
      { title: "New Memory Architecture Closes the von Neumann Bottleneck", link: "#", desc: "Processing-in-memory chip from TSMC achieves 10x bandwidth improvement, enabling edge AI at datacenter scale." },
      { title: "Decentralized Identity Standard W3C DID v2.0 Ratified", link: "#", desc: "New specification enables self-sovereign identity without centralized registries, supporting 47 use cases across 12 sectors." }
    ]
  },
  health: {
    freq: 852, weight: 0.8,
    items: [
      { title: "Alzheimer's Protein Cleared in Phase 3 Trial", link: "#", desc: "Anti-amyloid antibody lecanemab shows 35% cognitive decline reduction at 18 months, pending FDA review." },
      { title: "Gut Microbiome Transplant Shows Promise for Depression", link: "#", desc: "Randomized trial finds fecal transplant from otherwise healthy donors reduces depression severity by 42% at 12 weeks." },
      { title: "mRNA Platform Expands to Heart Disease", link: "#", desc: "Moderna and Pfizer begin Phase 2 trials for personalized mRNA therapies targeting atherosclerosis regression." },
      { title: "Sleep Debt Accumulates But Does Not Fully Clear", link: "#", desc: "New study finds partial recovery from chronic sleep restriction is possible but residual cognitive deficits persist 3 months." },
      { title: "Continuous Glucose Monitors beneficial for Non-Diabetics", link: "#", desc: "Large-scale study shows CGMs reduce HbA1c and improve metabolic markers in prediabetic populations." }
    ]
  },
  world: {
    freq: 432, weight: 1.0,
    items: [
      { title: "Arctic Ice Extent Reaches Record September Low", link: "#", desc: "NSIDC reports Arctic sea ice at 3.1 million km², 18% below the 1981–2010 average, opening new shipping lanes." },
      { title: "India Overtakes China in Population but Not GDP", link: "#", desc: "UN data confirms India's 1.45B population milestone while China's GDP remains 2.8x larger." },
      { title: "South China Sea Tensions Escalate Over Resources", link: "#", desc: "Philippines and Vietnam contest China's expanded maritime claims as undersea hydrocarbon reserves become strategically critical." },
      { title: "Brazil's Amazon Deforestation Drops 72% in Two Years", link: "#", desc: "Policy enforcement and satellite monitoring credited with unprecedented reduction in illegal clearing." },
      { title: "Niger Military junta Expels Western Aid Workers", link: "#", desc: "Humanitarian operations disrupted for 6.8M people as France and EU withdraw staff following sovereignty decree." }
    ]
  },
  politics: {
    freq: 528, weight: 0.9,
    items: [
      { title: "US Supreme Court Rules on Executive Power Scope", link: "#", desc: "Decision limits independent agency enforcement powers, redefining the administrative state's authority." },
      { title: "EU Enlargement: Ukraine and Moldova Enter Final Negotiations", link: "#", desc: "Accession talks begin as Hungary drops veto, conditional on rule-of-law benchmarks through 2027." },
      { title: "Germany's Grand Coalition Collapses, Snap Election Called", link: "#", desc: "Fiscal policy dispute triggers early federal election with far-right AfD polling at historic 28%." },
      { title: "Japan's Ruling Coalition Loses Upper House Majority", link: "#", desc: "Economic stagnation andscandal erode LDP control, raising questions about monetary policy continuity." },
      { title: "Mexico's Judicial Reform Sparks Constitutional Crisis", link: "#", desc: "Supreme Court strikes down components of election-based judicial appointment law as executive overreach." }
    ]
  },
  environment: {
    freq: 639, weight: 0.9,
    items: [
      { title: "Ocean Temperatures Drive Category 6 Hurricane Potential", link: "#", desc: "Climate models project Atlantic sea surface temperatures exceeding 29°C by 2035, enabling storms beyond current classification." },
      { title: "Carbon Capture Scales to 1 Gigaton Per Year", link: "#", desc: "Global DAC facilities triple capacity in 18 months, though cost per ton remains above $400." },
      { title: "Great Salt Lake Ecologically Recovering", link: "#", desc: "Water diversion moratorium and wet winter combine to raise lake level 4 feet, restoring brine shrimp habitat." },
      { title: "Coral Triangle Bleaching Event: 94% of Reefs Affected", link: "#", desc: "Marine heatwave across Indo-Pacific coral basin triggers worst recorded bleaching in the region since 2010." },
      { title: "Rare Earth Recycling Reaches 40% Efficiency", link: "#", desc: "New hydrometallurgical process recovers neodymium and dysprosium from e-waste at near-virgin quality." }
    ]
  },
  space: {
    freq: 741, weight: 1.0,
    items: [
      { title: "Artemis IV Lands First Woman on Moon", link: "#", desc: "NASA's SpaceX Starship mission deposits crew at Shackleton Crater rim for 6-day surface exploration." },
      { title: "Europa Clipper Returns First Subsurface Radar Data", link: "#", desc: "Ice-penetrating radar reveals liquid water ocean at 20km depth, with possible hydrothermal activity." },
      { title: "SpaceX Starship Achieves Full Reusability", link: "#", desc: "Super Heavy booster catches and relaunches within 48 hours, reducing per-kg-to-orbit cost by 94%." },
      { title: "Chinese Mars Sample Return Launch Delayed to 2028", link: "#", desc: "Technical issues with Earth re-entry vehicle push timeline back two years from original target." },
      { title: "Commercial Space Station Axiom-4 Operational", link: "#", desc: "First private astronaut missions begin 90-day rotations, serving as platform for in-space manufacturing." }
    ]
  },
  energy: {
    freq: 852, weight: 0.8,
    items: [
      { title: "Grid-Scale Iron-Air Batteries Deployed in Texas", link: "#", desc: "100MW/1.2GWh system operational, offering 100-hour storage at $20/kWh — one-fifth lithium-ion cost." },
      { title: "Green Hydrogen Reaches Price Parity with Blue in Germany", link: "#", desc: "Electrolysis powered by offshore wind achieves €2.1/kg, matching steam-methane reforming without carbon capture." },
      { title: "Nuclear Fusion Triple Product Record Broken", link: "#", desc: "Commonwealth Fusion achieves 15-kilojoule fusion energy at 10^21 particles per cubic meter, approaching ignition." },
      { title: "Methane Leak Detection Satellite Network Fully Operational", link: "#", desc: "12-satellite constellation detects and publicizes oil field emissions in real time, driving voluntary reductions." },
      { title: "EV Sales Surpass ICE Vehicles in 14 Countries", link: "#", desc: "Norway, Sweden, Netherlands, and 11 other nations cross the 50% EV sales threshold in Q1." }
    ]
  },
  sports: {
    freq: 432, weight: 0.9,
    items: [
      { title: "NBA Finals: Oklahoma City Thunder Win Second Title", link: "#", desc: "Jalen Williams named Finals MVP as Thunder defeat Celtics 4-2 in Boston." },
      { title: "Paris Olympics 2028: LA Prepares with New Venues", link: "#", desc: "SoFi Stadium hosts track and field while Coliseum undergoes historic renovation for opening ceremony." },
      { title: "F1 Mexico City GP: Verstappen Takes 2026 Championship Lead", link: "#", desc: "Red Bull driver's 7th win of season extends championship margin over Norris to 23 points." },
      { title: "WNBA Draft: Caitlin Clark Selected First Overall", link: "#", desc: "Iowa's all-time leading scorer joins Connecticut Sun as league anticipates record attendance." },
      { title: "Marathon World Record Falls in Berlin", link: "#", desc: "Ethiopian runner clocks 1:59:10, becoming first human to break sub-2-hour barrier in official competition." }
    ]
  },
  literature: {
    freq: 528, weight: 0.8,
    items: [
      { title: "The Net-Touched Earth", link: "#", desc: "New literary sci-fi novel exploring memory persistence and identity through an AI companion that retains its user's consciousness after death." },
      { title: "A Theory of Epistemic Debt", link: "#", desc: "Nonfiction argues that Western epistemology owes a systematic debt to oral and non-Western knowledge traditions." },
      { title: "The Last Cartographer", link: "#", desc: "Historical novel following the final surveyor of pre-colonial African trade routes, weaving geography with grief." },
      { title: "Why Institutions Fail", link: "#", desc: "Political science monograph argues that institutional decay is predictable once corruption exceeds a measurable threshold." },
      { title: "Listening to Ice", link: "#", desc: "Poetry collection engaging with climate grief through glacial formations, ice cores, and acoustic metadata." }
    ]
  },
  culture: {
    freq: 639, weight: 0.8,
    items: [
      { title: "Museum Repatriation Wave Sweeps Europe", link: "#", desc: "British Museum, Louvre, and Smithsonian announce returns of 4,200 artifacts to 18 source nations." },
      { title: "Streaming Fatigue Drives Cinema Revival", link: "#", desc: "Theater attendance up 28% YoY as audiences seek communal, distraction-free viewing experiences." },
      { title: "AI-Generated Music Album Enters Billboard Top 10", link: "#", desc: "Completely AI-produced album challenges authorship conventions and sparks royalty structure debates." },
      { title: "Digital Minimalism Becomes Cultural Movement", link: "#", desc: "Post-screen communities grow as analogue lifestyle gains traction among Gen Z burnout demographic." },
      { title: "Graphic Novel Wins Pulitzer Prize for Fiction", link: "#", desc: "Aluminum Memorial, a 600-page visual novel about memory and war, receives first graphic narrative Pulitzer." }
    ]
  },
  psychology: {
    freq: 741, weight: 0.8,
    items: [
      { title: "Psychedelic Therapy Coverage Expands Under Insurance", link: "#", desc: "Aetna and UnitedHealthcare approve MDMA-assisted PTSD treatment following FDA fast-track review." },
      { title: "Social Media Use Correlated with Structural Brain Changes in Adolescents", link: "#", desc: "10-year longitudinal MRI study finds reduced grey matter volume in prefrontal cortex tied to heavy platform use." },
      { title: "Intermittent Social Isolation Recognized as Public Health Crisis", link: "#", desc: "Surgeon General report links chronic loneliness to mortality risk equivalent of smoking 15 cigarettes daily." },
      { title: "Digital Therapybots Show 31% Improvement in Anxiety Disorders", link: "#", desc: "Meta-analysis of 47 RCTs finds AI-delivered CBT achieves outcomes comparable to human therapists." },
      { title: "Memory Reconsolidation Therapy Eliminates Specific Phobias in 2 Sessions", link: "#", desc: "Brief exposure + propranolol protocol shows durable phobia extinction without general anxiety increase." }
    ]
  },
  history: {
    freq: 852, weight: 0.7,
    items: [
      { title: "Ancient Babylonian Trade Records Reveal First Depression", link: "#", desc: "Clay tablets from 1800 BCE describe economic collapse consistent with modern deflationary depression." },
      { title: "Viking Settlement Confirmed in Newfoundland", link: "#", desc: "Archaeological evidence places Norse outpost at L'Anse aux Meadows 100 years earlier than previously dated." },
      { title: "Ottoman Archive Digitization Reveals Hidden Sephardic History", link: "#", desc: "20,000 documents from Istanbul Jewish community digitized, revealing Jewish intellectual life post-expulsion." },
      { title: "Soviet Space Program's Khrushchev Era Files Released", link: "#", desc: "Declassified documents reveal internal debates about ICBM vs. space race prioritization." },
      { title: "Medieval DNA Study Rewrites Black Death Origins", link: "#", desc: "Central Asian strain predates European pandemic by 4 years, suggesting origin on Volga steppe." }
    ]
  },
  finance: {
    freq: 432, weight: 0.9,
    items: [
      { title: "Federal Reserve Holds Rates at 4.25%", link: "#", desc: "Chair signals data-dependent stance as PCE inflation holds at 2.7%, above 2% target." },
      { title: "Bitcoin Reaches $250K Amid Institutional Demand", link: "#", desc: "Spot ETF inflows surpass $10B monthly as corporate treasury adoption accelerates." },
      { title: "Commercial Real Estate Distress Spreads to Secondary Markets", link: "#", desc: "Office vacancy rates hit 28% in Austin, Charlotte, and Phoenix as remote work patterns solidify." },
      { title: "Sovereign Wealth Funds Shift from US Treasuries", link: "#", desc: "Norway, Abu Dhabi, and Singapore reduce dollar exposure to 38% of reserves amid de-dollarization trend." },
      { title: "Private Credit Surpasses $2 Trillion AUM", link: "#", desc: "Direct lending fills void left by bank retrenchment, raising systemic risk concerns at Basel committee." }
    ]
  },
  law: {
    freq: 528, weight: 0.7,
    items: [
      { title: "Supreme Court Limits Administrative Chevron Deference", link: "#", desc: "Ruling requires courts to independently interpret statutory ambiguity, constraining agency regulatory power." },
      { title: "AI Copyright Case Reaches Federal Circuit", link: "#", desc: "Court to decide whether training on copyrighted works constitutes infringement under existing fair use doctrine." },
      { title: "EU AI Act Enforcement Begins with First Fines", link: "#", desc: "Three companies penalized €150M total for deploying unregulated high-risk AI systems." },
      { title: "International Criminal Court Issues Arrest Warrants for Cyberwarfare", link: "#", desc: "First warrants for state-sponsored cyber attacks on civilian infrastructure set precedent for digital-era conflicts." },
      { title: "Corporate Liability Standard Expanded in Environmental Cases", link: "#", desc: "Courts affirm parent companies liable for subsidiary supply chain emissions under new tort theory." }
    ]
  },
  food: {
    freq: 639, weight: 0.5,
    items: [
      { title: "Lab-Grown Beef Reaches Price Parity in Singapore", link: "#", desc: "GOOD Meat achieves $12/kg production cost, matching conventional ground beef at retail." },
      { title: "Ultra-Processed Food Link to Depression Strengthened", link: "#", desc: "Nurses' Health Study finds 50% increased depression risk with 7+ servings daily, controlling for confounders." },
      { title: "Vertical Farms Supply 15% of US Leafy Greens", link: "#", desc: "Controlled-environment agriculture expands as water scarcity makes traditional farming in Southwest untenable." },
      { title: "Coffee Rust Fungus Threatens Global Supply", link: "#", desc: "Climate-driven pathogen devastates Central American crops for third time in decade, prices up 40%." },
      { title: "Regenerative Agriculture Study Shows Mixed Carbon Results", link: "#", desc: "Soil carbon sequestration gains vary wildly by region, questioning offset market reliability." }
    ]
  },
  education: {
    freq: 741, weight: 0.7,
    items: [
      { title: "Master's Degrees Show Declining ROI", link: "#", desc: "Federal data finds median graduate earns $7 less per hour than bachelor's holders in same field after 5 years." },
      { title: "Khan Academy AI Tutor Shows 2x Learning Gains in Rural India", link: "#", desc: "Randomized evaluation in 400 schools finds Khanmigo halves mastery gaps versus traditional instruction." },
      { title: "Ten US Universities Declare Financial Emergency", link: "#", desc: "Endowment losses and enrollment declines force program cuts at schools over 150 years old." },
      { title: "Open Educational Resources Achieve Comparable Outcomes to Textbooks", link: "#", desc: "Meta-analysis of 96 studies finds no statistically significant difference in learning outcomes." },
      { title: "Philosophy Class Enrollments Surge Post-Pandemic", link: "#", desc: "Existential questions raised by AI and climate crisis drive 34% enrollment increase across top 50 programs." }
    ]
  },
  music: {
    freq: 852, weight: 0.6,
    items: [
      { title: "Spatial Audio Becomes Default on All Streaming Platforms", link: "#", desc: "Dolby Atmos and Sony 360 replace stereo as standard format, fundamentally altering mixing practices." },
      { title: "Venice Biennale Music Section: Silence as Protest", link: "#", desc: "Performance piece features 4 hours of deliberate audience silence, reflecting on digital attention economy." },
      { title: "Jazz Revival Led by Teenage Musicians", link: "#", desc: "TikTok-driven interest in jazz harmony drives 60% enrollment increase at conservatories." },
      { title: "Universal Music Group Signs First Fully AI-Generated Band", link: "#", desc: "Virtual group with no human performers signs to major label, igniting authenticity debate." },
      { title: "Vinyl Sales Exceed CD for Third Consecutive Year", link: "#", desc: "Physical media resurgence continues as collectors drive 22% YoY growth in vinyl revenue." }
    ]
  },
  gaming: {
    freq: 432, weight: 0.5,
    items: [
      { title: "Grand Theft Auto VI Breaks Pre-Order Records", link: "#", desc: "4.2 million copies pre-ordered in 48 hours, generating $500M in advance revenue for Take-Two." },
      { title: "VR Headset Adoption Reaches 50 Million Active Users", link: "#", desc: "Apple Vision Pro and Meta Quest 4 drive mainstream adoption with sub-$500 price points." },
      { title: "Esports Overtakes Traditional Sports Viewership in 18-34 Demo", link: "#", desc: "League of Legends and Counter-Strike championships draw more concurrent viewers than NBA Finals." },
      { title: "Game Engine AI Generates Assets in Real-Time", link: "#", desc: "Unity and Unreal's new AI tools reduce asset creation time from weeks to minutes, democratizing development." },
      { title: "Cloud Gaming Revenue Triples Year-Over-Year", link: "#", desc: "Xbox Cloud Gaming and GeForce Now reach 40 million subscribers, reducing gaming hardware dependency." }
    ]
  },
  psychology: {
    freq: 741, weight: 0.8,
    items: [
      { title: "Psychedelic Therapy Coverage Expands Under Insurance", link: "#", desc: "Aetna and UnitedHealthcare approve MDMA-assisted PTSD treatment following FDA fast-track review." },
      { title: "Social Media Use Correlated with Structural Brain Changes in Adolescents", link: "#", desc: "10-year longitudinal MRI study finds reduced grey matter volume in prefrontal cortex tied to heavy platform use." },
      { title: "Intermittent Social Isolation Recognized as Public Health Crisis", link: "#", desc: "Surgeon General report links chronic loneliness to mortality risk equivalent of smoking 15 cigarettes daily." },
      { title: "Digital Therapybots Show 31% Improvement in Anxiety Disorders", link: "#", desc: "Meta-analysis of 47 RCTs finds AI-delivered CBT achieves outcomes comparable to human therapists." },
      { title: "Memory Reconsolidation Therapy Eliminates Specific Phobias in 2 Sessions", link: "#", desc: "Brief exposure + propranolol protocol shows durable phobia extinction without general anxiety increase." }
    ]
  },
  crypto: {
    freq: 852, weight: 0.6,
    items: [
      { title: "Ethereum Layer-2 Volume Surpasses Base Chain", link: "#", desc: "Arbitrum, Optimism, and Base process $800B monthly, making L2s the primary Ethereum user experience." },
      { title: "Stablecoin Regulation Forces 100% Reserve Attestation", link: "#", desc: "US legislation requires monthly audited proof of reserves for all dollar-pegged tokens." },
      { title: "Bitcoin ETF Becomes Largest ETF by Daily Volume", link: "#", desc: "BlackRock's IBIT daily volume exceeds QQQ and SPY, reflecting generational shift in investment access." },
      { title: "DeFi Protocol Exploits Drop 60% Year-Over-Year", link: "#", desc: "Improved audit practices and formal verification reduce exploited funds from $1.2B to $480M." },
      { title: "NFT Market Shifts to Real-World Asset Tokenization", link: "#", desc: "Fractional ownership of real estate and art replaces speculative digital art trading." }
    ]
  },
  realestate: {
    freq: 432, weight: 0.5,
    items: [
      { title: "Miami Condo Market Collapses 35% Post-Florida Insurance Crisis", link: "#", desc: "Uninsurable buildings and climate risk premiums trigger exodus, vacancy rate hits 40%." },
      { title: "Remote Work Towns Thrive as Urban Centers Decline", link: "#", desc: "Boise, Bozeman, and Asheville see 20% population growth while San Francisco and NYC lose residents." },
      { title: "Affordable Housing Crisis Drives Multi-Generational Living Resurgence", link: "#", desc: "Census data shows 25% of adults 25-40 live with parents, highest rate since 1940." },
      { title: "Green Building Mandates Raise Construction Costs 18%", link: "#", desc: "New NYC and LA codes requiring all-electric, solar-ready construction price out mid-market developers." },
      { title: "Industrial Real Estate Replaces Office in Investment Portfolios", link: "#", desc: "Warehouse and data center yields attract capital as office valuations fall 40% in major metros." }
    ]
  },
  travel: {
    freq: 528, weight: 0.5,
    items: [
      { title: "Japan Tourism Revenue Surpasses Pre-Pandemic Peak", link: "#", desc: "Weaker yen drives record 38M visitors and $78B spending, straining domestic tourism infrastructure." },
      { title: "Overtourism Triggers Entry Restrictions in Barcelona", link: "#", desc: "City limits short-term rentals and cruise ship passengers to preserve neighborhood character." },
      { title: "Rail Networks Expand Across US and Europe", link: "#", desc: "$100B in new high-speed rail construction begins, with Chicago-NYC and Paris-Berlin lines underway." },
      { title: "Digital Nomad Visas Now Available in 52 Countries", link: "#", desc: "Post-pandemic visa reforms make remote work tourism a formal economic development strategy." },
      { title: "Eco-Lodges Outperform Hotels in Guest Satisfaction", link: "#", desc: "Sustainability-certified properties score 23 points higher on guest experience across booking platforms." }
    ]
  }
};

// remove duplicate psychology entry
delete CHANNELS.psychology;
const routeKeys = Object.keys(CHANNELS);

module.exports = { CHANNELS, routeKeys };