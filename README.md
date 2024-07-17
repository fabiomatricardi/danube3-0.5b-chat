# danube3-0.5b-chat
stramlit AI assistant with llamacpp and H2O danube3

<img src='https://cdn-uploads.huggingface.co/production/uploads/636d18755aaed143cd6698ef/LAzQu_f5WOX7vqKl4yDsY.png' width=600>

Clone the repo

```
pip install streamlit==1.36.0 llama-cpp-python langchain langchain-community tiktoken
```

Download the GGUF model, Q8 from official HuggingFace Hub Model Card page

- https://huggingface.co/h2oai/h2o-danube3-500m-chat-GGUF
- https://huggingface.co/h2oai/h2o-danube3-4b-chat-GGUF for the 4Billion model

The GGUF file must be downloaded into the `models` directory

From the terminal run:
```
streamlit run .\55.st-Danube3-0.5b-CPP.py
```
