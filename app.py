import streamlit as st
import streamlit.components.v1 as components


def main():
    # Initialize the chatbot
    chatbot = Chatbot()

    # Set wide layout for side-by-side columns
    st.set_page_config(layout="wide")
    st.title("Chatbot UI")

    # Create two columns: left for chat, right for website display
    left_col, right_col = st.columns(2)

    # --- Right Column: Website Display ---
    with right_col:
        st.header("Text Display")
        # Provide a dropdown menu to select one of the example texts
        example_texts = {
            "Example 1": "examples/example1.txt",
            "Example 2": "examples/example2.txt",
            "Example 3": "examples/example3.txt",
            "Example 4": "examples/example4.txt",
            "Example 5": "examples/example5.txt",
        }

        selected_example = st.selectbox("Choose an example text to display:", list(example_texts.keys()))

        # Display the content of the selected text
        try:
            with open(example_texts[selected_example], 'r', encoding='utf-8') as file:
                text_content = file.read()
                st.text_area("Example Text:", text_content, height=400)
        except FileNotFoundError:
            st.error("The selected example text file could not be found.")

    # --- Left Column: Chat Conversation ---
    with left_col:
        st.header("PACQGPT (Pro-Active Clarification Question Chatbot)")

        # Initialize session state for conversation messages if not already present.
        if "messages" not in st.session_state:
            st.session_state.messages = []  # Each message is a tuple: (role, text)

        # Display the conversation history
        for role, message in st.session_state.messages:
            if role == "user":
                st.markdown(f"**User:** {message}")
            else:
                st.markdown(f"**Bot:** {message}")

        # Input for new user message
        user_message = st.text_input("Your message:", key="user_message")
        if st.button("Send"):
            if user_message.strip():
                # Append the user message to conversation history
                st.session_state.messages.append(("user", user_message))

                # Placeholder: simulate a bot response.
                # Replace the following line with a call to your own model.
                next_question, answer = chatbot.get_response(user_message)

                if next_question is not None:
                    bot_response = next_question
                else:
                    bot_response = answer
                st.session_state.messages.append(("bot", bot_response))

                # Rerun to update the UI
                st.experimental_rerun()


if __name__ == "__main__":
    main()
