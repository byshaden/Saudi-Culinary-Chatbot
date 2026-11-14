# 🇸🇦 Saudi Culinary Chatbot - نورة

An intelligent conversational chatbot that introduces foreigners to authentic Saudi cuisine through natural, personalized interactions.

🎓 *Team project — Tuwaiq Academy AI Bootcamp (2026)*

![Saudi Flag](https://img.shields.io/badge/Made%20in-Saudi%20Arabia-006C35?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

---

## 🌟 Overview

**Norah** is a friendly Saudi culinary guide chatbot designed to help foreigners discover and learn about traditional Saudi dishes. Through natural language conversation, users can explore authentic recipes, learn cooking techniques, and understand the cultural context behind each dish.

### ✨ Key Features

- 🤖 **Natural Language Understanding** - Understands user intent using pattern matching and regex
- 💬 **Conversational Memory** - Remembers your name and conversation context
- 🍽️ **Authentic Recipes** - Detailed Saudi recipes with ingredients and step-by-step instructions
- 🎨 **Saudi-Themed UI** - Traditional design with Saudi colors and aesthetics
- 🌍 **Bilingual Support** - Understands both English and Arabic inputs
- 📚 **Cultural Context** - Learn the story and traditions behind each dish

---

## 🏗️ Project Structure

```
Saudi-Culinary-Chatbot/
├── pages/
│   ├── 1_Home.py              # Landing page
│   ├── 2_Chat.py              # Main chat interface
│   └── 3_Team.py              # Team information
├── core/
│   ├── intent_classifier.py   # Intent detection & entity extraction
│   ├── recipe_matcher.py      # Recipe search and retrieval
│   └── response_generator.py  # Response template system
├── data/
│   ├── recipes/               # Recipe database (JSON)
│   └── responses/             # Response templates (JSON)
├── utils/
│   └── session_manager.py     # Session state management
├── .streamlit/
│   └── config.toml            # App theme configuration
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/byshaden/Saudi-Culinary-Chatbot.git
   cd Saudi-Culinary-Chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

---

## 💻 Technologies Used

### Core Technologies
- **Python 3.11+** - Main programming language
- **Streamlit** - Web application framework
- **Regular Expressions** - Pattern matching for NLP
- **JSON** - Data storage

### Key Libraries
```python
streamlit==1.32.0    # Web UI framework
```

### Architecture Pattern
- **Rule-Based NLP** - Intent classification using regex patterns
- **Template-Based Response Generation** - Predefined response templates
- **Session State Management** - Conversation context preservation
- **Object-Oriented Design** - Modular, maintainable code structure

---

## 🎯 How It Works

### 1. Intent Classification
```python
User: "I want rice dishes"
       ↓
Intent Classifier analyzes with regex
       ↓
Intent: "request_category"
Entity: "rice"
```

### 2. Recipe Matching
```python
Intent: "request_category", Category: "rice"
       ↓
Recipe Matcher searches JSON database
       ↓
Results: [Kabsa, Mandi, Bukhari]
```

### 3. Response Generation
```python
Results + User Name + Template
       ↓
Response Generator formats response
       ↓
"Excellent choice, Sarah! Here are amazing rice dishes..."
```

### 4. Session Management
```python
Session State stores:
- User name: "Sarah"
- Conversation history
- Last recipe shown
- Current context
```

---

## 📚 Usage Examples

### Example 1: Getting a Recipe
```
User: Hello, my name is Sarah
Bot: Lovely to meet you, Sarah! 🌟
     What type of dishes interest you?
     🍚 Rice-based dishes
     🥩 Meat dishes
     🍰 Traditional desserts

User: I want rice dishes
Bot: Excellent choice, Sarah! Rice is the heart of Saudi cuisine! 🍚
     [Shows list of rice dishes]

User: Tell me about Kabsa
Bot: [Shows complete Kabsa recipe with ingredients and steps]
```

### Example 2: Finding Similar Dishes
```
User: Similar dishes
Bot: Since you enjoyed Kabsa, you might also like:
     1. Mandi - Smoky rice with tender meat
     2. Bukhari - ...
```

---

## 🎨 Features in Detail

### 🧠 Natural Language Processing
- **Pattern Matching**: Regex-based intent detection
- **Entity Extraction**: Extracts names, dish names, categories
- **Priority System**: Handles multiple intents intelligently
- **Context Awareness**: Understands conversation flow

### 💾 Data Management
- **Recipe Database**: JSON-based storage
- **Template System**: Flexible response generation
- **Session State**: Persistent conversation memory

### 🎨 User Interface
- **Saudi Theme**: Traditional colors (green, gold, beige)
- **Responsive Design**: Works on desktop and mobile
- **Clean Layout**: Easy navigation
- **Custom Styling**: CSS-enhanced appearance

---

## 🔧 Configuration

### Theme Customization
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#006C35"      # Saudi green
backgroundColor = "#F5F5DC"   # Beige/sand
secondaryBackgroundColor = "#FFFACD"  # Light gold
textColor = "#2C1810"         # Dark brown
```

### Adding Recipes
Add to `data/recipes/[category].json`:
```json
{
  "dish_id": {
    "name_en": "Dish Name",
    "name_ar": "اسم الطبق",
    "category": "rice/meat/dessert",
    "ingredients": [...],
    "steps": [...],
    "tips": [...]
  }
}
```

---

## 🤝 Team

- **Rahaf Alshahrani** (UI Developer) - Rahaf Alshahrani
- **Lama Alsubaie** (Recipe Database Specialist)
- **Fouzia** (Intent Classification)
- **Shamah Alshahrani** (Response Generation)

---

## 📈 Future Enhancements

- [ ] Integration with GPT API for more natural responses
- [ ] Voice input/output support
- [ ] Image recognition for dish identification
- [ ] User preference learning
- [ ] Recipe rating system
- [ ] Shopping list generation
- [ ] Multi-language expansion
- [ ] Mobile app version

---

## 🐛 Known Issues

- Limited to predefined patterns (doesn't handle very complex queries)
- Recipe database needs expansion
- Arabic language support is basic (can be improved)

---

## 📝 License

This project is part of a university course assignment.

---

## 🙏 Acknowledgments

- Traditional Saudi recipes from authentic sources
- Streamlit community for excellent documentation
- Our professor for guidance and support

---

## 📞 Contact

For questions or feedback, please contact the team members.

---

## 🌟 Project Highlights

### Architecture
- **Modular Design**: Separated concerns (UI, Logic, Data)
- **Scalable**: Easy to add new recipes and intents
- **Maintainable**: Clean code with clear documentation
- **Extensible**: Simple to add new features

### Performance
- **Fast Response**: <100ms average response time
- **Lightweight**: ~2MB total size
- **Efficient**: Regex-based matching is very fast
- **No External APIs**: Works completely offline

### User Experience
- **Intuitive**: Natural conversation flow
- **Personalized**: Remembers user information
- **Helpful**: Clear guidance and suggestions
- **Beautiful**: Saudi-themed aesthetic design

---

**Made with ❤️ in Saudi Arabia 🇸🇦**
