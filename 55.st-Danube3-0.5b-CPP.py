import streamlit as st
import datetime
import os
from io import StringIO
from rich.markdown import Markdown
import warnings
warnings.filterwarnings(action='ignore')
import datetime
from rich.console import Console
console = Console(width=90)
import tiktoken
import random
import string
from time import sleep

encoding = tiktoken.get_encoding("r50k_base") #context_count = len(encoding.encode(yourtext))

from llama_cpp import Llama

#AVATARS  👷🐦  🥶🌀
av_us = 'man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = 'h2oAI.jpg'

modelname = 'h2o-danube3-500m-chat'
modelfile = 'h2o-danube3-500m-chat-Q8_0.gguf'
# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT with 🌟 {modelname}",
    page_icon="🌟",
    layout="wide")

@st.cache_resource 
def create_chat():   
# Set HF API token  and HF repo
    from llama_cpp import Llama
    llm = Llama(
                model_path='models/h2o-danube3-500m-chat-Q8_0.gguf',
                n_gpu_layers=0,
                temperature=0.1,
                top_p = 0.5,
                n_ctx=8192,
                max_tokens=300,
                repeat_penalty=1.45,
                stop=['</s>'],
                verbose=True,
                )
    print(f'loading {modelfile} with LlamaCPP...')
    return llm

def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()



# Create a header element
mytitle = f'<p style="color:DarkOrange; font-size: 32px;text-align:center;"><b>Your own LocalGPT with 🌟 {modelname}</b></p>'
st.markdown(mytitle, unsafe_allow_html=True)
#st.header("Your own LocalGPT with 🌀 h2o-danube-1.8b-chat")
subtitle = '<p style="color:DeepSkyBlue; font-size: 20px;text-align:center;"><b><i>Powerwed by Danube3-chat - 0.5b parameter model. 8k conext window</i></b></p>'
st.markdown(subtitle, unsafe_allow_html=True)


def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res

# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀{modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')

if "len_context" not in st.session_state:
    st.session_state.len_context = 0

if "limiter" not in st.session_state:
    st.session_state.limiter = 0

if "bufstatus" not in st.session_state:
    st.session_state.bufstatus = "**:green[Good]**"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "repeat" not in st.session_state:
    st.session_state.repeat = 1.2

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

# Point to the local server
llm = create_chat()
 
# CREATE THE SIDEBAR
with st.sidebar:
    st.image('danube3.png', use_column_width=True) #use_column_width=True  #width=170
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.1, step=0.02)
    st.session_state.repeat = st.slider('Repeat Penalty:', min_value=0.0, max_value=2.0, value=1.2, step=0.01)
    #st.session_state.limiter = st.slider('Turns:', min_value=7, max_value=17, value=12, step=1)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=1500, 
                                           value=500, step=50)
    mytokens = st.markdown(f"""**Context turns** {st.session_state.len_context}""")
    st.markdown(f"Context Window: **8k** tokens")
    st.markdown(f"Buffer status: {st.session_state.bufstatus}")
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")
    btnClear = st.button("Clear History",type="primary", use_container_width=True)

# We store the conversation in the session state.
# This will be used to render the chat conversation.
# We initialize it with the first message we want to be greeted with.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Danube3-chat, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",},
        {"role": "user", "content": "Hi, I am Fabio."},
        {"role": "assistant", "content": "Hi there Fabio, I am Danube3-chat: with my 0.5b parameters I can be useful to you. how may I help you today?"}
    ]

def clearHistory():
    st.session_state.messages = [
        {"role": "system", "content": "You are Danube3-chat, a helpful assistant. You reply only to the user questions. You always reply in the language of the instructions.",},
        {"role": "user", "content": "Hi, I am Fabio."},
        {"role": "assistant", "content": "Hi there Fabio, I am Danube3-chat: with my 0.5b parameters I can be useful to you. how may I help you today?"}
    ]
    st.session_state.len_context = len(st.session_state.messages)
if btnClear:
      clearHistory()  
      st.session_state.len_context = len(st.session_state.messages)

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here. Shift+Enter to add a new line", key="user_input"):

    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Add our input to the chat window
    with st.chat_message("user", avatar=av_us):
        st.markdown(user_prompt)
        writehistory(st.session_state.logfilename,f'👷: {user_prompt}')

    
    with st.chat_message("assistant",avatar=av_ass):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            response = ''
            conv_messages = []
            #conv_messages.append({"role": "system", "content": "You are a helpful AI assistant."})
            conv_messages.append(st.session_state.messages[-1])
            st.session_state.len_context = len(st.session_state.messages) 
            st.session_state.bufstatus = "**:green[Good]**"
            full_response = ""
            for chunk in llm.create_chat_completion(
                messages=conv_messages,
                temperature=st.session_state.temperature,
                repeat_penalty= st.session_state.repeat,
                stop=['</s>'],
                max_tokens=st.session_state.maxlength,
                stream=True,):
                try:
                    if chunk["choices"][0]["delta"]["content"]:
                        full_response += chunk["choices"][0]["delta"]["content"]
                        message_placeholder.markdown(full_response + "🌟")                                 
                except:
                    pass                                           
            toregister = full_response + f"""
```

prompt tokens: {len(encoding.encode(st.session_state.messages[-1]['content']))}
generated tokens: {len(encoding.encode(full_response))}
```"""
            message_placeholder.markdown(toregister)
            writehistory(st.session_state.logfilename,f'🌟: {toregister}\n\n---\n\n') 
            
    # Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": toregister}
    )
    st.session_state.len_context = len(st.session_state.messages)
