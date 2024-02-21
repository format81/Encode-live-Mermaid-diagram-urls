import streamlit as st
import base64
import json
import zlib

def js_btoa(data):
    return base64.b64encode(data)

def pako_deflate(data):
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def genPakoLink(graphMarkdown: str):
    jGraph = {"code": graphMarkdown, "mermaid": {"theme": "default"}}
    byteStr = json.dumps(jGraph).encode('utf-8')
    deflated = pako_deflate(byteStr)
    dEncode = js_btoa(deflated)
    link = 'http://mermaid.live/edit#pako:' + dEncode.decode('ascii')
    return link

# Sidebar content
st.sidebar.title("Project Info")
st.sidebar.write("This is a simple Streamlit app for rendering Mermaid diagrams.")
st.sidebar.write("Contact: antonio.formato@gmail.com")
st.sidebar.write("[GitHub Repository](https://github.com/format81/Encode-live-Mermaid-diagram-urls)")
st.sidebar.write("[Mermaid.js](https://mermaid.js.org/intro/)")
st.sidebar.write("[TI Mindmap - GitHub](https://github.com/format81/TI-Mindmap-GPT)")
st.sidebar.write("[TI Mindmap - Streamlit App](https://ti-mindmap-gpt.streamlit.app/)")

st.markdown(
        "If you find this small project useful, follow me on [LinkedIn]https://www.linkedin.com/in/antonioformato/ and give me a ⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/format81/Encode-live-Mermaid-diagram-urls?style=social)](https://github.com/format81/Encode-live-Mermaid-diagram-urls)"
    )."
    )


# Main interface
st.title("Mermaid.live Code Renderer")

# Mermaid code input
mermaid_code = st.text_area("Enter Mermaid code here")

# Generating link to mermaid.live
if st.button("Generate link"):
    if mermaid_code:
        mermaid_link = genPakoLink(mermaid_code)
        st.success("Here is the link for rendering on mermaid.live:")
        st.write(mermaid_link)
    else:
        st.warning("Please enter Mermaid code to generate the link")
