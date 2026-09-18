import json
from pathlib import Path

PATH=Path(__file__).resolve().parents[2]/"data"/"knowledge.json"

def load_knowledge():
    return json.loads(PATH.read_text(encoding="utf-8"))

def retrieve_knowledge(environment,query,top_k=5):
    text=(query+" "+" ".join(f"{k} {v}" for k,v in environment.items())).lower()
    terms=set(text.replace(","," ").replace("."," ").split())
    scored=[]
    for item in load_knowledge():
        hay=(item["topic"]+" "+item["content"]+" "+" ".join(item.get("keywords",[]))).lower()
        score=sum(1 for t in terms if len(t)>2 and t in hay)
        if score: scored.append((score,item))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [x[1] for x in scored[:top_k]]
