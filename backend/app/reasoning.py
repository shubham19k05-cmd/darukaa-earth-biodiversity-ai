from .knowledge import retrieve_knowledge

def low_soc(v):
    try:return float(str(v).replace("%",""))<1
    except:return False
def low_rain(v): return str(v).lower() in {"low","very low","drought","semi-arid"}
def analyze(environment,query):
    required=["soil_organic_carbon","rainfall","land_use"]
    missing=[x for x in required if x not in environment or environment[x] in ("",None)]
    if missing:return True,"Please provide: "+", ".join(missing)+".",[],[]
    retrieved=retrieve_knowledge(environment,query)
    evidence=[{"organization":r["source_organization"],"title":r["title"],"url":r["source_url"]} for r in retrieved[:3]]
    land=str(environment.get("land_use","")).lower()
    crop=str(environment.get("crop","")).lower()
    rec={
      "action":"Introduce a legume-based cover crop/intercrop and retain diverse native vegetation strips where feasible.",
      "why_it_works":"Ground cover reduces bare-soil exposure, while plant diversity adds habitat and food resources. Legume-based systems can contribute biologically fixed nitrogen. Together these practices address soil condition, water stress and habitat simplification.",
      "impacted_metrics":["soil organic carbon","soil moisture","habitat diversity","species richness"],
      "time_horizon":"medium term (2–3 years)","confidence":"medium","evidence":evidence
    }
    if "deforestation" in str(environment).lower() or "fragment" in str(environment).lower():
      rec={"action":"Restore native habitat connections between remaining vegetation patches and prioritize continuous corridors.","why_it_works":"Connected habitat can reduce fragmentation effects and improve movement opportunities for organisms. Linking habitat structure with land-cover context makes the intervention more targeted.","impacted_metrics":["habitat diversity","species richness","land-cover connectivity"],"time_horizon":"long term (3–10 years)","confidence":"medium","evidence":evidence}
    return False,None,[rec],retrieved
