import streamlit as st
import re
import random
from difflib import SequenceMatcher


# ============================================================
# INTENTS
# ============================================================

INTENTS = {

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    "greeting": {
        "keywords": [
            "hi",
            "hello",
            "hey",
            "hii",
            "hiii",
            "goodmorning",
            "goodafternoon",
            "goodevening"
        ],

        "examples": [
            "hi",
            "hello",
            "hey",
            "hi there",
            "hello chatbot",
            "hey chatbot",
            "good morning",
            "good afternoon",
            "good evening"
        ],

        "responses": [
            "Hello! 👋 How can I help you with the college confession page?",
            "Hi! 😊 You can ask me about posting confessions, privacy, reporting, deleting posts, or the website.",
            "Hey! 👋 How can I help you today?"
        ]
    },


    # --------------------------------------------------------
    # POST CONFESSION
    # --------------------------------------------------------

    "post_confession": {
        "keywords": [
            "post",
            "submit",
            "share",
            "write",
            "publish",
            "confession",
            "confess"
        ],

        "examples": [
            "how do I post a confession",
            "how can I post a confession",
            "how to submit a confession",
            "where can I post my confession",
            "I want to post a confession",
            "how can I share my confession",
            "how do I submit a post",
            "how can I write a confession"
        ],

        "responses": [
            "To post a confession, go to the confession section and submit your message using the available form. 📝",
            "You can share your confession through the confession submission section of the website.",
            "Simply open the confession submission form, write your message, and submit it."
        ]
    },


    # --------------------------------------------------------
    # ANONYMITY / PRIVACY
    # --------------------------------------------------------

    "anonymity": {
        "keywords": [
            "anonymous",
            "anonymity",
            "private",
            "privacy",
            "identity",
            "name",
            "secret"
        ],

        "examples": [
            "is my confession anonymous",
            "will my name be shown",
            "is this anonymous",
            "can people see my identity",
            "will my identity be hidden",
            "is my identity private",
            "can I post anonymously",
            "will my name be visible",
            "does anyone know who posted"
            " is it safe "
        ],

        "responses": [
            "Yes, the confession page is designed to allow users to share their thoughts without publicly revealing their identity. 🔒",
            "Your identity should remain private when posting an anonymous confession.",
            "You can share a confession anonymously without displaying your name publicly."
        ]
    },


    # --------------------------------------------------------
    # DELETE CONFESSION
    # --------------------------------------------------------

    "delete_confession": {
        "keywords": [
            "delete",
            "remove",
            "erase",
            "removeconfession"
        ],

        "examples": [
            "how do I delete my confession",
            "can I delete my confession",
            "how can I remove my confession",
            "I want to delete my post",
            "can I remove a confession",
            "how do I remove my post",
            "delete my confession"
        ],

        "responses": [
            "If you want to remove a confession, use the available delete option or contact the page administrator for assistance.",
            "You can request the removal of your confession through the website administrator.",
            "If your confession needs to be deleted, please use the available removal option or contact the administrator."
        ]
    },


    # --------------------------------------------------------
    # REPORT CONFESSION
    # --------------------------------------------------------

    "report_confession": {
        "keywords": [
            "report",
            "abuse",
            "offensive",
            "inappropriate",
            "harassment",
            "spam",
            "fake"
        ],

        "examples": [
            "how do I report a confession",
            "how can I report a post",
            "I want to report a confession",
            "where can I report inappropriate content",
            "how do I report offensive content",
            "can I report a post",
            "this confession is inappropriate",
            "how to report spam"
        ],

        "responses": [
            "If you find inappropriate or offensive content, please use the report option to notify the administrator.",
            "You can report inappropriate content through the reporting option on the website.",
            "If a confession violates the page rules, please report it so that it can be reviewed."
        ]
    },


    # --------------------------------------------------------
    # ABOUT WEBSITE
    # --------------------------------------------------------

    "about_website": {
        "keywords": [
            "website",
            "site",
            "purpose",
            "platform",
            "app"
        ],

        "examples": [
            "what is this website",
            "what is this site",
            "what is this platform",
            "what is this page",
            "what does this website do",
            "what is the purpose of this website",
            "tell me about this website",
            "how does this website work",
            "what is this confession page"
        ],

        "responses": [
            "This website is a college confession platform where students can share their thoughts and experiences.",
            "This page allows college students to share confessions and thoughts with the community.",
            "The purpose of this website is to provide students with a platform to express themselves through confessions."
        ]
    },


    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    "help": {
        "keywords": [
            "help",
            "support",
            "guide",
            "options"
        ],

        "examples": [
            "help me",
            "what can you do",
            "how can you help me",
            "what can I ask",
            "give me some help",
            "what are the options",
            "I need help"
        ],

        "responses": [
            "Sure! 😊 I can help you with posting a confession, privacy, deleting a confession, reporting content, and information about this website.",
            "I can help you understand how the college confession page works.",
            "You can ask me about confessions, privacy, reporting, deleting posts, or the website."
        ]
    },


    # --------------------------------------------------------
    # THANKS
    # --------------------------------------------------------

    "thanks": {
        "keywords": [
            "thanks",
            "thank",
            "thankyou",
            "thx"
        ],

        "examples": [
            "thanks",
            "thank you",
            "thankyou",
            "thanks a lot",
            "thank you so much",
            "thx"
        ],

        "responses": [
            "You're welcome! 😊",
            "No problem! Happy to help. 😊",
            "You're most welcome!"
        ]
    },


    # --------------------------------------------------------
    # CONFIRMATION
    # --------------------------------------------------------

    "confirmation": {
        "keywords": [
            "yes",
            "yeah",
            "yep",
            "sure",
            "okay",
            "ok"
        ],

        "examples": [
            "yes",
            "yeah",
            "yep",
            "sure",
            "okay",
            "ok"
        ],

        "responses": [
            "Great! 😊",
            "Alright!",
            "Sure! 👍"
        ]
    },


    # --------------------------------------------------------
    # GOODBYE
    # --------------------------------------------------------

    "goodbye": {
        "keywords": [
            "bye",
            "goodbye",
            "see",
            "later"
        ],

        "examples": [
            "bye",
            "goodbye",
            "see you",
            "see you later",
            "bye chatbot",
            "goodbye chatbot"
        ],

        "responses": [
            "Goodbye! 👋",
            "See you later! 😊",
            "Take care! 👋"
        ]
    }
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Convert text into a simple normalized form.
    """

    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# SIMILARITY
# ============================================================

def similarity(text1, text2):
    """
    Calculate similarity between two strings.
    Returns a value between 0 and 1.
    """

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(message):
    """
    Find the most suitable intent for the user's message.

    The chatbot checks:
    1. Matching keywords
    2. Similarity with example questions

    If the message appears unrelated to the chatbot,
    it returns None.
    """

    message = clean_text(message)

    # Empty message
    if not message:
        return None

    words = set(message.split())

    best_intent = None
    best_score = 0

    best_keyword_matches = 0
    best_example_score = 0

    # Check every intent
    for intent, data in INTENTS.items():

        # ----------------------------------------------------
        # Keyword matching
        # ----------------------------------------------------

        keyword_matches = len(
            words.intersection(data["keywords"])
        )

        keyword_score = keyword_matches * 0.15

        # ----------------------------------------------------
        # Example similarity
        # ----------------------------------------------------

        example_score = 0

        for example in data["examples"]:

            example = clean_text(example)

            score = similarity(
                message,
                example
            )

            if score > example_score:
                example_score = score

        # ----------------------------------------------------
        # Final score
        # ----------------------------------------------------

        final_score = keyword_score + example_score

        # ----------------------------------------------------
        # Store best intent
        # ----------------------------------------------------

        if final_score > best_score:

            best_score = final_score
            best_intent = intent
            best_keyword_matches = keyword_matches
            best_example_score = example_score

    # ========================================================
    # IMPORTANT:
    # Reject unrelated questions
    # ========================================================

    # If no keywords match, the message must be highly
    # similar to one of our known examples.
    if (
        best_keyword_matches == 0
        and best_example_score < 0.65
    ):
        return None

    # General confidence check
    if best_score < 0.35:
        return None

    return best_intent


# ============================================================
# RESPONSE GENERATOR
# ============================================================

def get_response(message):

    intent = detect_intent(message)

    # --------------------------------------------------------
    # Unknown / unrelated question
    # --------------------------------------------------------

    if intent is None:

        return (
            "I'm sorry, but that doesn't seem to be related "
            "to this page. 😊\n\n"
            "I'm here to help with the college confession "
            "website. You can ask me about posting a "
            "confession, privacy, deleting a post, reporting "
            "content, or how the website works."
        )

    # --------------------------------------------------------
    # Get random response
    # --------------------------------------------------------

    return random.choice(
        INTENTS[intent]["responses"]
    )


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="College Confession Chatbot",
    page_icon="💬",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */

    .stApp {
        background-color: #f5f3ff;
    }


    /* Title */

    .main-title {
        text-align: center;
        color: #4c1d95;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
    }


    /* Subtitle */

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }


    /* Chat container */

    .chat-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    }


    /* Welcome box */

    .welcome {
        background-color: #ede9fe;
        padding: 15px;
        border-radius: 12px;
        color: #4c1d95;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">💬 College Confession Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your friendly assistant for the college confession page</div>',
    unsafe_allow_html=True
)


# ============================================================
# WELCOME MESSAGE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to the College Confession "
                "Chatbot.\n\n"
                "I can help you with posting confessions, "
                "privacy, deleting posts, reporting content, "
                "and information about this website."
            )
        }

    ]


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input(
    "Type your message here..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # Generate chatbot response
    response = get_response(
        user_input
    )


    # Add assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    # Display chatbot response
    with st.chat_message("assistant"):

        st.markdown(
            response
        )
