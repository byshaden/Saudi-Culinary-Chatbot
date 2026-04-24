import json
import random


class ResponseGenerator:
    def __init__(self):
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        """Load response templates from JSON"""
        try:
            with open("data/responses/templates.json", "r", encoding="utf-8") as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            print("Warning: templates.json not found")
            self._set_default_templates()
        except json.JSONDecodeError:
            print("Error: Invalid JSON in templates.json")
            self._set_default_templates()

    def _set_default_templates(self):
        """Set default templates if file not found"""
        self.templates = {
            "greeting": ["Hello! I'm Norah, your Saudi culinary guide! What's your name?"],
            "acknowledge_name": ["Nice to meet you, {name}!"],
            "default": ["I'm here to help with Saudi recipes!"],
            "show_category_rice": ["Here are rice dishes:\n{recipes}"],
            "show_category_meat": ["Here are meat dishes:\n{recipes}"],
            "show_category_dessert": ["Here are dessert options:\n{recipes}"],
            "show_similar": ["Here are similar dishes:\n{similar}"],
            "thanks_response": ["You're welcome, {name}!"],
            "goodbye": ["Goodbye, {name}!"],
            "need_clarification": ["Could you be more specific, {name}?"],
            "no_recipe_found": ["I couldn't find that recipe, {name}."],
        }

    def generate_greeting(self):
        templates = self.templates.get("greeting", ["Hello! Welcome!"])
        return random.choice(templates)

    def generate_name_acknowledgment(self, name):
        templates = self.templates.get("acknowledge_name", ["Nice to meet you, {name}!"])
        template = random.choice(templates)
        return template.format(name=name)

    def generate_category_response(self, category, recipes, user_name=""):
        """Generate response showing category recipes"""
        recipe_list = ""

        for i, recipe in enumerate(recipes, 1):
            name_en = recipe.get("name_en", "Unknown")
            name_ar = recipe.get("name_ar", "")

            desc = recipe.get("description", "")
            prep_time = recipe.get("prep_time", "N/A")
            cook_time = recipe.get("cook_time", "N/A")

            # Handle spice vs sweetness safely
            spice_or_sweet = (
                recipe.get("spice_level")
                or recipe.get("sweetness_level")
                or recipe.get("sweetness_level".replace("_", ""))  # harmless fallback
                or "N/A"
            )

            emoji = "🌶️" if recipe.get("spice_level") is not None else "🧁"

            recipe_list += f"\n{i}️⃣ **{name_en}**"
            if name_ar:
                recipe_list += f" ({name_ar})"
            recipe_list += "\n"
            if desc:
                recipe_list += f"   {desc}\n"
            recipe_list += f"   ⏱️ {prep_time} + {cook_time}\n"
            recipe_list += f"   {emoji} {spice_or_sweet}\n"

        template_key = f"show_category_{category}"
        templates = self.templates.get(
            template_key,
            ["Here are {category} dishes:\n{recipes}"],
        )

        template = random.choice(templates)
        return template.format(name=user_name, recipes=recipe_list, category=category)

    def generate_recipe_display(self, recipe):
        """Generate formatted full recipe (works for rice/meat/dessert)"""
        name_en = recipe.get("name_en", "Unknown")
        name_ar = recipe.get("name_ar", "")
        description = recipe.get("description", "")
        region = recipe.get("region", "N/A")
        servings = recipe.get("servings", "N/A")
        prep_time = recipe.get("prep_time", "N/A")
        cook_time = recipe.get("cook_time", "N/A")
        difficulty = recipe.get("difficulty", "N/A")

        spice_level = recipe.get("spice_level")
        sweetness_level = recipe.get("sweetness_level")

        output = f"# 🍽️ {name_en}"
        if name_ar:
            output += f" ({name_ar})"
        output += "\n\n"

        output += f"## 📖 About\n{description}\n\n"
        output += f"**Region:** {region}\n"
        output += f"**Servings:** {servings}\n"
        output += f"**Prep Time:** {prep_time}\n"
        output += f"**Cook Time:** {cook_time}\n"
        output += f"**Difficulty:** {difficulty}\n"

        # Show spice or sweetness depending on recipe type
        if spice_level is not None:
            output += f"**Spice Level:** {spice_level}\n\n"
        elif sweetness_level is not None:
            output += f"**Sweetness Level:** {sweetness_level}\n\n"
        else:
            output += "**Taste Level:** N/A\n\n"

        output += "---\n\n"

        output += "## 🛒 Ingredients\n"
        for ingredient in recipe.get("ingredients", []):
            output += f"- {ingredient}\n"
        output += "\n---\n\n"

        output += "## 👨‍🍳 Instructions\n\n"
        for i, step in enumerate(recipe.get("steps", []), 1):
            output += f"**Step {i}:**\n{step}\n\n"

        output += "---\n\n"

        output += "## 💡 Pro Tips\n"
        for tip in recipe.get("tips", []):
            output += f"- {tip}\n"
        output += "\n"

        return output

    def generate_similar_dishes_response(self, similar_recipes, user_name=""):
        if not similar_recipes:
            return f"I don't have similar dishes right now, {user_name}."

        similar_list = ""
        for i, recipe in enumerate(similar_recipes, 1):
            similar_list += f"\n{i}. **{recipe.get('name_en','Unknown')}** - {recipe.get('description','')}\n"

        templates = self.templates.get("show_similar", ["Here are similar dishes:\n{similar}"])
        template = random.choice(templates)
        return template.format(name=user_name, similar=similar_list)

    def generate_thanks_response(self, user_name=""):
        templates = self.templates.get("thanks_response", ["You're welcome!"])
        template = random.choice(templates)
        return template.format(name=user_name)

    def generate_goodbye_response(self, user_name=""):
        templates = self.templates.get("goodbye", ["Goodbye!"])
        template = random.choice(templates)
        return template.format(name=user_name)

    def generate_clarification_request(self, user_name=""):
        templates = self.templates.get("need_clarification", ["Could you be more specific?"])
        template = random.choice(templates)
        return template.format(name=user_name)

    def generate_no_recipe_response(self, user_name=""):
        templates = self.templates.get("no_recipe_found", ["I couldn't find that recipe."])
        template = random.choice(templates)
        return template.format(name=user_name)

    def generate_default_response(self, user_name=""):
        templates = self.templates.get("default", ["How can I help you?"])
        template = random.choice(templates)
        return template.format(name=user_name)
