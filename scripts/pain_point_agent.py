import json
import re

STOPWORDS = {
    "của", "và", "là", "cho", "bị", "thì", "được", "khi", "tới", "sau", "trong", "về", "tại", "các",
    "một", "này", "những", "với", "có", "không", "nên", "để", "bằng", "đã", "của", "ra", "hoặc"
}

def load_db(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ\s]", " ", text)
    words = [w for w in text.split() if w not in STOPWORDS]
    return set(words)

def preprocess_context(context):
    results = set()
    if not context:
        return results
    for k, v in context.items():
        if isinstance(v, str):
            results.add(v.lower())
        elif isinstance(v, list):
            for val in v:
                results.add(str(val).lower())
    return results


def match_score(words, targer_list):
    score = 0
    for t in targer_list:
        t_w = preprocess(t)
        matches = words & t_w
        score += len(matches)
    return score

def explain_matching(pain, context, feature):
    exp = []

    kw_matches = pain & set([kw.lower() for kw in feature.get("keywords", [])])
    if kw_matches:
        exp.append(f"Từ khóa trùng: {', '.join(kw_matches)}")

    epp_matches = []
    for ep in feature.get("example_pain_points", []):
        ep_words = preprocess(ep)
        if pain & ep_words:
            epp_matches.append(ep)
    if epp_matches:
        exp.append(f"Pain point gần giống ví dụ: {', '.join(epp_matches)}")

    context_match = context & set([c.lower() for c in feature.get("channels", []) + feature.get("customer_types", [])])
    if context_match:
            exp.append(f"Context trùng: {', '.join(context_match)}")
    return "; ".join(exp)


def match_pain_point(pain_point, features, context=None, top_n=3):
    pain_words = preprocess(pain_point)
    context_words = preprocess_context(context)
    results = []

    for feature in features:
        score = 0
        score += match_score(pain_words, feature.get("keywords", []))
        score += 2 * match_score(pain_words, feature.get("example_pain_points", []))
        score += 0.5 * match_score(context_words, feature.get("channels", []))
        score += 0.5 * match_score(context_words, feature.get("customer_types", []))
        if score > 0:
            results.append({
                "feature_name": feature["feature_name"],
                "category": feature["category"],
                "description": feature["description"],
                "how_it_helps": feature["how_it_helps"],
                "link": feature["link"],
                "relevance_score": score,
                "explanation": explain_matching(pain_words, context_words, feature)
            })

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:top_n]

if __name__ == "__main__":
    path = '../database/features.json'
    features = load_db(path)

    input_json = {
        "pain_point": "Nhân viên hỗ trợ bị quá tải câu hỏi lặp lại",
        "context": {
            "channel": "email",
            "customer_type": "B2C"
        }
    }

    output = match_pain_point(input_json["pain_point"], features, input_json.get("context"))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    with open('../output/output.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

# python pain_point_agent.py