import streamlit as st
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from core.recipe_matcher import RecipeMatcher
from core.response_generator import ResponseGenerator

st.set_page_config(
    page_title="Chat with Norah",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Chat with Norah")
st.caption("Your Saudi Culinary Guide 🇸🇦")

session = SessionManager()
classifier = IntentClassifier()
recipe_matcher = RecipeMatcher()
response_gen = ResponseGenerator()

with st.sidebar:
    st.header("Chat Options")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        session.clear_messages()
        st.rerun()

    st.markdown("---")
    st.subheader("About")
    st.write("Ask Norah about Saudi dishes, recipes, and cooking tips!")

    if session.has_user_name():
        st.info(f"👤 User: {session.get_user_name()}")

if len(session.get_messages()) == 0:
    greeting = response_gen.generate_greeting()
    session.add_message("assistant", greeting)

for message in session.get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    session.add_message("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Norah is thinking..."):
            user_name = session.get_user_name() or ""

            # SUPER IMPORTANT FALLBACK:
            # If user typed a dish name directly, show recipe even if intent classifier returns default
            dish_direct = classifier.extract_dish_name(prompt)
            if dish_direct:
                recipe = recipe_matcher.get_recipe_by_name(dish_direct)
                if recipe:
                    session.set_last_recipe(dish_direct)
                    response = response_gen.generate_recipe_display(recipe)
                    st.markdown(response)
                    session.add_message("assistant", response)
                    st.stop()

            intent = classifier.classify_intent(prompt)

            # ---- Fallbacks (IMPORTANT for Arabic dish names) ----
            dish_name = classifier.extract_dish_name(prompt)
            category_hint = classifier.extract_category(prompt)

            if intent in (None, "", "default"):
               if dish_name:
                  intent = "request_recipe"
            elif category_hint:
             intent = "request_category"
            # 1) Name
            if intent == "provide_name" and not session.has_user_name():
                name = classifier.extract_name(prompt)
                if name:
                    session.set_user_name(name)
                    response = response_gen.generate_name_acknowledgment(name)
                else:
                    response = "I didn't quite catch your name. Could you tell me again?"

            # 2) Greeting
            elif intent == "greeting":
                if session.has_user_name():
                    response = f"Hello again, {session.get_user_name()}! How can I help you today?"
                else:
                    response = response_gen.generate_greeting()

            # 3) Category
            elif intent == "request_category":
                category = classifier.extract_category(prompt)
                if category:
                    session.set_current_category(category)
                    recipes = recipe_matcher.search_by_category(category)
                    if recipes:
                        response = response_gen.generate_category_response(category, recipes, user_name)
                    else:
                        response = f"I don't have {category} recipes yet, {user_name}. Try rice, meat, or dessert!"
                else:
                    response = response_gen.generate_clarification_request(user_name)

            # 4) mention_dish (if your intents.json returns mention_dish)
            elif intent == "mention_dish":
                dish_name = classifier.extract_dish_name(prompt)
                if dish_name:
                    recipe = recipe_matcher.get_recipe_by_name(dish_name)
                    if recipe:
                        session.set_last_recipe(dish_name)
                        response = response_gen.generate_recipe_display(recipe)
                    else:
                        response = response_gen.generate_no_recipe_response(user_name)
                else:
                    response = response_gen.generate_clarification_request(user_name)

            # 5) Request recipe/details
            elif intent in ("request_recipe", "request_details"):
                dish_name = classifier.extract_dish_name(prompt)
                if dish_name:
                    recipe = recipe_matcher.get_recipe_by_name(dish_name)
                    if recipe:
                        session.set_last_recipe(dish_name)
                        response = response_gen.generate_recipe_display(recipe)
                    else:
                        response = response_gen.generate_no_recipe_response(user_name)
                else:
                    results = recipe_matcher.search_by_keyword(prompt)
                    if results:
                        response = response_gen.generate_category_response("search results", results[:5], user_name)
                    else:
                        response = response_gen.generate_clarification_request(user_name)

            # 6) Similar dishes
            elif intent == "similar_dishes":
                last_recipe = session.get_last_recipe()
                if last_recipe and len(session.get_messages()) > 2:
                    similar = recipe_matcher.get_similar_recipes(last_recipe)
                    if similar:
                        response = response_gen.generate_similar_dishes_response(similar, user_name)
                    else:
                        response = "I don't have similar dishes for that one yet!"
                else:
                    response = "Which dish would you like similar recipes for?"

            # 7) Thanks / goodbye
            elif intent == "thanks":
                response = response_gen.generate_thanks_response(user_name)

            elif intent == "goodbye":
                response = response_gen.generate_goodbye_response(user_name)

            else:
                response = response_gen.generate_default_response(user_name)

        st.markdown(response)

    session.add_message("assistant", response)
