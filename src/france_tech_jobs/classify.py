"""Conservative role, experience and location classification.

Classification is intentionally deterministic and transparent: uncertain records
are held back rather than silently assigned an experience level or country.
"""

from __future__ import annotations

import re
import unicodedata


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold().replace("’", "'"))
    return "".join(char for char in text if not unicodedata.combining(char))


def _matches(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text))


_DATA = r"\b(?:data engineer|data engineering|analytics engineer|big data engineer|data[ -]?ops engineer|ingenieur(?:e)? (?:de |des |en )?(?:donnees|data)|data platform engineer)\b"
_AI = r"\b(?:ai engineer|ia engineer|ai software engineer|machine learning engineer|ml engineer|mlops engineer|ml ops engineer|ingenieur(?:e)? (?:en )?(?:ia|machine learning)|llm engineer|nlp engineer|computer vision engineer)\b"
_AI_TOPIC = r"\b(?:generative ai|agentic ai|gen ?ai|ia generative|intelligence artificielle|ai platform|ml platform|mlops|ml ops|natural language processing|computer vision|large language models?)\b"
_SOFTWARE = r"\b(?:software (?:development engineer|engineer|developer)|(?:back[ -]?end|front[ -]?end|full[ -]?stack|mobile|platform) (?:engineer|developer)|developpeur(?:se)?(?: logiciel| software| full[ -]?stack| back[ -]?end| front[ -]?end| web)?|ingenieur(?:e)? (?:logiciel|software)|software engineering)\b"
_ENGINEER = r"\b(?:engineer|engineering|developer|developpeur|developpeuse|ingenieur|ingenieure)\b"
_INTERN = r"\b(?:internship|intern|interns|apprenticeship|apprentice|alternance|alternant|alternante|stage|stagiaire)\b"
_SENIOR = r"\b(?:senior|sr\.?|staff|principal|lead|manager|architect|architecte|head|director|directeur|directrice)\b"
_EXPERT_SENIOR = r"^\W*expert(?:e)?\s|\b(?:engineer|ingenieur|developer|developpeur)\s+expert(?:e)?\b"
_JUNIOR = r"\b(?:junior|jr\.?|new[ -]?grad(?:uate)?|graduate|early career|entry[ -]?level|debutant|debutante|jeune diplome|jeune diplomee)\b"
_MID = r"\b(?:mid[ -]?level|intermediate|confirme|confirmee|confirmed)\b"
_FRANCE = r"\b(?:france|french guiana|guyane|guadeloupe|martinique|reunion|mayotte|paris|toulouse|lyon|nantes|bordeaux|lille|marseille|montpellier|rennes|strasbourg|grenoble|nice|niort|sophia antipolis|saclay|ile de france)\b"
_INTERNATIONAL = r"\b(?:germany|allemagne|berlin|united kingdom|royaume uni|london|londres|ireland|irlande|dublin|spain|espagne|madrid|barcelona|barcelone|netherlands|pays bas|amsterdam|rotterdam|belgium|belgique|brussels|bruxelles|switzerland|suisse|geneva|geneve|zurich|luxembourg|portugal|italy|italie|canada|united states|usa|singapore|singapour|hong kong)\b"
_EXPERIENCE = re.compile(
    r"\b(?P<low>\d{1,2})\s*(?:(?:[-–]|to|a)\s*(?P<high>\d{1,2})|(?P<plus>\+))?\s*"
    r"(?:years?|ans?)\s*(?:(?P<minimum_before>minimum|min\.?|at least)\s*)?"
    r"(?:of\s+|d[' ]|de\s+)?(?:(?:professional|professionnelle?|hands[ -]on|software|development|engineering|work|relevant)\s+){0,5}"
    r"experience(?:\s+professionnelle?)?\b(?:\s*(?P<minimum_after>minimum|min\.?))?"
)
_COMPANY = r"\b(?:company|business|organisation|organization|entreprise|societe|agence|agency|founded|fondee|notre equipe|our team|we have|nous avons)\b"
_CANDIDATE = r"\b(?:candidate|candidates|applicant|applicants|you|your|requires?|required|must|have you|vous|votre|candidat|candidate|profil|recherche|exige|exigee|requis|requise)\b"


def _categories(title: str, description: str) -> list[str]:
    categories = []
    for name, pattern in (("data", _DATA), ("ai", _AI), ("software", _SOFTWARE)):
        if _matches(pattern, title):
            categories.append(name)
    # The description may mention AI for company context or as a productivity
    # tool. Require the engineering job title itself to indicate AI work.
    if _matches(_ENGINEER, title):
        if "ai" not in categories and _matches(_AI_TOPIC, title):
            categories.append("ai")
    return [name for name in ("data", "ai", "software") if name in categories]


def _experience(title: str, description: str, contract: str) -> str:
    if _matches(_INTERN, title) or _matches(_INTERN, contract):
        return "excluded"
    if _matches(r"\b(?:this|an?) (?:internship|apprenticeship)\b|\b(?:contrat|poste) (?:d[' ]|en )?(?:alternance|apprentissage|stage)\b", description):
        return "excluded"
    if _matches(_SENIOR, title) or _matches(_EXPERT_SENIOR, title):
        return "excluded"
    if _matches(r"\b(?:senior[ -]level\s+(?:role|position|job)|(?:role|position|poste)\s+senior)\b", description):
        return "excluded"

    junior = _matches(_JUNIOR, title)
    mid = _matches(_MID, title)
    title_range = _matches(r"\b(?:junior\s*(?:/|-|–|or|to)\s*(?:intermediate|mid(?:[ -]?level)?)|(?:intermediate|mid(?:[ -]?level)?)\s*(?:/|-|–|or|to)\s*junior)\b", title)
    if junior and mid and not title_range:
        return "unknown"
    title_level = "junior-mid" if title_range else "junior" if junior else "mid" if mid else "unknown"
    # Examine every explicit experience expression. An employer's own history
    # isn't an applicant requirement, and a later requirement must not be
    # hidden by an earlier number.
    requirements = []
    for clause in re.split(r"[.;!?\n]", description):
        previous_end = 0
        for experience in _EXPERIENCE.finditer(clause):
            prefix = clause[previous_end:experience.start()]
            previous_end = experience.end()
            company_mentions = list(re.finditer(_COMPANY, prefix))
            if company_mentions and not _matches(_CANDIDATE, prefix[company_mentions[-1].end():]):
                continue
            first = int(experience.group("low"))
            last = int(experience.group("high") or first)
            if first >= 5:
                return "excluded"
            open_ended = (
                experience.group("plus")
                or experience.group("minimum_before")
                or experience.group("minimum_after")
                or _matches(r"(?:at least|minimum(?: of)?|au moins|(?:au )?minimum(?: de)?|a partir de)\s*$", prefix)
            )
            if first > last or open_ended:
                requirements.append("unknown")
            elif last <= 2:
                requirements.append("junior")
            elif 3 <= first and last <= 4:
                requirements.append("mid")
            elif experience.group("high") and first <= 2 and last <= 4:
                requirements.append("junior-mid")
            else:
                requirements.append("unknown")
    if "unknown" in requirements or len(set(requirements)) > 1:
        return "unknown"
    if not requirements:
        return title_level
    requirement = requirements[0]
    if title_level == "unknown":
        return requirement
    if title_level == requirement:
        return title_level
    if "junior-mid" in (title_level, requirement):
        return "junior-mid"
    return "unknown"


def _geography(location: str) -> str:
    france = _matches(_FRANCE, location)
    international = _matches(_INTERNATIONAL, location)
    if france == international:
        return "unknown"
    return "france" if france else "international"


def classify(title: str, description: str, location: str, contract: str = "") -> dict:
    """Return category tags, experience, geography and publishing eligibility."""
    title, description, location, contract = map(_normalize, (title, description, location, contract))
    categories = _categories(title, description)
    seniority = _experience(title, description, contract)
    geography = _geography(location)
    return {
        "categories": categories,
        "seniority": seniority,
        "geography": geography,
        "eligible": bool(categories) and seniority in ("junior", "junior-mid", "mid") and geography != "unknown",
    }
