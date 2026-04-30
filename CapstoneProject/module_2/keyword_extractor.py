# module2/keyword_extractor.py

KEYWORD_DICT = {
    "budget":        ["budget", "price", "cost", "lakhs", "emi"],
    "loan":          ["loan", "finance", "bank"],
    "visit":         ["site visit", "visit", "schedule"],
    "urgency":       ["urgent", "immediately", "this month"],
    "comparison":    ["compare", "difference", "better than"],
    "specification": ["2bhk", "3bhk", "sqft", "amenities"]
}

def extract_keywords(text: str):
    """
    Returns:
      keywords      : list of matched category names
      keyword_count : total matched categories
      has_budget    : 1 if budget matched
      has_loan      : 1 if loan matched
      has_visit     : 1 if visit matched
    """
    matched = set()

    for category, terms in KEYWORD_DICT.items():
        for term in terms:
            if term in text:
                matched.add(category)
                break

    matched = sorted(list(matched))  # deterministic ordering

    has_budget = 1 if "budget" in matched else 0
    has_loan   = 1 if "loan" in matched else 0
    has_visit  = 1 if "visit" in matched else 0

    return matched, len(matched), has_budget, has_loan, has_visit