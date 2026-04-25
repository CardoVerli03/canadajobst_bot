import keywords

def calculate_job_score(title, description):
    """Analyse job description na title kupata alama"""
    score = 0
    matched_reasons = []
    text = f"{title} {description}".lower()

    # 1. Check Sponsorship (+3 points)
    for term in keywords.SCORING["VISA_SPONSORSHIP"]["terms"]:
        if term in text:
            score += keywords.SCORING["VISA_SPONSORSHIP"]["points"]
            matched_reasons.append(f"✅ {term.upper()}")
            break # Piga moja tu kwa category hii

    # 2. Check No Experience (+2 points)
    for term in keywords.SCORING["NO_EXPERIENCE"]["terms"]:
        if term in text:
            score += keywords.SCORING["NO_EXPERIENCE"]["points"]
            matched_reasons.append(f"🎓 {term.title()}")
            break

    # 3. Check Categories (+2 points)
    job_category = "General"
    for cat_name, terms in keywords.CATEGORIES.items():
        for term in terms:
            if term in text:
                score += 2
                job_category = cat_name
                break
    
    return score, job_category, matched_reasons

def is_job_worthy(score):
    """Vigezo vyako: Lazima iwe na minimum 3 points"""
    return score >= 3
