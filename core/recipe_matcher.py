import json
import re

class RecipeMatcher:
    """
    Loads recipes from JSON files and provides robust search by:
    - recipe id (e.g., grilled_lamb, madfoon, maamoul)
    - English name (e.g., "Grilled Lamb")
    - Arabic name (e.g., "لحم مشوي")
    - tolerant matching for Arabic variants + punctuation (e.g., ma'amoul)
    """
    def __init__(self):
        self.recipes = {}
        self._name_index = {}  # normalized_name -> recipe_id
        self.load_all_recipes()

    @staticmethod
    def _normalize(text: str) -> str:
        if text is None:
            return ""
        text = str(text).lower().strip()

        # Remove Arabic diacritics + tatweel
        text = re.sub(r"[ًٌٍَُِّْـ]", "", text)

        # Arabic letter normalization
        text = re.sub(r"[إأآا]", "ا", text)
        text = re.sub(r"ى", "ي", text)
        text = re.sub(r"ؤ", "و", text)
        text = re.sub(r"ئ", "ي", text)
        text = re.sub(r"ة", "ه", text)

        # Normalize common apostrophes/quotes
        text = text.replace("’", "'").replace("`", "'").replace("ʻ", "'").replace("ʾ", "'")

        # Keep letters/numbers/underscore (so grilled_lamb stays searchable)
        # Convert everything else to spaces
        text = re.sub(r"[^0-9a-z_\u0600-\u06FF\s']", " ", text)

        # Remove apostrophes in matching (ma'amoul -> maamoul)
        text = text.replace("'", "")

        # Collapse spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def load_all_recipes(self):
        """Load all recipes from JSON files and build a search index."""
        recipe_files = {
            "rice": "data/recipes/rice_dishes.json",
            "meat": "data/recipes/meat_dishes.json",
            "dessert": "data/recipes/desserts.json",
        }

        for category, filepath in recipe_files.items():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    recipes = json.load(f)

                for recipe_id, recipe_data in recipes.items():
                    recipe_data["id"] = recipe_id
                    recipe_data["category"] = category
                    self.recipes[recipe_id] = recipe_data

                    # Index by id, English name, Arabic name (all normalized)
                    candidates = [
                        recipe_id,
                        recipe_data.get("name_en", ""),
                        recipe_data.get("name_ar", ""),
                    ]
                    for c in candidates:
                        key = self._normalize(c)
                        if key:
                            self._name_index[key] = recipe_id

            except FileNotFoundError:
                print(f"Warning: {filepath} not found")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {filepath}")

    def search_by_category(self, category: str):
        category = (category or "").lower().strip()
        return [r for r in self.recipes.values() if r.get("category", "").lower() == category]

    def search_by_keyword(self, keyword: str):
        keyword_norm = self._normalize(keyword)
        if not keyword_norm:
            return []

        results = []
        for recipe in self.recipes.values():
            hay = " ".join([
                recipe.get("name_en", ""),
                recipe.get("name_ar", ""),
                recipe.get("description", ""),
                " ".join(recipe.get("tags", []) or []),
                recipe.get("id", "")
            ])
            if keyword_norm in self._normalize(hay):
                results.append(recipe)
        return results

    def get_recipe_by_name(self, name: str):
        """
        Robust lookup:
        - direct match via normalized index (id/name_en/name_ar)
        - fallback: contains match (normalized)
        """
        q = self._normalize(name)
        if not q:
            return None

        # 1) Direct index hit
        recipe_id = self._name_index.get(q)
        if recipe_id and recipe_id in self.recipes:
            return self.recipes[recipe_id]

        # 2) Try a few query variants (spaces vs underscores)
        q2 = q.replace("_", " ")
        recipe_id = self._name_index.get(q2)
        if recipe_id and recipe_id in self.recipes:
            return self.recipes[recipe_id]

        # 3) Fallback: contains match across indexed keys
        for key, rid in self._name_index.items():
            if q == key or q2 == key:
                return self.recipes.get(rid)

        for key, rid in self._name_index.items():
            if q in key or q2 in key or key in q or key in q2:
                return self.recipes.get(rid)

        return None

    def get_similar_recipes(self, recipe_name: str):
        recipe = self.get_recipe_by_name(recipe_name)
        if not recipe:
            return []
        similar_ids = recipe.get("similar_dishes", []) or []
        return [self.recipes[sid] for sid in similar_ids if sid in self.recipes]
