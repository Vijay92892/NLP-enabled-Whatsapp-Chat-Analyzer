# GEMINI API KEY
# AIzaSyCAigjfZNs2VnUEz6ZINBhsWmHj2vux4Lk

#use python 3.7
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from openai import *


st.sidebar.title("Whats-app chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data) # DATAFRAME
    
    from ollama import Client
    model_name = st.sidebar.selectbox("Choose local model", ["llama3", "mistral", "codellama"]) # CHOOSE MODEL NAME

    client = Client(host='http://localhost:11434')  # default Ollama serve

    # Initialize limited memory if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    # st.write("-----------------")
    with st.expander("## 🤖 Chat with AI (Limited Memory)"):
        for msg in st.session_state.chat_history[-5:]:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # Get limited AI Response
        def get_limited_ai_response(user_query, chat_df, history,model_name):
            df_preview = chat_df.head(10).to_string(index=False)

            # Use last 5 messages from history for memory
            limited_context = history[-20:] if len(history) > 20 else history
            messages = [{"role": "system", "content": f"You are a helpful WhatsApp chat analyst. Here's the chat preview:\n{df_preview}"}]
            messages += limited_context
            messages.append({"role": "user", "content": user_query})

            response = client.chat(
                model=model_name,  # or mistral, codellama, etc.
                messages=messages
            )
            return response["message"]["content"].strip()
        # Input box
        if prompt := st.chat_input("Ask about the chat..."):
            st.chat_message("user").write(prompt)

            # Generate response using your local LLM
            with st.spinner("Thinking..."):
                response = get_limited_ai_response(prompt, df, st.session_state.chat_history, model_name)

            # Display response and save to history
            st.chat_message("assistant").write(response)

            # Append both user input and assistant response to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    #------------------->>>>>>>>>>>>>>>>>>>>>>>>>




###################33
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # stores messages as {"role": "user"/"assistant", "content": "..."}

    from ollama import Client
    import matplotlib.pyplot as plt
    import io
   
    import re

    def extract_python_code(text):
        """
        Extracts the Python code block from a string.
        It supports markdown-style fenced blocks and ignores extra text like 'Here is the answer:'
        """
        # Look for markdown-style code blocks
        code_blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()

        # Fallback: remove non-code lines like explanations or comments
        lines = text.strip().splitlines()
        code_lines = [line for line in lines if not line.lower().startswith("here is") and not line.startswith("```")]
        return "\n".join(code_lines)

    def run_code_or_text_response(user_query, chat_df):
        client = Client(host="http://localhost:11434")
        df_preview = chat_df.head(10).to_string(index=False)
        system_prompt = f"""
    You are a helpful AI data analyst. Based on this WhatsApp chat DataFrame preview:
    {df_preview}
    Answer the following question. If needed, generate a Python plot using matplotlib. Return ONLY code if it's a plot.
    """
        messages = [{"role": "user", "content": system_prompt + "\n\nQuestion: " + user_query}]
        result = client.chat(model=model_name, messages=messages)
        content = result["message"]["content"]
        # Check if it's code
        if "plt." in content or "import matplotlib" in content:
            try:
                code = extract_python_code(content)
                exec_globals = {"df": chat_df, "chat_df": chat_df, "plt": plt}
                exec(code, exec_globals)
                # Render plot
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                st.image(buf, caption="📊 AI-generated chart")
                # plt.clf()
                return "✅ Plot generated."
            except Exception as e:
                return f"❌ Error in generated code:\n\n```python\n{code}\n```\n\nException:\n`{e}`"
        else:
            return content
        

    st.markdown("## 🤖 Chat with the AI Assistant")

    # Display chat history (limit to last 6)
    for msg in st.session_state.chat_history[-6:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    if user_input := st.chat_input("Ask anything about the chat (e.g., 'Plot messages per hour')"):
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate response using your llama3 model
        with st.spinner("Thinking..."):
            response = run_code_or_text_response(user_input, df)

        # Show response
        st.chat_message("assistant").markdown(response if isinstance(response, str) else "📊 See generated plot above 👆")
        st.session_state.chat_history.append({"role": "assistant", "content": response if isinstance(response, str) else "Generated a plot!"})


        




    with st.sidebar.expander("💬 Ask the AI Assistant"):
        user_query = st.text_input("Ask about the chat", placeholder="e.g., Who sends the most messages after midnight?")
        if st.button("Ask"):
            if user_query:
                response = get_ai_response(user_query, df)  # We'll define this next
                st.session_state.ai_outpput = response
    # st.write(st.session_state.ai_outpput,'\n\n\n')
    ####*********************************************************************####
    ####*********************************************************************####



    # RESULT    

    # DATA PLOTS
    st.dataframe(df)

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notificatioin')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("show analysis wrt ", user_list)

    if st.sidebar.button("Show Analysis"):
        #stats area

        num_messages, num_words, num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("No. of media")
            st.title(num_media_messages)
        with col4:
            st.header("No. of links")
            st.title(num_links)      


        #finding the bussiest user in group
        if selected_user == 'Overall':
            st.title('Most busy users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)  
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        #Word Cloud
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        most_common_words = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        plt.xticks(rotation="vertical")
        ax.barh(most_common_words[0],most_common_words[1])
        st.pyplot(fig)


            