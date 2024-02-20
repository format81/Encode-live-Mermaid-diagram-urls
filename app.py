import streamlit as st
import base64
import json
import zlib
from streamlit.components.v1 import iframe

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

# User Interface Creation
st.title("Mermaid Code Renderer")

# Mermaid code input
mermaid_code = st.text_area("Enter Mermaid code here")

# Generating link to mermaid.live
if st.button("Generate link"):
    if mermaid_code:
        mermaid_link = genPakoLink(mermaid_code)
        st.success("Here is the link for rendering on mermaid.live:")
        st.write(mermaid_link)
        st.markdown(f'<iframe src="{mermaid_link}" height="600" width="100%"></iframe>', unsafe_allow_html=True)
    else:
        st.warning("Please enter Mermaid code to generate the link")
