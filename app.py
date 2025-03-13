import streamlit as st
from chatbot import Chatbot
from profiler import GeminiProfiler

# Set page configuration to use wide mode.
st.set_page_config(page_title="Clarification Tree Chatbot", layout="wide")

# Inject custom CSS for chat message styling
st.markdown("""
    <style>
    .chat-container {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 95%;
        word-wrap: break-word;
        color: black;
    }
    .user-msg {
        background-color: #DCF8C6;
        margin-left: auto;
        text-align: right;
    }
    .bot-msg {
        background-color: #F1F0F0;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_chatbot(example_file_path, language):
    """
    Initializes the chatbot instance with the content from the given file.
    Resets the conversation history.
    """
    try:
        with open(example_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        content = ""

    st.session_state.chatbot_instance = Chatbot(language, content)
    st.session_state.chat_history = []


def on_example_change():
    """
    Callback triggered when the example text selection changes.
    Reinitializes the chatbot instance with the newly selected example.
    """
    selected_title = st.session_state.selected_example
    file_path = example_texts[selected_title]
    language = example_texts_languages[selected_title]
    initialize_chatbot(file_path, language)


# Initialize session state variables if they don't exist yet
if "chatbot_instance" not in st.session_state:
    st.session_state.chatbot_instance = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Layout: Two columns, left for chat and right for example selection.
left_col, right_col = st.columns([1, 1])

with right_col:
    st.header("Example Text Display")

    # Provide a dropdown menu to select one of the example texts
    example_texts = {
        "City Taxes Elders": "examples/city_taxes_elders.txt",
        "Israel Hiking": "examples/israel_hikings.txt",
        "Pregnancy Vacation": "examples/pregnancy_vacation.txt",
        "Special Allowance Immigrants": "examples/special_allowance_immigrants.txt",
        "Teeth Military": "examples/teeth_military.txt",
        "Youth Public Transport": "examples/youth_public_transport.txt",
    }
    # Provide a dropdown menu to select one of the example texts
    example_texts_languages = {
        "City Taxes Elders": "Hebrew",
        "Israel Hiking": "English",
        "Pregnancy Vacation": "Hebrew",
        "Special Allowance Immigrants": "Hebrew",
        "Teeth Military": "Hebrew",
        "Youth Public Transport": "Hebrew",
    }

    # The selectbox displays example titles; on change, it triggers reinitialization.
    selected_example = st.selectbox("Choose an example text to display and ask a question about it:",
                                    list(example_texts.keys()),
                                    key="selected_example",
                                    on_change=on_example_change)

    # Display the content of the selected text
    try:
        with open(example_texts[selected_example], 'r', encoding='utf-8') as file:
            text_content = file.read()
            st.text_area("Example Text:", text_content, height=400)
    except FileNotFoundError:
        st.error("The selected example text file could not be found.")

with left_col:
    st.header("Clarification Tree Chatbot")

    # Input field for the user's message.
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:")
        submitted = st.form_submit_button("Send")

    if example_texts_languages[st.session_state.selected_example] == "Hebrew":
        st.markdown(
            '<div class="chat-container bot-msg"><strong>Bot:</strong> שלום! מה השאלה שלך על הטקסט המוצג?</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="chat-container bot-msg"><strong>Bot:</strong> Hello! What is your question about the displayed text?</div>',
            unsafe_allow_html=True
        )

    if submitted:
        # If chatbot instance hasn't been initialized, use the first example.
        if st.session_state.chatbot_instance is None:
            initialize_chatbot(example_texts[st.session_state.selected_example],
                               example_texts_languages[st.session_state.selected_example])

        # Process the user's input and get the chatbot's response.
        next_question, answer = st.session_state.chatbot_instance.get_response(user_input)
        # Append the interaction to the conversation history.
        st.session_state.chat_history.append(("User", user_input))
        if next_question is not None:
            chat_response = next_question
        else:
            chat_response = answer
        st.session_state.chat_history.append(("Chat", chat_response))

    # Display the entire conversation history.
    for sender, message in st.session_state.chat_history:
        if sender == "User":
            st.markdown(
                f'<div class="chat-container user-msg"><strong>You:</strong> {message}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-container bot-msg"><strong>Bot:</strong> {message}</div>',
                unsafe_allow_html=True
            )
