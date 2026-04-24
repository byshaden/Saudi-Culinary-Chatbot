import streamlit as st

class SessionManager:
    """Manages user session state for the chatbot"""
    
    def __init__(self):
        """Initialize session state variables"""
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Set up default session state values"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'user_name' not in st.session_state:
            st.session_state.user_name = None
        
        if 'conversation_state' not in st.session_state:
            st.session_state.conversation_state = 'greeting'
        
        if 'last_recipe_shown' not in st.session_state:
            st.session_state.last_recipe_shown = None
        
        if 'current_category' not in st.session_state:
            st.session_state.current_category = None
    
    def get_user_name(self):
        """Get the user's name"""
        return st.session_state.user_name
    
    def set_user_name(self, name):
        """Set the user's name"""
        st.session_state.user_name = name
        st.session_state.conversation_state = 'name_provided'
    
    def has_user_name(self):
        """Check if user has provided their name"""
        return st.session_state.user_name is not None
    
    def add_message(self, role, content):
        """Add a message to the conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: message text
        """
        st.session_state.messages.append({
            'role': role,
            'content': content
        })
    
    def get_messages(self):
        """Get all messages in the conversation"""
        return st.session_state.messages
    
    def clear_messages(self):
        """Clear all messages and reset conversation"""
        st.session_state.messages = []
        st.session_state.user_name = None
        st.session_state.conversation_state = 'greeting'
        st.session_state.last_recipe_shown = None
        st.session_state.current_category = None
    
    def get_conversation_state(self):
        """Get current conversation state"""
        return st.session_state.conversation_state
    
    def set_conversation_state(self, state):
        """Set conversation state
        
        Valid states:
        - 'greeting': Initial greeting
        - 'waiting_for_name': Waiting for user name
        - 'name_provided': Name received
        - 'browsing_categories': User browsing food categories
        - 'viewing_recipe': Showing specific recipe
        - 'showing_similar': Showing similar dishes
        """
        st.session_state.conversation_state = state
    
    def set_last_recipe(self, recipe_name):
        """Remember the last recipe shown"""
        st.session_state.last_recipe_shown = recipe_name
    
    def get_last_recipe(self):
        """Get the last recipe shown"""
        return st.session_state.last_recipe_shown
    
    def set_current_category(self, category):
        """Set the current food category being browsed"""
        st.session_state.current_category = category
    
    def get_current_category(self):
        """Get current category"""
        return st.session_state.current_category
    
    def get_last_user_message(self):
        """Get the most recent user message"""
        for message in reversed(st.session_state.messages):
            if message['role'] == 'user':
                return message['content']
        return None