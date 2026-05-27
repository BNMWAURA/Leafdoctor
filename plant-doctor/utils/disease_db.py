"""
Comprehensive disease knowledge base for 13 supported crops.
Each entry: symptoms, causes, treatment, prevention, severity.
"""

DISEASE_DB: dict = {
    "Tomato": {
        "icon": "🍅",
        "diseases": {
            "Early Blight": {
                "pathogen": "Alternaria solani (fungus)",
                "severity": "Medium",
                "symptoms": [
                    "Dark brown spots with concentric rings (target-board pattern)",
                    "Yellow halo surrounding lesions",
                    "Lower leaves affected first",
                    "Lesions merge causing leaf death",
                ],
                "causes": ["High humidity", "Warm temperatures 24–29°C", "Leaf wetness"],
                "treatment": [
                    "Apply chlorothalonil or mancozeb fungicide every 7–10 days",
                    "Remove and destroy infected leaves immediately",
                    "Apply copper-based fungicide as organic option",
                ],
                "prevention": [
                    "Use certified disease-free seeds",
                    "Rotate crops every 2–3 years",
                    "Avoid overhead irrigation",
                    "Improve air circulation with proper spacing",
                ],
                "recovery_days": "14–21 days with treatment",
            },
            "Late Blight": {
                "pathogen": "Phytophthora infestans (oomycete)",
                "severity": "High",
                "symptoms": [
                    "Water-soaked, irregular greenish-grey spots",
                    "White mouldy growth on leaf undersides",
                    "Rapid browning and death of leaves",
                    "Dark brown streaks on stems",
                ],
                "causes": ["Cool temperatures 10–20°C", "High humidity >90%", "Prolonged leaf wetness"],
                "treatment": [
                    "Apply metalaxyl or cymoxanil fungicides immediately",
                    "Remove all infected plant material",
                    "Use fosetyl-aluminium as preventive spray",
                ],
                "prevention": [
                    "Plant resistant varieties (e.g. Legend, Mountain Magic)",
                    "Avoid planting near potatoes",
                    "Apply preventive copper fungicide during wet seasons",
                    "Stake plants for better air circulation",
                ],
                "recovery_days": "7–14 days if caught early",
            },
            "Leaf Miner": {
                "pathogen": "Liriomyza spp. (insect)",
                "severity": "Low-Medium",
                "symptoms": [
                    "Winding white or yellow tunnels (mines) on leaf surface",
                    "Small white stippling dots on leaves",
                    "Premature leaf drop",
                ],
                "causes": ["Adult flies lay eggs in leaf tissue", "Warm dry conditions favour infestation"],
                "treatment": [
                    "Apply spinosad or abamectin insecticide",
                    "Remove heavily infested leaves",
                    "Introduce parasitic wasps (Diglyphus isaea) as biocontrol",
                ],
                "prevention": [
                    "Use yellow sticky traps to monitor adult flies",
                    "Install fine mesh netting over seedbeds",
                    "Avoid over-application of nitrogen fertiliser",
                ],
                "recovery_days": "10–14 days with treatment",
            },
            "Bacterial Spot": {
                "pathogen": "Xanthomonas campestris (bacterium)",
                "severity": "Medium-High",
                "symptoms": [
                    "Small water-soaked spots turning dark brown",
                    "Yellow halo around lesions",
                    "Spots on fruit causing scab-like lesions",
                    "Leaf distortion and drop",
                ],
                "causes": ["Warm wet weather", "Splashing rain", "Infected seeds or transplants"],
                "treatment": [
                    "Apply copper hydroxide bactericide",
                    "Use streptomycin sulfate spray",
                    "Remove infected plant debris",
                ],
                "prevention": [
                    "Use disease-free certified seeds",
                    "Avoid working in field when plants are wet",
                    "Rotate crops with non-solanaceous plants",
                ],
                "recovery_days": "21–28 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["No visible disease symptoms", "Green, vibrant leaves", "Normal growth"],
                "causes": [],
                "treatment": ["Continue regular crop management"],
                "prevention": ["Maintain good agricultural practices", "Regular scouting"],
                "recovery_days": "N/A",
            },
        },
    },

    "Maize": {
        "icon": "🌽",
        "diseases": {
            "Northern Leaf Blight": {
                "pathogen": "Exserohilum turcicum (fungus)",
                "severity": "High",
                "symptoms": [
                    "Long elliptical grey-green to tan lesions on leaves",
                    "Lesions 2.5–15 cm long",
                    "Dark spores visible in lesion centres",
                    "Lower leaves infected first",
                ],
                "causes": ["Moderate temperatures 18–27°C", "High humidity", "Extended leaf wetness"],
                "treatment": [
                    "Apply propiconazole or azoxystrobin fungicide",
                    "Spray at tassel emergence for maximum protection",
                ],
                "prevention": [
                    "Plant resistant hybrids",
                    "Crop rotation with non-grass crops",
                    "Bury crop residue after harvest",
                ],
                "recovery_days": "14–21 days",
            },
            "Gray Leaf Spot": {
                "pathogen": "Cercospora zeae-maydis (fungus)",
                "severity": "High",
                "symptoms": [
                    "Rectangular pale grey lesions bounded by leaf veins",
                    "Lesions run parallel to leaf margins",
                    "Premature leaf death in severe cases",
                ],
                "causes": ["High humidity", "Warm temperatures 25–30°C", "Reduced air circulation"],
                "treatment": [
                    "Fungicide applications of strobilurin or triazole",
                    "Apply at early disease detection stage",
                ],
                "prevention": [
                    "Use tolerant hybrids",
                    "Minimum tillage to reduce residue",
                    "Adequate plant spacing",
                ],
                "recovery_days": "14–28 days",
            },
            "Common Rust": {
                "pathogen": "Puccinia sorghi (fungus)",
                "severity": "Medium",
                "symptoms": [
                    "Small oval brick-red pustules on both leaf surfaces",
                    "Pustules rupture releasing powdery rust-red spores",
                    "Severe infection causes yellowing",
                ],
                "causes": ["Cool temperatures 16–23°C", "High humidity", "Wind-dispersed spores"],
                "treatment": [
                    "Fungicide (mancozeb, propiconazole) at first sign",
                    "Remove badly infected leaves",
                ],
                "prevention": [
                    "Plant rust-resistant varieties",
                    "Early planting to escape peak rust season",
                ],
                "recovery_days": "10–14 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["No visible disease symptoms", "Deep green leaves", "Normal growth"],
                "causes": [],
                "treatment": ["Maintain regular fertilisation schedule"],
                "prevention": ["Scout regularly during humid periods"],
                "recovery_days": "N/A",
            },
        },
    },

    "Potato": {
        "icon": "🥔",
        "diseases": {
            "Early Blight": {
                "pathogen": "Alternaria solani (fungus)",
                "severity": "Medium",
                "symptoms": [
                    "Dark brown circular lesions with concentric rings",
                    "Yellow halo around lesions",
                    "Older leaves affected first",
                    "Defoliation under severe conditions",
                ],
                "causes": ["Warm temperatures 24–29°C", "High humidity", "Plant stress"],
                "treatment": [
                    "Apply chlorothalonil or mancozeb fungicide",
                    "Spray every 7–10 days during wet weather",
                ],
                "prevention": [
                    "Use certified disease-free seed tubers",
                    "Avoid water stress",
                    "Rotate with non-solanaceous crops",
                ],
                "recovery_days": "14–21 days",
            },
            "Late Blight": {
                "pathogen": "Phytophthora infestans (oomycete)",
                "severity": "Very High",
                "symptoms": [
                    "Water-soaked pale green to brown leaf spots",
                    "White sporulation on leaf undersides",
                    "Rapid collapse of foliage",
                    "Brown rot in tubers",
                ],
                "causes": ["Cool wet weather", "Temperatures 10–20°C with humidity >90%"],
                "treatment": [
                    "Metalaxyl-M or cymoxanil + mancozeb fungicide",
                    "Remove and destroy infected foliage immediately",
                    "Destroy infected tubers — do not compost",
                ],
                "prevention": [
                    "Plant resistant varieties",
                    "Apply preventive copper sprays in wet seasons",
                    "Hill soil around plants to protect tubers",
                ],
                "recovery_days": "10–14 days if treated early",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy dark green foliage", "No lesions or discolouration"],
                "causes": [],
                "treatment": ["Regular hilling and irrigation management"],
                "prevention": ["Monitor for Colorado beetle and aphid vectors"],
                "recovery_days": "N/A",
            },
        },
    },

    "Coffee": {
        "icon": "☕",
        "diseases": {
            "Leaf Rust": {
                "pathogen": "Hemileia vastatrix (fungus)",
                "severity": "Very High",
                "symptoms": [
                    "Yellow-orange powdery spots on leaf undersides",
                    "Corresponding pale yellow areas on upper leaf surface",
                    "Premature leaf drop",
                    "Branch dieback in severe cases",
                ],
                "causes": ["Temperatures 21–25°C", "High humidity", "Extended rainfall"],
                "treatment": [
                    "Apply triazole fungicides (propiconazole, tebuconazole)",
                    "Copper-based fungicides as organic option",
                    "Foliar spray at 6–8 week intervals",
                ],
                "prevention": [
                    "Plant resistant varieties (Catimor, Ruiru 11)",
                    "Prune to improve canopy air circulation",
                    "Balanced fertilisation — avoid excess nitrogen",
                ],
                "recovery_days": "21–30 days",
            },
            "Berry Borer": {
                "pathogen": "Hypothenemus hampei (insect)",
                "severity": "High",
                "symptoms": [
                    "Small circular entry holes in coffee berries",
                    "Premature berry drop",
                    "Discolouration inside affected berries",
                ],
                "causes": ["Adult female beetles bore into berries", "Year-round in tropical climates"],
                "treatment": [
                    "Apply endosulfan or spinetoram insecticide",
                    "Use Beauveria bassiana (biological control)",
                    "Harvest all ripe berries promptly",
                ],
                "prevention": [
                    "Regular harvesting to remove all ripe/overripe berries",
                    "Strip picking at season end",
                    "Use berry borer traps with attractant",
                ],
                "recovery_days": "Ongoing management required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Deep green glossy leaves", "No lesions or powder"],
                "causes": [],
                "treatment": ["Continue regular shade management and fertilisation"],
                "prevention": ["Scout weekly during rainy season"],
                "recovery_days": "N/A",
            },
        },
    },

    "Banana": {
        "icon": "🍌",
        "diseases": {
            "Black Sigatoka": {
                "pathogen": "Mycosphaerella fijiensis (fungus)",
                "severity": "Very High",
                "symptoms": [
                    "Small yellow streaks on leaf surface",
                    "Streaks enlarge to dark brown-black elliptical lesions",
                    "Lesions with grey centre and yellow halo",
                    "Premature leaf death causing significant yield loss",
                ],
                "causes": ["High humidity >80%", "Temperatures 25–28°C", "Rainfall"],
                "treatment": [
                    "Systemic fungicides: propiconazole, tridemorph",
                    "Oil-based sprays to reduce humidity on leaves",
                    "Regular leaf stripping of infected material",
                ],
                "prevention": [
                    "Use tolerant varieties (FHIA hybrids)",
                    "Remove and destroy infected leaf portions",
                    "Adequate spacing for air circulation",
                ],
                "recovery_days": "21–35 days with intensive management",
            },
            "Panama Disease": {
                "pathogen": "Fusarium oxysporum f.sp. cubense (fungus)",
                "severity": "Very High",
                "symptoms": [
                    "Yellowing of older outer leaves",
                    "Wilting and collapse of leaf petioles",
                    "Brown-red discolouration inside pseudostem",
                    "Plant death — no recovery possible",
                ],
                "causes": ["Soil-borne pathogen", "Infested soil or water", "Infected planting material"],
                "treatment": [
                    "No effective chemical cure — remove and destroy infected plants",
                    "Drench soil with fungicide to reduce spread",
                    "Quarantine affected area immediately",
                ],
                "prevention": [
                    "Plant Cavendish or TR4-resistant varieties",
                    "Use certified disease-free tissue culture plants",
                    "Avoid movement of soil from infected areas",
                    "Disinfect tools with 10% bleach solution",
                ],
                "recovery_days": "Not recoverable — field replanting required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Bright green upright leaves", "No streaks or browning"],
                "causes": [],
                "treatment": ["Regular sucker management and fertilisation"],
                "prevention": ["Inspect new planting material for disease signs"],
                "recovery_days": "N/A",
            },
        },
    },

    "Beans": {
        "icon": "🫘",
        "diseases": {
            "Angular Leaf Spot": {
                "pathogen": "Phaeoisariopsis griseola (fungus)",
                "severity": "High",
                "symptoms": [
                    "Angular brown lesions bounded by leaf veins",
                    "Grey sporulation on leaf undersides",
                    "Lesions coalesce causing leaf death",
                    "Water-soaked spots on pods",
                ],
                "causes": ["High humidity", "Temperatures 16–28°C", "Splash dispersal"],
                "treatment": [
                    "Mancozeb or chlorothalonil fungicide spray",
                    "Remove infected leaves and debris",
                ],
                "prevention": [
                    "Resistant varieties (CAL 96, CIAT breeding lines)",
                    "Crop rotation every 2 years",
                    "Avoid overhead irrigation",
                ],
                "recovery_days": "14–21 days",
            },
            "Bean Rust": {
                "pathogen": "Uromyces appendiculatus (fungus)",
                "severity": "Medium-High",
                "symptoms": [
                    "Brown powdery pustules on leaves",
                    "Yellow halo around pustules",
                    "Severe defoliation if untreated",
                ],
                "causes": ["Moderate temperatures 17–27°C", "High humidity"],
                "treatment": [
                    "Triadimefon or mancozeb fungicide",
                    "Apply at first pustule appearance",
                ],
                "prevention": [
                    "Resistant varieties",
                    "Wider plant spacing",
                    "Avoid planting during peak rust season",
                ],
                "recovery_days": "14–21 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Uniform green leaves", "No spots or pustules"],
                "causes": [],
                "treatment": ["Regular weeding and balanced NPK fertilisation"],
                "prevention": ["Scout during humid, rainy periods"],
                "recovery_days": "N/A",
            },
        },
    },

    "Cassava": {
        "icon": "🪴",
        "diseases": {
            "Cassava Mosaic Disease": {
                "pathogen": "Cassava mosaic begomoviruses (virus, whitefly-vectored)",
                "severity": "Very High",
                "symptoms": [
                    "Mosaic yellow-green mottling on leaves",
                    "Leaf distortion and stunting",
                    "Reduced tuber yield by up to 95%",
                ],
                "causes": ["Whitefly (Bemisia tabaci) transmission", "Infected cuttings"],
                "treatment": [
                    "No direct cure — rogue out infected plants",
                    "Control whitefly vectors with imidacloprid or neem oil",
                ],
                "prevention": [
                    "Use virus-free certified cuttings",
                    "Plant CMD-resistant varieties (e.g. NASE series)",
                    "Inspect planting material carefully",
                    "Control whitefly populations",
                ],
                "recovery_days": "Plant removal required — not recoverable",
            },
            "Cassava Brown Streak Disease": {
                "pathogen": "Cassava brown streak viruses (virus)",
                "severity": "Very High",
                "symptoms": [
                    "Yellowish chlorosis on leaves along veins",
                    "Brown necrotic streaks on stems",
                    "Severe brown rot in tubers (roots)",
                    "Tubers become inedible",
                ],
                "causes": ["Whitefly transmission", "Infected planting material"],
                "treatment": [
                    "Remove and destroy infected plants",
                    "Control whitefly populations urgently",
                ],
                "prevention": [
                    "Use CBSD-tolerant varieties",
                    "Source certified clean cuttings",
                    "Rogue symptomatic plants early",
                ],
                "recovery_days": "Not recoverable — field management required",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy green leaves", "No mosaic or streaks"],
                "causes": [],
                "treatment": ["Maintain soil fertility with organic manure"],
                "prevention": ["Monitor for whitefly populations weekly"],
                "recovery_days": "N/A",
            },
        },
    },

    "Wheat": {
        "icon": "🌾",
        "diseases": {
            "Wheat Rust (Stem Rust)": {
                "pathogen": "Puccinia graminis (fungus)",
                "severity": "Very High",
                "symptoms": [
                    "Brick-red oval pustules on stems and leaves",
                    "Pustules rupture releasing reddish spores",
                    "Stem weakening leading to lodging",
                    "Premature grain shrivelling",
                ],
                "causes": ["Temperatures 15–35°C", "High humidity", "Wind-dispersed spores"],
                "treatment": [
                    "Triazole fungicides (propiconazole, tebuconazole)",
                    "Apply at first sign of disease",
                ],
                "prevention": [
                    "Plant resistant varieties (e.g. DRRW 7, Kakamega series)",
                    "Early planting to avoid peak rust season",
                    "Destroy volunteer wheat plants",
                ],
                "recovery_days": "7–14 days with early treatment",
            },
            "Powdery Mildew": {
                "pathogen": "Blumeria graminis f.sp. tritici (fungus)",
                "severity": "Medium",
                "symptoms": [
                    "White powdery patches on upper leaf surfaces",
                    "Patches enlarge covering entire leaf",
                    "Yellow-brown tissue beneath patches",
                ],
                "causes": ["Moderate temperatures 15–22°C", "High humidity but dry leaf surface", "Dense canopy"],
                "treatment": [
                    "Triazole or strobilurin fungicide",
                    "Sulphur-based fungicide as organic option",
                ],
                "prevention": [
                    "Resistant varieties",
                    "Reduce seeding rate for better ventilation",
                    "Avoid excessive nitrogen",
                ],
                "recovery_days": "10–14 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Upright green healthy tillers", "No lesions or powder"],
                "causes": [],
                "treatment": ["Timely top-dressing with nitrogen at tillering"],
                "prevention": ["Scout 3× per season: seedling, tillering, heading"],
                "recovery_days": "N/A",
            },
        },
    },

    "Rice": {
        "icon": "🌾",
        "diseases": {
            "Rice Blast": {
                "pathogen": "Magnaporthe oryzae (fungus)",
                "severity": "Very High",
                "symptoms": [
                    "Diamond-shaped lesions with grey centre and brown border",
                    "Neck rot at panicle base (neck blast)",
                    "Collar rot killing tillers",
                    "Whitehead symptom — empty panicles",
                ],
                "causes": ["Temperatures 20–28°C", "High humidity", "Excess nitrogen"],
                "treatment": [
                    "Tricyclazole or isoprothiolane fungicide",
                    "Spray at panicle initiation and heading",
                ],
                "prevention": [
                    "Resistant varieties (NERICA, IR64-blast resistant)",
                    "Balanced nitrogen — avoid over-application",
                    "Silicon application to strengthen cell walls",
                ],
                "recovery_days": "10–14 days with treatment",
            },
            "Bacterial Leaf Blight": {
                "pathogen": "Xanthomonas oryzae pv. oryzae (bacterium)",
                "severity": "High",
                "symptoms": [
                    "Water-soaked to yellowish stripes along leaf margins",
                    "Lesions extend to entire leaf",
                    "Milky bacterial ooze from cut tissue",
                    "Kresek symptom — wilting of young tillers",
                ],
                "causes": ["Flood water spread", "Warm temperatures 25–35°C", "High nitrogen"],
                "treatment": [
                    "Copper-based bactericide spray",
                    "Drain flooded fields to reduce spread",
                ],
                "prevention": [
                    "Resistant varieties",
                    "Avoid excessive nitrogen fertilisation",
                    "Use clean irrigation water",
                ],
                "recovery_days": "21–28 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Healthy upright tillers", "Green leaves without lesions"],
                "causes": [],
                "treatment": ["Regular water management and weeding"],
                "prevention": ["Scout especially after heavy rain or flooding"],
                "recovery_days": "N/A",
            },
        },
    },

    "Sugarcane": {
        "icon": "🎋",
        "diseases": {
            "Red Rot": {
                "pathogen": "Colletotrichum falcatum (fungus)",
                "severity": "High",
                "symptoms": [
                    "Red discolouration inside cane stalks",
                    "White patches alternating with red tissue",
                    "Sour fermented smell from infected stalks",
                    "Wilting and yellowing of leaves",
                ],
                "causes": ["Warm humid conditions", "Waterlogging", "Infected setts"],
                "treatment": [
                    "No effective field treatment — remove infected stalks",
                    "Treat setts with hot water (50°C, 30 min)",
                    "Fungicidal sett treatment with carbendazim",
                ],
                "prevention": [
                    "Plant resistant varieties",
                    "Use disease-free planting material",
                    "Improve field drainage",
                ],
                "recovery_days": "Not recoverable in severe cases",
            },
            "Smut": {
                "pathogen": "Sporisorium scitamineum (fungus)",
                "severity": "High",
                "symptoms": [
                    "Characteristic whip-like black structure from growing point",
                    "Thin grass-like shoots with black spores",
                    "Stunted growth",
                ],
                "causes": ["Soil-borne spores", "Infected setts", "Warm dry conditions"],
                "treatment": [
                    "Rogue and destroy infected stools",
                    "Hot water treatment of setts",
                ],
                "prevention": [
                    "Resistant varieties",
                    "Certified disease-free planting material",
                ],
                "recovery_days": "Not recoverable",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Tall vigorous canes", "Healthy green leaves"],
                "causes": [],
                "treatment": ["Split nitrogen application for optimal yield"],
                "prevention": ["Inspect ratoon crops for smut whips each season"],
                "recovery_days": "N/A",
            },
        },
    },

    "Pepper": {
        "icon": "🌶️",
        "diseases": {
            "Anthracnose": {
                "pathogen": "Colletotrichum spp. (fungus)",
                "severity": "High",
                "symptoms": [
                    "Circular water-soaked lesions on fruit",
                    "Lesions turn black with concentric rings",
                    "Salmon-coloured spore masses in lesion centres",
                    "Fruit rot and collapse",
                ],
                "causes": ["Warm humid weather", "Rain splash dispersal", "Temperatures 20–30°C"],
                "treatment": [
                    "Mancozeb or azoxystrobin fungicide",
                    "Copper-based fungicide for organic approach",
                    "Remove and destroy infected fruit",
                ],
                "prevention": [
                    "Plant resistant varieties",
                    "Avoid overhead irrigation",
                    "Harvest fruit promptly at maturity",
                ],
                "recovery_days": "14–21 days",
            },
            "Bacterial Wilt": {
                "pathogen": "Ralstonia solanacearum (bacterium)",
                "severity": "Very High",
                "symptoms": [
                    "Sudden wilting of entire plant",
                    "Wilting without yellowing initially",
                    "Brown discolouration inside stem",
                    "Bacterial ooze from cut stem in water",
                ],
                "causes": ["Soil-borne bacterium", "Warm temperatures >25°C", "Wet conditions"],
                "treatment": [
                    "No effective chemical cure",
                    "Remove and destroy infected plants",
                    "Drench surrounding soil with copper bactericide",
                ],
                "prevention": [
                    "Resistant varieties",
                    "Grafting onto resistant rootstocks",
                    "Strict crop rotation (4+ years)",
                    "Avoid waterlogged soils",
                ],
                "recovery_days": "Not recoverable",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Dark green leaves", "Firm healthy fruit"],
                "causes": [],
                "treatment": ["Consistent calcium and potassium application to prevent blossom end rot"],
                "prevention": ["Scout weekly for spider mites and aphids"],
                "recovery_days": "N/A",
            },
        },
    },

    "Mango": {
        "icon": "🥭",
        "diseases": {
            "Powdery Mildew": {
                "pathogen": "Oidium mangiferae (fungus)",
                "severity": "High",
                "symptoms": [
                    "White powdery growth on young leaves, flowers, and fruits",
                    "Flower drop causing yield loss",
                    "Young fruits with powdery coating drop prematurely",
                    "Leaf distortion in severe cases",
                ],
                "causes": ["Cool temperatures 10–20°C at flowering", "Dry weather with high humidity at night"],
                "treatment": [
                    "Wettable sulphur spray at 2 g/L",
                    "Difenoconazole or hexaconazole systemic fungicide",
                    "Spray at 80% bud burst, full bloom, and fruitlet stage",
                ],
                "prevention": [
                    "Prune for canopy aeration",
                    "Spray preventively at bud burst",
                    "Avoid excessive irrigation near flowering",
                ],
                "recovery_days": "7–14 days",
            },
            "Anthracnose": {
                "pathogen": "Colletotrichum gloeosporioides (fungus)",
                "severity": "High",
                "symptoms": [
                    "Dark brown to black irregular spots on leaves",
                    "Leaf tip and margin browning",
                    "Black sunken lesions on mature fruit",
                    "Post-harvest fruit rot",
                ],
                "causes": ["High humidity", "Warm temperatures 25–30°C", "Rain splash"],
                "treatment": [
                    "Mancozeb + copper oxychloride mixture",
                    "Post-harvest hot water treatment (52°C, 5 min)",
                    "Propiconazole pre-harvest spray",
                ],
                "prevention": [
                    "Remove and destroy infected plant material",
                    "Avoid overhead irrigation",
                    "Regular canopy pruning",
                ],
                "recovery_days": "14–21 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Dark glossy green leaves", "Normal flower and fruit development"],
                "causes": [],
                "treatment": ["Foliar micronutrient spray at flowering for better fruit set"],
                "prevention": ["Scout for mango hoppers (Idioscopus spp.) during flowering"],
                "recovery_days": "N/A",
            },
        },
    },

    "Onion": {
        "icon": "🧅",
        "diseases": {
            "Purple Blotch": {
                "pathogen": "Alternaria porri (fungus)",
                "severity": "Medium-High",
                "symptoms": [
                    "Small white lesions with purple centres on leaves",
                    "Lesions enlarge with concentric zones",
                    "Leaf tips die back",
                    "Dark brown rot on bulb necks",
                ],
                "causes": ["Warm temperatures 21–30°C", "High humidity", "Overhead irrigation"],
                "treatment": [
                    "Mancozeb or iprodione fungicide every 7–10 days",
                    "Remove infected leaves",
                ],
                "prevention": [
                    "Certified disease-free sets/seeds",
                    "Avoid overhead irrigation",
                    "Proper crop rotation",
                ],
                "recovery_days": "14–21 days",
            },
            "Downy Mildew": {
                "pathogen": "Peronospora destructor (oomycete)",
                "severity": "High",
                "symptoms": [
                    "Pale green to violet furry sporulation on leaves",
                    "Leaves turn yellow then collapse",
                    "Plants appear as if frosted",
                    "Secondary infections cause rapid field spread",
                ],
                "causes": ["Cool moist conditions", "Temperatures 13–20°C", "Dew and fog"],
                "treatment": [
                    "Metalaxyl + mancozeb systemic fungicide",
                    "Remove infected plants",
                ],
                "prevention": [
                    "Avoid overhead irrigation",
                    "Good field drainage",
                    "Wider spacing",
                ],
                "recovery_days": "14–28 days",
            },
            "Healthy": {
                "pathogen": "None",
                "severity": "None",
                "symptoms": ["Upright green healthy tops", "Firm well-formed bulbs"],
                "causes": [],
                "treatment": ["Timely irrigation and sulphur or potassium fertilisation"],
                "prevention": ["Scout for thrips — major virus vector"],
                "recovery_days": "N/A",
            },
        },
    },
}

FARMING_KB: dict = {
    "fertilizer": {
        "keywords": ["fertilizer", "fertiliser", "npk", "nitrogen", "phosphorus", "potassium", "nutrient", "manure", "compost"],
        "answer": (
            "**Fertiliser Guidance 🌱**\n\n"
            "**Basal application (at planting):**\n"
            "- Apply DAP (18-46-0) or NPK (17-17-17) at 50–150 kg/ha depending on crop\n"
            "- Mix well with soil before planting\n\n"
            "**Top dressing (4–6 weeks after planting):**\n"
            "- Use CAN (Calcium Ammonium Nitrate) or Urea at 50–100 kg/ha\n"
            "- Apply when soil is moist, avoid during drought\n\n"
            "**Organic alternatives:**\n"
            "- Well-composted manure: 5–10 tonnes/ha at planting\n"
            "- Vermicompost: 2–3 tonnes/ha\n"
            "- Green manure: incorporate legume biomass before main crop\n\n"
            "**Micronutrient tip:** Yellowing between veins often signals magnesium or iron deficiency — use foliar spray (MgSO₄ or chelated iron)."
        ),
    },
    "irrigation": {
        "keywords": ["irrigation", "water", "watering", "drought", "dry", "moisture", "drip"],
        "answer": (
            "**Irrigation & Water Management 💧**\n\n"
            "**General rules:**\n"
            "- Water deeply and infrequently rather than shallowly and often\n"
            "- Morning irrigation reduces fungal disease risk compared to evening\n"
            "- Drip irrigation saves 30–50% water and keeps leaves dry\n\n"
            "**Crop water requirements (mm/week):**\n"
            "- Tomato: 25–35 mm | Maize: 20–30 mm | Beans: 15–20 mm\n"
            "- Rice: 30–40 mm | Sugarcane: 35–50 mm\n\n"
            "**Drought signs:**\n"
            "- Wilting in morning = severe stress — irrigate immediately\n"
            "- Leaf curl without wilting = early stress — irrigate within 24h\n\n"
            "**Waterlogging prevention:**\n"
            "- Create raised beds or ridges in flood-prone areas\n"
            "- Install field drains before rainy season"
        ),
    },
    "pest": {
        "keywords": ["pest", "insect", "bug", "aphid", "whitefly", "caterpillar", "worm", "spider mite", "thrips", "borer"],
        "answer": (
            "**Pest Management 🐛**\n\n"
            "**Integrated Pest Management (IPM) approach:**\n\n"
            "1. **Monitor regularly** — scout fields twice a week\n"
            "2. **Economic threshold** — only spray when pest numbers exceed threshold\n"
            "3. **Biological control first:**\n"
            "   - Introduce predatory insects (ladybirds, lacewings)\n"
            "   - Use Bacillus thuringiensis (Bt) for caterpillars\n"
            "   - Neem oil (5 ml/L) for soft-bodied insects\n"
            "4. **Chemical control (last resort):**\n"
            "   - Aphids/whiteflies: imidacloprid or acetamiprid\n"
            "   - Caterpillars: lambda-cyhalothrin or spinosad\n"
            "   - Spider mites: abamectin or bifenazate\n\n"
            "**Trap crops:** Plant sunflower or maize borders to attract pests away from main crop."
        ),
    },
    "disease_prevention": {
        "keywords": ["prevent", "prevention", "avoid", "protect", "healthy crop", "disease management"],
        "answer": (
            "**General Disease Prevention 🛡️**\n\n"
            "**Cultural practices:**\n"
            "- Rotate crops every 2–3 seasons — breaks disease cycles\n"
            "- Remove and destroy crop debris after harvest\n"
            "- Use certified disease-free seeds and planting material\n"
            "- Maintain proper plant spacing for air circulation\n\n"
            "**Preventive spraying schedule:**\n"
            "- Begin preventive fungicide sprays at start of rainy season\n"
            "- Spray every 7–14 days during high-risk periods\n"
            "- Alternate fungicide modes of action to prevent resistance\n\n"
            "**Farm hygiene:**\n"
            "- Disinfect tools with 70% alcohol or 10% bleach between plants\n"
            "- Wash hands before handling healthy plants after touching diseased ones\n"
            "- Control weeds — they host many pests and diseases"
        ),
    },
    "harvest": {
        "keywords": ["harvest", "yield", "maturity", "when to harvest", "post-harvest", "storage"],
        "answer": (
            "**Harvest & Post-Harvest Tips 🌾**\n\n"
            "**Maturity indicators by crop:**\n"
            "- Maize: silks brown, husk dry, kernel milky-starchy → doughy\n"
            "- Tomato: full colour change, firm to soft touch\n"
            "- Beans: pod turns yellow-brown, seeds rattle in pod\n"
            "- Potato: vines die back, skin sets firmly (doesn't peel easily)\n\n"
            "**Maximising yield:**\n"
            "- Harvest at correct maturity — late harvest loses quality\n"
            "- Handle gently to prevent bruising\n"
            "- Cool produce quickly after harvest\n\n"
            "**Storage tips:**\n"
            "- Store in cool (10–15°C), dry, well-ventilated spaces\n"
            "- Sort out damaged/diseased produce immediately\n"
            "- Maize: dry to <13% moisture content before storage\n"
            "- Potatoes: store in dark to prevent greening (solanine)"
        ),
    },
    "soil": {
        "keywords": ["soil", "ph", "lime", "acidity", "clay", "sandy", "loam", "organic matter", "humus"],
        "answer": (
            "**Soil Management 🏔️**\n\n"
            "**Ideal soil pH by crop:**\n"
            "- Maize: 5.8–7.0 | Tomato: 6.0–6.8 | Beans: 6.0–7.0\n"
            "- Potato: 5.0–6.5 | Rice: 5.5–7.0 | Banana: 5.5–7.0\n\n"
            "**Correcting acidic soil (pH <5.5):**\n"
            "- Apply agricultural lime at 1–3 tonnes/ha\n"
            "- Apply 3–6 months before planting\n"
            "- Dolomitic lime also adds Mg\n\n"
            "**Improving soil structure:**\n"
            "- Add organic matter (compost, manure) annually\n"
            "- Minimum tillage protects soil structure\n"
            "- Cover crops (mucuna, dolichos) fix nitrogen and add biomass\n\n"
            "**Low-cost soil test:** Send 500g sample to nearest agricultural office or agro-dealer lab"
        ),
    },
    "weather": {
        "keywords": ["weather", "rain", "temperature", "season", "climate", "drought", "flood", "frost"],
        "answer": (
            "**Weather & Seasonal Farming 🌤️**\n\n"
            "**Adapting to weather patterns:**\n"
            "- **Dry spells:** Mulch with 5–10 cm of crop residue to retain moisture\n"
            "- **Excessive rain:** Improve drainage; spray preventive fungicide\n"
            "- **High temperatures:** Provide shade nets for sensitive crops (tomato, pepper)\n\n"
            "**Climate-smart practices:**\n"
            "- Stagger planting dates to spread risk\n"
            "- Use drought-tolerant varieties during erratic rainfall\n"
            "- Plant windbreaks (Grevillea, Leucaena) to reduce wind damage\n\n"
            "**Disease weather alerts:**\n"
            "- 2+ days of high humidity + temps 20–25°C → high blight risk\n"
            "- Spray preventive fungicide before and after rain events"
        ),
    },
    "default": {
        "answer": (
            "**AI Farming Assistant 🤖**\n\n"
            "I can help you with:\n\n"
            "| Topic | Ask about |\n"
            "|-------|----------|\n"
            "| 💊 Fertiliser | NPK ratios, dosage, organic options |\n"
            "| 💧 Irrigation | Watering schedules, drought management |\n"
            "| 🐛 Pests | Identification, control, IPM |\n"
            "| 🛡️ Disease prevention | Cultural practices, spray schedules |\n"
            "| 🌾 Harvest | Maturity signs, storage tips |\n"
            "| 🏔️ Soil | pH, fertility, amendment |\n"
            "| 🌤️ Weather | Seasonal planning, climate adaptation |\n\n"
            "Type your farming question in plain English or Swahili!"
        ),
    },
}


def get_chat_response(query: str) -> str:
    q = query.lower()
    for topic, data in FARMING_KB.items():
        if topic == "default":
            continue
        if any(kw in q for kw in data["keywords"]):
            return data["answer"]
    # Check for crop-specific disease questions
    for crop, info in DISEASE_DB.items():
        if crop.lower() in q:
            disease_list = [d for d in info["diseases"].keys() if d != "Healthy"]
            response = f"**{info['icon']} {crop} Diseases**\n\n"
            response += f"Common diseases affecting {crop}:\n\n"
            for d in disease_list:
                sev = info["diseases"][d]["severity"]
                response += f"• **{d}** — Severity: {sev}\n"
            response += f"\n💡 Upload a leaf photo on the **Crop Doctor** page for instant AI diagnosis!"
            return response
    return FARMING_KB["default"]["answer"]


SEVERITY_COLOR = {
    "None": "🟢",
    "Low": "🟡",
    "Low-Medium": "🟡",
    "Medium": "🟠",
    "Medium-High": "🟠",
    "High": "🔴",
    "Very High": "🔴",
}
