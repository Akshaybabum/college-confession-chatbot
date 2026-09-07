import streamlit as st
import re
import random
from difflib import SequenceMatcher


# ============================================================
# COLLEGE CONFESSION CHATBOT
# ============================================================

INTENTS = {

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------
    "greeting": {
        "keywords": [
            "hello", "hi", "hey", "hai", "hii", "hiii",
            "morning", "evening", "afternoon"
        ],

        "examples": [
            "hello",
            "hi",
            "hey",
            "hey there",
            "hi there",
            "hii",
            "hiii",
            "hai",
            "hello chatbot",
            "hi bot",
            "hey bot",
            "good morning",
            "good afternoon",
            "good evening"
        ],

        "responses": [
            "Hello! 👋 How can I help you?",
            "Hi! 😊 What can I help you with?",
            "Hey! 👋 I'm your College Confession Assistant.",
            "Hello! Feel free to ask me anything about the confession website."
        ]
    },


    # --------------------------------------------------------
    # POST CONFESSION
    # --------------------------------------------------------
    "post_confession": {
        "keywords": [
            "post", "submit", "send", "share",
            "confession", "write", "publish",
            "upload", "create"
        ],

        "examples": [
            "How do I post a confession?",
            "Where can I submit a confession?",
            "I want to share a confession",
            "How can I post something?",
            "I want to write a confession",
            "How do I submit my confession?",
            "Where do I write my confession?",
            "Can I post something?",
            "Can I share my thoughts?",
            "I want to submit a post",
            "How can I share a post?",
            "Where can I publish my confession?",
            "How do I create a confession?",
            "I want to tell my story",
            "I want to share something",
            "How can I send my confession?",
            "Where can I post?",
            "I want to submit something"
        ],

        "responses": [
            "You can submit your confession using the confession form on the website.",
            "To share a confession, open the confession submission section and write your message.",
            "Sure! You can share your thoughts by submitting a confession through the website.",
            "Want to post something? Go to the confession submission section and enter your message."
        ]
    },


    # --------------------------------------------------------
    # ANONYMITY / PRIVACY
    # --------------------------------------------------------
    "anonymity": {
        "keywords": [
            "anonymous", "anonymity", "identity",
            "name", "private", "privacy",
            "secret", "hidden", "visible"
        ],

        "examples": [
            "Is my confession anonymous?",
            "Will people know my name?",
            "Can others see my identity?",
            "Is my identity hidden?",
            "Will my name be shown?",
            "Can people find out who posted?",
            "Is this anonymous?",
            "Will my identity be revealed?",
            "Can anyone see my name?",
            "Is my confession private?",
            "Will others know it is me?",
            "Can my friends know who posted?",
            "Does the confession show my name?",
            "Is my post private?",
            "Can people see who submitted it?",
            "Will everyone know who posted this?",
            "Is my identity safe?"
        ],

        "responses": [
            "The public confession should not display your identity. Check the website's privacy rules for the exact details.",
            "Privacy is important for confessions. The public post is intended to be separate from your identity.",
            "Your identity and privacy depend on how the website's submission system is configured. Check the privacy information before posting."
        ]
    },


    # --------------------------------------------------------
    # DELETE CONFESSION
    # --------------------------------------------------------
    "delete_confession": {
        "keywords": [
            "delete", "remove", "erase",
            "confession", "post", "clear"
        ],

        "examples": [
            "How can I delete my confession?",
            "I want to remove my post",
            "Can I delete a confession?",
            "How do I remove my confession?",
            "I want to delete my post",
            "Can I remove something I posted?",
            "How can I erase my confession?",
            "I posted something by mistake",
            "Can I remove my confession?",
            "I want to take down my post",
            "I don't want my confession anymore",
            "Can my confession be removed?",
            "How do I delete something I posted?"
        ],

        "responses": [
            "If you want to remove a confession, use the available delete option or contact the website administrator.",
            "Posted something by mistake? Check whether a delete option is available, or contact the administrator.",
            "You can request removal of a confession from the website administrator if a delete option isn't available."
        ]
    },


    # --------------------------------------------------------
    # REPORT CONFESSION
    # --------------------------------------------------------
    "report_confession": {
        "keywords": [
            "report", "abuse", "offensive",
            "spam", "inappropriate", "bad",
            "harmful", "fake"
        ],

        "examples": [
            "How do I report a confession?",
            "I want to report a post",
            "This confession is inappropriate",
            "How can I report spam?",
            "I found an offensive post",
            "How do I report something?",
            "Can I report a confession?",
            "Where can I report a post?",
            "This post is bad",
            "Someone posted something inappropriate",
            "I want to report this confession",
            "How can I report abuse?",
            "This is spam",
            "I found a harmful confession",
            "Where is the report option?"
        ],

        "responses": [
            "You can report inappropriate or harmful content using the report option provided on the website.",
            "If you find a confession inappropriate, use the report option so it can be reviewed.",
            "You can report spam, offensive or inappropriate content through the website's reporting option."
        ]
    },


    # --------------------------------------------------------
    # ABOUT WEBSITE
    # --------------------------------------------------------
    "about_website": {
        "keywords": [
            "website", "site", "purpose",
            "about", "college", "confession",
            "platform", "app"
        ],

        "examples": [
            "What is this website?",
            "What is this site about?",
            "What is the purpose of this website?",
            "Tell me about the confession page",
            "What is this platform?",
            "Why was this website created?",
            "What can I do on this website?",
            "What is the confession page?",
            "Tell me about this site",
            "How does this website work?",
            "What is this app?",
            "Why do we have this website?",
            "What is the purpose of this page?"
        ],

        "responses": [
            "This is a college confession platform where students can share their thoughts, experiences and confessions.",
            "The website allows college students to share confessions and thoughts with the college community.",
            "It's a platform designed for students to express their thoughts and experiences through confessions."
        ]
    },


    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------
    "help": {
        "keywords": [
            "help", "options", "assist",
            "support", "guide"
        ],

        "examples": [
            "What can you help me with?",
            "What can I ask you?",
            "I need help",
            "Show me what you can do",
            "Can you help me?",
            "How can you help?",
            "What are your options?",
            "I need some help",
            "Help me",
            "What questions can I ask?",
            "What can you do?",
            "How do you help?"
        ],

        "responses": [
            "I can help you with posting confessions, privacy, deleting or reporting posts, and information about this website.",
            "You can ask me about posting a confession, anonymity, deleting a post, reporting content, or the website.",
            "I'm here to help! Ask me about confessions, privacy, reports, deleting posts, or the website."
        ]
    },


    # --------------------------------------------------------
    # THANKS
    # --------------------------------------------------------
    "thanks": {
        "keywords": [
            "thanks", "thank", "thankyou",
            "appreciate", "helpful"
        ],

        "examples": [
            "thanks",
            "thank you",
            "thanks a lot",
            "thankyou",
            "thank you so much",
            "that was helpful",
            "thanks for helping",
            "appreciate it",
            "very helpful",
            "thank you so much",
            "thanks bot",
            "thank you bot"
        ],

        "responses": [
            "You're welcome! 😊",
            "No problem! Happy to help. 👍",
            "You're welcome! Feel free to ask anything else.",
            "Glad I could help! 😊"
        ]
    },


    # --------------------------------------------------------
    # OK / YES / CONFIRMATION
    # --------------------------------------------------------
    "confirmation": {
        "keywords": [
            "ok", "okay", "okk", "okayy",
            "yes", "yeah", "yep", "yaa", "ya",
            "sure", "alright", "fine",
            "cool", "nice", "great"
        ],

        "examples": [
            "ok",
            "okay",
            "okk",
            "okayy",
            "okayyy",
            "yes",
            "yeah",
            "yep",
            "yaa",
            "ya",
            "sure",
            "alright",
            "fine",
            "cool",
            "nice",
            "great",
            "okay thanks",
            "yes please",
            "yeah sure",
            "yaa okay",
            "ok fine",
            "cool thanks",
            "nice"
        ],

        "responses": [
            "Okay! 😊",
            "Sure! 👍",
            "Alright!",
            "Great! How can I help you next?",
            "Got it! 😊"
        ]
    },


    # --------------------------------------------------------
    # GOODBYE
    # --------------------------------------------------------
    "goodbye": {
        "keywords": [
            "bye", "goodbye", "exit",
            "quit", "later"
        ],

        "examples": [
            "bye",
            "goodbye",
            "see you",
            "see you later",
            "I have to go",
            "talk to you later",
            "bye bye",
            "good night",
            "see ya",
            "bye bot"
        ],

        "responses": [
            "Goodbye! 👋 Have a great day!",
            "See you later! 👋",
            "Bye! 😊 Take care!"
        ]
    }
}


# ============================================================
# CLEAN USER MESSAGE
# ============================================================

def clean_text(text):
    """
    Convert the user's message into a simple format.
    """

    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# TEXT SIMILARITY
# ============================================================

def similarity(text1, text2):
    """
    Compare two sentences and return a similarity score.
    """

    return SequenceMatcher(None, text1, text2).ratio()


# ============================================================
# DETECT INTENT
# ============================================================

def detect_intent(message):
    """
    Find the most suitable intent for the user's message.
    """

    message = clean_text(message)

    words = set(message.split())

    best_intent = None
    best_score = 0

    for intent, data in INTENTS.items():

        # ---------------------------------------------
        # Check matching keywords
        # ---------------------------------------------

        keyword_matches = len(
            words.intersection(data["keywords"])
        )

        keyword_score = keyword_matches * 0.15


        # ---------------------------------------------
        # Compare message with example questions
        # ---------------------------------------------

        example_score = 0

        for example in data["examples"]:

            example = clean_text(example)

            score = similarity(message, example)

            if score > example_score:
                example_score = score


        # ---------------------------------------------
        # Calculate final score
        # ---------------------------------------------

        final_score = keyword_score + example_score


        # ---------------------------------------------
        # Store best intent
        # ---------------------------------------------

        if final_score > best_score:

            best_score = final_score
            best_intent = intent


    # ---------------------------------------------
    # Confidence check
    # ---------------------------------------------

    if best_score < 0.35:

        return None


    return best_intent


# ============================================================
# GET RESPONSE
# ============================================================

def get_response(message):
    """
    Generate a response for the user's message.
    """

    intent = detect_intent(message)

    # If chatbot doesn't understand
    if intent is None:

        return (
            "I'm not sure I understood that. 🤔\n"
            "You can ask me about posting a confession, "
            "privacy, deleting a post, reporting content, "
            "or the confession website."
        )

    # Select a random response
    return random.choice(
        INTENTS[intent]["responses"]
    )


# ============================================================

# ============================================================
# STREAMLIT WEB APP
# ============================================================

st.set_page_config(
    page_title="College Confession Assistant",
    page_icon="💬",
    layout="centered"
)

st.title("💬 College Confession Assistant")
st.write("Ask me anything about the confession website!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_message = st.chat_input("Type your message...")

if user_message:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.write(user_message)

    # Generate and display bot response
    response = get_response(user_message)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)
