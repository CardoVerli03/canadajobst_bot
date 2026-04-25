import keywords

def calculate_job_score(title, description):
    """Deep analysis of job postings for scoring"""
    score = 0
    matched_reasons = []
    
    # Combine everything into one text block for scanning
    text = f"{title} {description}".lower()

    # 1. PRIORITY: Visa & Sponsorship Check (+3 points)
    has_sponsorship = False
    for term in keywords.SCORING["VISA_SPONSORSHIP"]["terms"]:
        if term in text:
            score += keywords.SCORING["VISA_SPONSORSHIP"]["points"]
            matched_reasons.append(f"✅ {term.upper()}")
            has_sponsorship = True
            break # Only score once per category

    # 2. EXPERIENCE: Entry Level/No Exp Check (+2 points)
    for term in keywords.SCORING["NO_EXPERIENCE"]["terms"]:
        if term in text:
            score += keywords.SCORING["NO_EXPERIENCE"]["points"]
            matched_reasons.append(f"🎓 {term.title()}")
            break

    # 3. SECTOR: Job Category Detection (+2 points)
    job_category = "💼 General" # Default
    for cat_emoji_name, terms in keywords.CATEGORIES.items():
        for term in terms:
            if term in text:
                score += 2
                job_category = cat_emoji_name
                break
        if job_category != "💼 General":
            break
    
    # ULINZI WA ZIADA: Kama haina sponsorship kabisa, ipunguzie alama
    # Hii inahakikisha bot haiposti kazi za Wacanada tu zisizo na visa support
    if not has_sponsorship:
        score = 0 

    return score, job_category, matched_reasons

def is_job_worthy(score):
    """Threshold for posting (3 points means it MUST have sponsorship)"""
    return score >= 3
