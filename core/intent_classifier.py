import json
import re


class IntentClassifier:
    def __init__(self):
        self.intents = {}
        self.load_intents()

    def load_intents(self):
        """Load intent patterns from JSON"""
        try:
            with open("data/responses/intents.json", "r", encoding="utf-8") as f:
                self.intents = json.load(f)
        except FileNotFoundError:
            print("Warning: intents.json not found")
            self._set_default_intents()
        except json.JSONDecodeError:
            print("Error: Invalid JSON in intents.json")
            self._set_default_intents()

    def _set_default_intents(self):
        """Set default intents if file not found"""
        self.intents = {
            "greeting": {"patterns": ["hello", "hi"], "priority": 10},
            "provide_name": {"patterns": ["my name is", "i'm", "i am"], "priority": 9},
            "request_category": {"patterns": ["rice", "meat", "dessert"], "priority": 8},
        }

    def _match_pattern(self, message: str, pattern: str) -> bool:
        """
        Match pattern against message.
        - If pattern looks like regex (contains \s, \w, [], (), |, ?, +, *, ., ^, $ ...),
          we treat it as regex directly.
        - Otherwise, we match as a whole word/phrase using boundaries.
        """
        pattern = (pattern or "").strip()
        if not pattern:
            return False

        # Decide if this pattern is regex-ish
        regex_markers = ["\\s", "\\w", "[", "]", "(", ")", "|", "?", "+", "*", ".", "^", "$"]
        looks_like_regex = any(m in pattern for m in regex_markers)

        try:
            if looks_like_regex:
                return re.search(pattern, message, flags=re.IGNORECASE) is not None
            else:
                # literal phrase/word, use boundaries
                # if it has spaces, boundaries still work ok for phrases too
                escaped = re.escape(pattern)
                return re.search(rf"\b{escaped}\b", message, flags=re.IGNORECASE) is not None
        except re.error:
            # If regex is invalid, fall back to literal
            escaped = re.escape(pattern)
            return re.search(rf"\b{escaped}\b", message, flags=re.IGNORECASE) is not None

    def classify_intent(self, message: str) -> str:
        """Determine user's intent using patterns from intents.json"""
        message = (message or "").lower().strip()

        best_intent = None
        highest_priority = -1

        for intent_name, intent_data in self.intents.items():
            patterns = intent_data.get("patterns", [])
            priority = intent_data.get("priority", 0)

            for pattern in patterns:
                if self._match_pattern(message, pattern):
                    if priority > highest_priority:
                        highest_priority = priority
                        best_intent = intent_name
                    break  # stop checking other patterns for this intent

        return best_intent if best_intent else "default"

    def extract_name(self, message: str):
        """Extract user's name using regex patterns"""
        message = (message or "").strip()

        patterns = [
            r"(?:my name is|i'?m|call me|i am|this is)\s+([a-zA-Z]+)",
            r"اسمي\s+(\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                name = match.group(1)
                return name.capitalize()

        # fallback: pick a plausible short name token
        words = message.split()
        if len(words) <= 3:
            skip_words = {"hello", "hi", "hey", "iam", "am", "i", "im"}
            for word in words:
                if word.isalpha() and len(word) > 1 and word.lower() not in skip_words:
                    return word.capitalize()

        return None

    def extract_category(self, message: str):
        """Extract food category"""
        message = (message or "").lower()

        categories = {
            "rice": [r"\brice\b", r"\bرز\b", r"\bkabsa\b", r"\bmandi\b"],
            "meat": [r"\bmeat\b", r"\blamb\b", r"\bbeef\b", r"\bchicken\b", r"\bلحم\b"],
            "dessert": [
                r"\bdessert\b", r"\bdesserts\b",
                r"\bsweet\b", r"\bsweets\b",
                r"\bcake\b",
                r"\bحلو\b", r"\bحلويات\b"
            ],
        }

        for category, patterns in categories.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return category

        return None

    def extract_dish_name(self, message):
        import re

        msg = (message or "").lower().strip()

        # Normalize apostrophes (ma'amoul → maamoul)
        msg = re.sub(r"[’`ʻʾ']", "", msg)

        dishes = [
            # Rice
            r"kabsa", r"كبسة", r"كبسه",
            r"mandi", r"مندي",
            r"bukhari", r"بخاري",

            # Meat
            r"mathbi", r"مظبي",
            r"haneeth", r"حنيذ",
            r"madfoon", r"مدفون",
            r"grilled\s*lamb", r"grilled_lamb", r"لحم\s*مشوي",

            # Desserts
            r"kunafa", r"كنافة",
            r"basbousa", r"بسبوسة", r"بسبوسه",
            r"maamoul", r"maamol", r"mamoul", r"معمول",
        ]

        for pattern in dishes:
            if re.search(pattern, msg):
                return pattern

        return None

    def is_positive_response(self, message: str) -> bool:
        message = (message or "").lower().strip()
        positive_pattern = r"\b(yes|yeah|yep|sure|ok|okay|نعم|ايوه|تمام)\b"
        return bool(re.search(positive_pattern, message))

    def is_negative_response(self, message: str) -> bool:
        message = (message or "").lower().strip()
        negative_pattern = r"\b(no|nope|not|don\'?t|لا|ماني|مو|مب)\b"
        return bool(re.search(negative_pattern, message))
