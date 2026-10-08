"""
Sensitive Patterns and Word Dictionaries for Content Moderation.

Categories:
1. Offensive / Profanity (Medium risk, weight 15)
2. Harmful / Abusive (High risk, weight 25)
3. Prohibited / Illegal / Threat (Critical risk, weight 40)
4. Spam / Suspicious (Low risk, weight 10)

Note: Terms are demo/academic patterns designed to demonstrate DSA search algorithms.
"""

from typing import Dict, List, Any

CATEGORY_WEIGHTS: Dict[str, int] = {
    "Offensive / Profanity": 15,
    "Harmful / Abusive": 25,
    "Prohibited / Illegal / Threat": 40,
    "Spam / Suspicious": 10
}

# Categorized dictionary of sensitive pattern strings
SENSITIVE_PATTERNS: List[Dict[str, Any]] = [
    # Offensive / Profanity
    {"pattern": "stupid", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "idiot", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "useless", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "dumb", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "fool", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "hate", "category": "Offensive / Profanity", "severity": "Medium"},
    {"pattern": "trash", "category": "Offensive / Profanity", "severity": "Medium"},

    # Harmful / Abusive
    {"pattern": "kill yourself", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "die", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "shut up", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "abuse", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "attack", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "destroy you", "category": "Harmful / Abusive", "severity": "High"},
    {"pattern": "worthless", "category": "Harmful / Abusive", "severity": "High"},

    # Prohibited / Illegal / Threat
    {"pattern": "hack account", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},
    {"pattern": "steal credit card", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},
    {"pattern": "bomb threat", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},
    {"pattern": "buy illegal drugs", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},
    {"pattern": "malware payload", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},
    {"pattern": "bypass security", "category": "Prohibited / Illegal / Threat", "severity": "Critical"},

    # Spam / Suspicious
    {"pattern": "click here now", "category": "Spam / Suspicious", "severity": "Low"},
    {"pattern": "free money", "category": "Spam / Suspicious", "severity": "Low"},
    {"pattern": "guaranteed prize", "category": "Spam / Suspicious", "severity": "Low"},
    {"pattern": "buy followers", "category": "Spam / Suspicious", "severity": "Low"},
    {"pattern": "earn fast cash", "category": "Spam / Suspicious", "severity": "Low"},
    {"pattern": "subscribe immediately", "category": "Spam / Suspicious", "severity": "Low"},
]
