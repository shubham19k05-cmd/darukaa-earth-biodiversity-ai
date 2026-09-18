from backend.app.reasoning import analyze

def test_multi_metric():
    e={"soil_organic_carbon":"0.3%","rainfall":"low","land_use":"monoculture","crop":"wheat"}
    n,q,r,k=analyze(e,"biodiversity decline")
    assert not n and r and len(r[0]["impacted_metrics"])>=3

def test_clarification():
    n,q,r,k=analyze({"soil_organic_carbon":"0.3%"},"biodiversity")
    assert n and "rainfall" in q
