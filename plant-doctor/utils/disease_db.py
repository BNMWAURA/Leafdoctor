"""
Complete disease knowledge base for 13 supported crops.
Includes symptoms, pathogen, severity, treatment, prevention, recovery.
"""

DISEASE_DB: dict = {
    "Tomato": {
        "icon": "🍅",
        "diseases": {
            "Early Blight": {
                "pathogen": "Alternaria solani (fungus)",
                "severity": "Medium",
                "symptoms": ["Dark brown spots with concentric rings (target-board pattern)", "Yellow halo around lesions", "Lower leaves affected first", "Lesions merge causing leaf death"],
                "treatment": ["Apply chlorothalonil or mancozeb fungicide every 7–10 days", "Remove and destroy infected leaves immediately", "Apply copper-based fungicide as organic option"],
                "prevention": ["Use certified disease-free seeds", "Rotate crops every 2–3 years", "Avoid overhead irrigation", "Improve air circulation with proper spacing"],
                "recovery": "14–21 days with consistent treatment",
            },
            "Late Blight": {
                "pathogen": "Phytophthora infestans (oomycete)",
                "severity": "Very High",
                "symptoms": ["Water-soaked irregular greenish-grey spots", "White mouldy growth on leaf undersides", "Rapid browning and death of leaves", "Dark brown streaks on stems"],
                "treatment": ["Apply metalaxyl or cymoxanil fungicides immediately", "Remove all infected plant material", "Use fosetyl-aluminium as preventive spray"],
                "prevention": ["Plant resistant varieties", "Avoid planting near potatoes", "Apply preventive copper fungicide during wet seasons", "Stake plants for better air circulation"],
                "recovery": "7–14 days if caught early",
            },
            "Leaf Miner": {
                "pathogen": "Liriomyza spp. (insect)",
                "severity": "Low-Medium",
                "symptoms": ["Winding white/yellow tunnels (mines) on leaf surface", "Small white stippling dots on leaves", "Premature leaf drop"],
                "treatment": ["Apply spinosad or abamectin insecticide", "Remove heavily infested leaves", "Introduce parasitic wasps (Diglyphus isaea) as biocontrol"],
                "prevention": ["Use yellow sticky traps to monitor adults", "Install fine mesh netting over seedbeds", "Avoid over-application of nitrogen fertiliser"],
                "recovery": "10–14 days with treatment",
            },
            "Bacterial Spot": {
                "pathogen": "Xanthomonas campestris (bacterium)",
                "severity": "Medium-High",
                "symptoms": ["Small water-soaked spots turning dark brown", "Yellow halo around lesions", "Scab-like lesions on fruit", "Leaf distortion and drop"],
                "treatment": ["Apply copper hydroxide bactericide", "Use streptomycin sulfate spray", "Remove infected plant debris"],
                "prevention": ["Use disease-free certified seeds", "Avoid working when plants are wet", "Rotate crops with non-solanaceous plants"],
                "recovery": "21–28 days",
            },
            "Septoria Leaf Spot": {
                "pathogen": "Septoria lycopersici (fungus)",
                "severity": "Medium",
                "symptoms": ["Small circular spots with dark brown margins and grey centres", "Dark specks (pycnidia) visible in lesion centres", "Lower leaves affected first", "Severe defoliation"],
                "treatment": ["Chlorothalonil or mancozeb fungicide", "Remove infected leaves immediately", "Copper-based spray as organic option"],
                "prevention": ["Crop rotation", "Avoid working when plants are wet", "Mulching to reduce soil splash"],
                "recovery": "14–21 days",
            },
            "Spider Mites": {
                "pathogen": "Tetranychus urticae (mite)",
                "severity": "Medium",
                "symptoms": ["Fine yellow stippling on upper leaf surface", "Fine webbing on leaves in severe cases", "Leaves turn bronze/yellow then die"],
                "treatment": ["Apply abamectin or bifenazate miticide", "Neem oil spray", "Introduce predatory mite Phytoseiulus persimilis"],
                "prevention": ["Avoid water stress — stressed plants more susceptible", "Avoid dusty conditions", "Monitor with hand lens weekly"],
                "recovery": "7–14 days",
            },
            "Target Spot": {
                "pathogen": "Corynespora cassiicola (fungus)",
                "severity": "Medium",
                "symptoms": ["Brown concentric ring lesions on leaves", "Lesions with yellow halos", "Premature leaf drop"],
                "treatment": ["Azoxystrobin or chlorothalonil fungicide", "Remove infected foliage"],
                "prevention": ["Good ventilation", "Avoid overhead irrigation", "Crop rotation"],
                "recovery": "14–21 days",
            },
            "Yellow Leaf Curl Virus": {
                "pathogen": "Tomato Yellow Leaf Curl Virus (begomovirus)",
                "severity": "Very High",
                "symptoms": ["Upward curling and yellowing of young leaves", "Stunted plant growth", "Flower drop and poor fruit set"],
                "treatment": ["No cure — remove infected plants", "Control whitefly vectors urgently with imidacloprid"],
                "prevention": ["Use resistant varieties (TY varieties)", "Install insect-proof nets", "Eradicate whitefly populations"],
                "recovery": "Not recoverable — remove and destroy plant",
            },
            "Mosaic Virus": {
                "pathogen": "Tomato Mosaic Virus (tobamovirus)",
                "severity": "High",
                "symptoms": ["Mosaic light/dark green mottling on leaves", "Leaf distortion and malformation", "Stunted growth", "Poor fruit quality"],
                "treatment": ["No chemical cure — remove infected plants", "Disinfect tools with 10% bleach"],
                "prevention": ["Handle transplants carefully", "Control aphid vectors", "Wash hands before handling plants"],
                "recovery": "Not recoverable — rogue plants",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Vibrant green leaves", "No lesions or discolouration", "Normal growth and development"],
                "treatment": ["Continue regular crop management practices"],
                "prevention": ["Maintain scouting schedule twice weekly"],
                "recovery": "N/A — plant is healthy",
            },
        },
    },

    "Maize": {
        "icon": "🌽",
        "diseases": {
            "Northern Leaf Blight": {
                "pathogen": "Exserohilum turcicum (fungus)",
                "severity": "High",
                "symptoms": ["Long elliptical 2.5–15 cm grey-green lesions", "Lesions turn tan with age", "Dark spores visible in centres", "Lower leaves infected first"],
                "treatment": ["Propiconazole or azoxystrobin fungicide at tassel emergence", "Spray before 50% lesion coverage on lower leaves"],
                "prevention": ["Plant resistant hybrids", "Crop rotation with non-grass crops", "Bury crop residue after harvest"],
                "recovery": "14–21 days",
            },
            "Gray Leaf Spot": {
                "pathogen": "Cercospora zeae-maydis (fungus)",
                "severity": "High",
                "symptoms": ["Rectangular pale grey lesions bounded by leaf veins", "Lesions run parallel to leaf margins", "Premature leaf death in severe cases"],
                "treatment": ["Strobilurin or triazole fungicide", "Apply at early detection stage"],
                "prevention": ["Tolerant hybrids", "Minimum tillage to reduce residue", "Adequate plant spacing"],
                "recovery": "14–28 days",
            },
            "Common Rust": {
                "pathogen": "Puccinia sorghi (fungus)",
                "severity": "Medium",
                "symptoms": ["Small oval brick-red pustules on both leaf surfaces", "Pustules release powdery rust-red spores", "Severe infection causes yellowing"],
                "treatment": ["Mancozeb or propiconazole at first sign of disease", "Remove badly infected leaves"],
                "prevention": ["Plant rust-resistant varieties", "Early planting to avoid peak rust season"],
                "recovery": "10–14 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Deep green healthy leaves", "No lesions or pustules", "Normal growth"],
                "treatment": ["Maintain regular fertilisation schedule"],
                "prevention": ["Scout during humid periods, especially silking"],
                "recovery": "N/A",
            },
        },
    },

    "Potato": {
        "icon": "🥔",
        "diseases": {
            "Early Blight": {
                "pathogen": "Alternaria solani (fungus)",
                "severity": "Medium",
                "symptoms": ["Dark brown circular lesions with concentric rings", "Yellow halo around lesions", "Older leaves affected first", "Defoliation under severe conditions"],
                "treatment": ["Chlorothalonil or mancozeb fungicide every 7–10 days", "Spray during wet weather"],
                "prevention": ["Certified disease-free seed tubers", "Avoid water stress", "Rotate with non-solanaceous crops"],
                "recovery": "14–21 days",
            },
            "Late Blight": {
                "pathogen": "Phytophthora infestans (oomycete)",
                "severity": "Very High",
                "symptoms": ["Water-soaked pale green to brown leaf spots", "White sporulation on leaf undersides", "Rapid foliage collapse", "Brown rot in tubers"],
                "treatment": ["Metalaxyl-M or cymoxanil + mancozeb fungicide", "Remove and destroy infected foliage immediately", "Do not compost infected tubers"],
                "prevention": ["Plant resistant varieties", "Preventive copper sprays in wet seasons", "Hill soil around plants to protect tubers"],
                "recovery": "10–14 days if treated early",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy dark green foliage", "No lesions or discolouration"],
                "treatment": ["Regular hilling and irrigation management"],
                "prevention": ["Monitor for Colorado beetle and aphid vectors"],
                "recovery": "N/A",
            },
        },
    },

    "Coffee": {
        "icon": "☕",
        "diseases": {
            "Leaf Rust": {
                "pathogen": "Hemileia vastatrix (fungus)",
                "severity": "Very High",
                "symptoms": ["Yellow-orange powdery spots on leaf undersides", "Corresponding pale yellow areas on upper surface", "Premature leaf drop", "Branch dieback in severe cases"],
                "treatment": ["Triazole fungicides (propiconazole, tebuconazole)", "Copper-based fungicides as organic option", "Foliar spray at 6–8 week intervals"],
                "prevention": ["Plant resistant varieties (Catimor, Ruiru 11)", "Prune for canopy air circulation", "Balanced fertilisation — avoid excess nitrogen"],
                "recovery": "21–30 days",
            },
            "Berry Borer": {
                "pathogen": "Hypothenemus hampei (insect)",
                "severity": "High",
                "symptoms": ["Small circular entry holes in coffee berries", "Premature berry drop", "Discolouration inside affected berries"],
                "treatment": ["Spinetoram insecticide", "Beauveria bassiana biological control", "Harvest all ripe berries promptly"],
                "prevention": ["Regular harvesting to remove all ripe/overripe berries", "Strip picking at season end", "Use berry borer traps with attractant"],
                "recovery": "Ongoing management required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Deep green glossy leaves", "No lesions or powder"],
                "treatment": ["Continue regular shade management and fertilisation"],
                "prevention": ["Scout weekly during rainy season"],
                "recovery": "N/A",
            },
        },
    },

    "Banana": {
        "icon": "🍌",
        "diseases": {
            "Black Sigatoka": {
                "pathogen": "Mycosphaerella fijiensis (fungus)",
                "severity": "Very High",
                "symptoms": ["Small yellow streaks on leaf surface", "Streaks enlarge to dark brown-black elliptical lesions", "Lesions with grey centre and yellow halo", "Premature leaf death and yield loss"],
                "treatment": ["Systemic fungicides: propiconazole, tridemorph", "Oil-based sprays to reduce humidity on leaves", "Regular leaf stripping of infected material"],
                "prevention": ["Use tolerant varieties (FHIA hybrids)", "Remove and destroy infected leaf portions", "Adequate spacing for air circulation"],
                "recovery": "21–35 days with intensive management",
            },
            "Panama Disease": {
                "pathogen": "Fusarium oxysporum f.sp. cubense (fungus)",
                "severity": "Very High",
                "symptoms": ["Yellowing of older outer leaves", "Wilting and collapse of leaf petioles", "Brown-red discolouration inside pseudostem", "Plant death — no recovery possible"],
                "treatment": ["No effective chemical cure — remove and destroy infected plants", "Quarantine affected area immediately", "Drench soil with fungicide to reduce spread"],
                "prevention": ["Plant Cavendish or TR4-resistant varieties", "Use certified disease-free tissue culture plants", "Disinfect tools with 10% bleach solution"],
                "recovery": "Not recoverable — field replanting required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Bright green upright leaves", "No streaks or browning"],
                "treatment": ["Regular sucker management and fertilisation"],
                "prevention": ["Inspect new planting material for disease signs"],
                "recovery": "N/A",
            },
        },
    },

    "Beans": {
        "icon": "🫘",
        "diseases": {
            "Angular Leaf Spot": {
                "pathogen": "Phaeoisariopsis griseola (fungus)",
                "severity": "High",
                "symptoms": ["Angular brown lesions bounded by leaf veins", "Grey sporulation on leaf undersides", "Lesions coalesce causing leaf death", "Water-soaked spots on pods"],
                "treatment": ["Mancozeb or chlorothalonil fungicide spray", "Remove infected leaves and debris"],
                "prevention": ["Resistant varieties", "Crop rotation every 2 years", "Avoid overhead irrigation"],
                "recovery": "14–21 days",
            },
            "Bean Rust": {
                "pathogen": "Uromyces appendiculatus (fungus)",
                "severity": "Medium-High",
                "symptoms": ["Brown powdery pustules on leaves", "Yellow halo around pustules", "Severe defoliation if untreated"],
                "treatment": ["Triadimefon or mancozeb fungicide", "Apply at first pustule appearance"],
                "prevention": ["Resistant varieties", "Wider plant spacing", "Avoid planting during peak rust season"],
                "recovery": "14–21 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Uniform green leaves", "No spots or pustules"],
                "treatment": ["Regular weeding and balanced NPK fertilisation"],
                "prevention": ["Scout during humid rainy periods"],
                "recovery": "N/A",
            },
        },
    },

    "Cassava": {
        "icon": "🪴",
        "diseases": {
            "Cassava Mosaic Disease": {
                "pathogen": "Cassava mosaic begomoviruses (virus, whitefly-vectored)",
                "severity": "Very High",
                "symptoms": ["Mosaic yellow-green mottling on leaves", "Leaf distortion and stunting", "Reduced tuber yield by up to 95%"],
                "treatment": ["No direct cure — rogue out infected plants", "Control whitefly vectors with imidacloprid or neem oil"],
                "prevention": ["Use virus-free certified cuttings", "Plant CMD-resistant varieties", "Control whitefly populations"],
                "recovery": "Plant removal required — not recoverable",
            },
            "Cassava Brown Streak Disease": {
                "pathogen": "Cassava brown streak viruses (virus)",
                "severity": "Very High",
                "symptoms": ["Yellowish chlorosis along veins", "Brown necrotic streaks on stems", "Severe brown rot in tubers", "Tubers become inedible"],
                "treatment": ["Remove and destroy infected plants", "Control whitefly populations urgently"],
                "prevention": ["CBSD-tolerant varieties", "Source certified clean cuttings", "Rogue symptomatic plants early"],
                "recovery": "Not recoverable — field management required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy green leaves", "No mosaic or streaks"],
                "treatment": ["Maintain soil fertility with organic manure"],
                "prevention": ["Monitor for whitefly populations weekly"],
                "recovery": "N/A",
            },
        },
    },

    "Wheat": {
        "icon": "🌾",
        "diseases": {
            "Stem Rust": {
                "pathogen": "Puccinia graminis (fungus)",
                "severity": "Very High",
                "symptoms": ["Brick-red oval pustules on stems and leaves", "Pustules rupture releasing reddish spores", "Stem weakening leading to lodging", "Premature grain shrivelling"],
                "treatment": ["Triazole fungicides (propiconazole, tebuconazole)", "Apply at first sign of disease"],
                "prevention": ["Plant resistant varieties", "Early planting to avoid peak rust season", "Destroy volunteer wheat plants"],
                "recovery": "7–14 days with early treatment",
            },
            "Powdery Mildew": {
                "pathogen": "Blumeria graminis f.sp. tritici (fungus)",
                "severity": "Medium",
                "symptoms": ["White powdery patches on upper leaf surfaces", "Patches enlarge covering entire leaf", "Yellow-brown tissue beneath patches"],
                "treatment": ["Triazole or strobilurin fungicide", "Sulphur-based fungicide as organic option"],
                "prevention": ["Resistant varieties", "Reduce seeding rate for better ventilation", "Avoid excessive nitrogen"],
                "recovery": "10–14 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Upright green healthy tillers", "No lesions or powder"],
                "treatment": ["Timely top-dressing with nitrogen at tillering"],
                "prevention": ["Scout 3× per season"],
                "recovery": "N/A",
            },
        },
    },

    "Rice": {
        "icon": "🌾",
        "diseases": {
            "Rice Blast": {
                "pathogen": "Magnaporthe oryzae (fungus)",
                "severity": "Very High",
                "symptoms": ["Diamond-shaped lesions with grey centre and brown border", "Neck rot at panicle base", "Collar rot killing tillers", "Empty panicles (whitehead)"],
                "treatment": ["Tricyclazole or isoprothiolane fungicide", "Spray at panicle initiation and heading"],
                "prevention": ["Resistant varieties (NERICA, IR64-blast resistant)", "Balanced nitrogen — avoid over-application", "Silicon application to strengthen cell walls"],
                "recovery": "10–14 days with treatment",
            },
            "Bacterial Leaf Blight": {
                "pathogen": "Xanthomonas oryzae pv. oryzae (bacterium)",
                "severity": "High",
                "symptoms": ["Water-soaked to yellowish stripes along leaf margins", "Lesions extend to entire leaf", "Milky bacterial ooze from cut tissue", "Wilting of young tillers (kresek)"],
                "treatment": ["Copper-based bactericide spray", "Drain flooded fields to reduce spread"],
                "prevention": ["Resistant varieties", "Avoid excessive nitrogen", "Use clean irrigation water"],
                "recovery": "21–28 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy upright tillers", "Green leaves without lesions"],
                "treatment": ["Regular water management and weeding"],
                "prevention": ["Scout especially after heavy rain or flooding"],
                "recovery": "N/A",
            },
        },
    },

    "Sugarcane": {
        "icon": "🎋",
        "diseases": {
            "Red Rot": {
                "pathogen": "Colletotrichum falcatum (fungus)",
                "severity": "High",
                "symptoms": ["Red discolouration inside cane stalks", "White patches alternating with red tissue", "Sour fermented smell from infected stalks", "Wilting and yellowing of leaves"],
                "treatment": ["No effective field treatment — remove infected stalks", "Treat setts with hot water (50°C, 30 min)", "Fungicidal sett treatment with carbendazim"],
                "prevention": ["Plant resistant varieties", "Use disease-free planting material", "Improve field drainage"],
                "recovery": "Not recoverable in severe cases",
            },
            "Smut": {
                "pathogen": "Sporisorium scitamineum (fungus)",
                "severity": "High",
                "symptoms": ["Whip-like black structure from growing point", "Thin grass-like shoots with black spores", "Stunted growth"],
                "treatment": ["Rogue and destroy infected stools", "Hot water treatment of setts"],
                "prevention": ["Resistant varieties", "Certified disease-free planting material"],
                "recovery": "Not recoverable",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Tall vigorous canes", "Healthy green leaves"],
                "treatment": ["Split nitrogen application for optimal yield"],
                "prevention": ["Inspect ratoon crops for smut whips each season"],
                "recovery": "N/A",
            },
        },
    },

    "Pepper": {
        "icon": "🌶️",
        "diseases": {
            "Anthracnose": {
                "pathogen": "Colletotrichum spp. (fungus)",
                "severity": "High",
                "symptoms": ["Circular water-soaked lesions on fruit", "Lesions turn black with concentric rings", "Salmon-coloured spore masses in lesion centres", "Fruit rot and collapse"],
                "treatment": ["Mancozeb or azoxystrobin fungicide", "Copper-based fungicide for organic approach", "Remove and destroy infected fruit"],
                "prevention": ["Plant resistant varieties", "Avoid overhead irrigation", "Harvest fruit promptly at maturity"],
                "recovery": "14–21 days",
            },
            "Bacterial Wilt": {
                "pathogen": "Ralstonia solanacearum (bacterium)",
                "severity": "Very High",
                "symptoms": ["Sudden wilting of entire plant", "Wilting without initial yellowing", "Brown discolouration inside stem", "Bacterial ooze from cut stem in water"],
                "treatment": ["No effective chemical cure", "Remove and destroy infected plants", "Drench surrounding soil with copper bactericide"],
                "prevention": ["Resistant varieties", "Grafting onto resistant rootstocks", "Strict crop rotation (4+ years)", "Avoid waterlogged soils"],
                "recovery": "Not recoverable",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Dark green leaves", "Firm healthy fruit"],
                "treatment": ["Consistent calcium and potassium application"],
                "prevention": ["Scout weekly for spider mites and aphids"],
                "recovery": "N/A",
            },
        },
    },

    "Mango": {
        "icon": "🥭",
        "diseases": {
            "Powdery Mildew": {
                "pathogen": "Oidium mangiferae (fungus)",
                "severity": "High",
                "symptoms": ["White powdery growth on young leaves, flowers, and fruits", "Flower drop causing yield loss", "Young fruits drop prematurely", "Leaf distortion in severe cases"],
                "treatment": ["Wettable sulphur spray at 2 g/L", "Difenoconazole or hexaconazole systemic fungicide", "Spray at 80% bud burst, full bloom, and fruitlet stage"],
                "prevention": ["Prune for canopy aeration", "Spray preventively at bud burst", "Avoid excessive irrigation near flowering"],
                "recovery": "7–14 days",
            },
            "Anthracnose": {
                "pathogen": "Colletotrichum gloeosporioides (fungus)",
                "severity": "High",
                "symptoms": ["Dark brown to black irregular spots on leaves", "Leaf tip and margin browning", "Black sunken lesions on mature fruit", "Post-harvest fruit rot"],
                "treatment": ["Mancozeb + copper oxychloride mixture", "Post-harvest hot water treatment (52°C, 5 min)", "Propiconazole pre-harvest spray"],
                "prevention": ["Remove and destroy infected plant material", "Avoid overhead irrigation", "Regular canopy pruning"],
                "recovery": "14–21 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Dark glossy green leaves", "Normal flower and fruit development"],
                "treatment": ["Foliar micronutrient spray at flowering"],
                "prevention": ["Scout for mango hoppers during flowering"],
                "recovery": "N/A",
            },
        },
    },

    "Onion": {
        "icon": "🧅",
        "diseases": {
            "Purple Blotch": {
                "pathogen": "Alternaria porri (fungus)",
                "severity": "Medium-High",
                "symptoms": ["Small white lesions with purple centres on leaves", "Lesions enlarge with concentric zones", "Leaf tips die back", "Dark brown rot on bulb necks"],
                "treatment": ["Mancozeb or iprodione fungicide every 7–10 days", "Remove infected leaves"],
                "prevention": ["Certified disease-free sets/seeds", "Avoid overhead irrigation", "Proper crop rotation"],
                "recovery": "14–21 days",
            },
            "Downy Mildew": {
                "pathogen": "Peronospora destructor (oomycete)",
                "severity": "High",
                "symptoms": ["Pale green to violet furry sporulation on leaves", "Leaves turn yellow then collapse", "Plants appear as if frosted", "Secondary infections cause rapid field spread"],
                "treatment": ["Metalaxyl + mancozeb systemic fungicide", "Remove infected plants"],
                "prevention": ["Avoid overhead irrigation", "Good field drainage", "Wider spacing"],
                "recovery": "14–28 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Upright green healthy tops", "Firm well-formed bulbs"],
                "treatment": ["Timely irrigation and sulphur or potassium fertilisation"],
                "prevention": ["Scout for thrips — major virus vector"],
                "recovery": "N/A",
            },
        },
    },
}

# ── Farming chatbot knowledge base ────────────────────────────────────────────
FARMING_KB = [
    {
        "keys": ["fertilizer", "fertiliser", "npk", "nitrogen", "phosphorus", "potassium", "nutrient", "manure", "compost", "top dress", "basal"],
        "answer": "**Fertiliser Guidance 🌱**\n\n**Basal application (at planting):**\n- DAP (18-46-0) or NPK (17-17-17) at 50–150 kg/ha\n- Mix well into soil before planting\n\n**Top dressing (4–6 weeks after planting):**\n- CAN or Urea at 50–100 kg/ha when soil is moist\n\n**Organic alternatives:**\n- Well-composted manure: 5–10 tonnes/ha at planting\n- Vermicompost: 2–3 tonnes/ha\n\n**Micronutrient tip:** Yellowing between veins = magnesium or iron deficiency → foliar spray with MgSO₄ or chelated iron.",
    },
    {
        "keys": ["irrigation", "water", "watering", "drought", "dry season", "moisture", "drip"],
        "answer": "**Irrigation & Water Management 💧**\n\n**Rules:**\n- Water deeply and infrequently rather than shallowly and often\n- Morning irrigation reduces fungal disease risk vs evening\n- Drip irrigation saves 30–50% water and keeps leaves dry\n\n**Crop water needs (mm/week):**\n- Tomato: 25–35 | Maize: 20–30 | Beans: 15–20\n- Rice: 30–40 | Sugarcane: 35–50\n\n**Drought signs:**\n- Morning wilting = severe stress → irrigate immediately\n- Leaf curl without wilting = early stress → irrigate within 24h",
    },
    {
        "keys": ["pest", "insect", "bug", "aphid", "whitefly", "caterpillar", "worm", "spider mite", "thrips", "borer"],
        "answer": "**Pest Management (IPM) 🐛**\n\n1. **Monitor** twice a week — scout before spraying\n2. **Biological control first:**\n   - Bt (Bacillus thuringiensis) for caterpillars\n   - Neem oil (5 ml/L) for soft-bodied insects\n   - Predatory insects (ladybirds, lacewings)\n3. **Chemical control (last resort):**\n   - Aphids/whiteflies: imidacloprid or acetamiprid\n   - Caterpillars: lambda-cyhalothrin or spinosad\n   - Spider mites: abamectin or bifenazate\n\n**Trap crops:** Plant sunflower or maize borders to draw pests away from main crop.",
    },
    {
        "keys": ["prevent", "prevention", "protect", "disease management", "spray schedule", "fungicide"],
        "answer": "**Disease Prevention Protocol 🛡️**\n\n**Cultural practices:**\n- Rotate crops every 2–3 seasons\n- Remove and destroy crop debris after harvest\n- Use certified disease-free seeds and planting material\n- Maintain proper plant spacing for air circulation\n\n**Preventive spray schedule:**\n- Begin at start of rainy season\n- Spray every 7–14 days during high-risk periods\n- Alternate fungicide modes of action to prevent resistance\n\n**Farm hygiene:**\n- Disinfect tools with 70% alcohol or 10% bleach\n- Wash hands before handling healthy plants",
    },
    {
        "keys": ["harvest", "yield", "maturity", "when to harvest", "post-harvest", "storage"],
        "answer": "**Harvest & Storage Tips 🌾**\n\n**Maturity signs:**\n- Maize: silks brown, husk dry, kernel doughy\n- Tomato: full colour change, firm to soft\n- Beans: pod yellow-brown, seeds rattle\n- Potato: vines die back, skin sets firmly\n\n**Post-harvest:**\n- Handle gently to prevent bruising\n- Cool produce quickly after harvest\n- Sort out damaged/diseased produce immediately\n\n**Storage:**\n- Cool (10–15°C), dry, well-ventilated spaces\n- Maize: dry to <13% moisture before storage\n- Potatoes: store in dark to prevent greening",
    },
    {
        "keys": ["soil", "ph", "lime", "acidity", "clay", "sandy", "loam", "organic matter"],
        "answer": "**Soil Management 🏔️**\n\n**Ideal pH by crop:**\n- Maize: 5.8–7.0 | Tomato: 6.0–6.8 | Beans: 6.0–7.0\n- Potato: 5.0–6.5 | Rice: 5.5–7.0 | Banana: 5.5–7.0\n\n**Correcting acidic soil (pH <5.5):**\n- Apply agricultural lime: 1–3 tonnes/ha\n- Apply 3–6 months before planting\n- Dolomitic lime also adds Mg\n\n**Improving structure:**\n- Add organic matter (compost/manure) annually\n- Minimum tillage protects soil structure\n- Cover crops (mucuna, dolichos) fix nitrogen",
    },
    {
        "keys": ["weather", "rain", "temperature", "season", "climate", "flood", "frost"],
        "answer": "**Weather & Climate Adaptation 🌤️**\n\n**Adapting to weather:**\n- Dry spells: Mulch 5–10 cm deep to retain moisture\n- Excessive rain: Improve drainage; spray preventive fungicide\n- High temperatures: Shade nets for tomato, pepper\n\n**Climate-smart practices:**\n- Stagger planting dates to spread risk\n- Use drought-tolerant varieties in erratic rainfall areas\n- Plant windbreaks (Grevillea, Leucaena) to reduce wind damage\n\n**Disease weather alert:**\n- 2+ days of high humidity + temps 20–25°C → high blight risk\n- Spray preventive fungicide before and after rain events",
    },
]

SEVERITY_CLASS = {
    "None": "sev-none",
    "Low": "sev-low",
    "Low-Medium": "sev-low",
    "Medium": "sev-medium",
    "Medium-High": "sev-medium",
    "High": "sev-high",
    "Very High": "sev-vhigh",
}

SEVERITY_COLOR_HEX = {
    "None": "#4ade80",
    "Low": "#22c55e",
    "Low-Medium": "#22c55e",
    "Medium": "#fbbf24",
    "Medium-High": "#f97316",
    "High": "#f97316",
    "Very High": "#f85149",
}

SEVERITY_BAR_PCT = {
    "None": 5, "Low": 15, "Low-Medium": 30,
    "Medium": 50, "Medium-High": 65,
    "High": 80, "Very High": 100,
}


def get_bot_response(query: str) -> str:
    q = query.lower()
    for item in FARMING_KB:
        if any(kw in q for kw in item["keys"]):
            return item["answer"]
    # Crop-specific lookup
    for crop, info in DISEASE_DB.items():
        if crop.lower() in q:
            lines = [f"**{info['icon']} {crop} Disease Guide**\n"]
            for d, dinfo in info["diseases"].items():
                if d == "Healthy":
                    continue
                lines.append(f"• **{d}** — Severity: {dinfo['severity']}")
            lines.append("\n💡 Upload a leaf photo on the **🔬 Detect Disease** page for instant AI diagnosis!")
            return "\n".join(lines)
    return (
        "**AI Farming Assistant 🤖**\n\n"
        "I can help you with:\n"
        "- 🌱 Fertiliser guidance\n"
        "- 💧 Irrigation management\n"
        "- 🐛 Pest control (IPM)\n"
        "- 🛡️ Disease prevention\n"
        "- 🌾 Harvest & storage\n"
        "- 🏔️ Soil management\n"
        "- 🌤️ Weather & seasonal advice\n"
        "- Specific crop diseases (just mention the crop name)\n\n"
        "Type your question in plain English or Swahili!"
    )
