import streamlit as st
import base64
import json
import zlib
import requests

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

def render_mermaid_image(mermaid_code):
    url = "https://mermaid.ink/img/"
    payload = {"code": mermaid_code}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            image_url = response.json().get("url")
            return image_url
        else:
            st.error("Error rendering Mermaid image")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# User Interface Creation
st.title("Mermaid Code Renderer")

# Mermaid code input
mermaid_code = st.text_area("Enter Mermaid code here")

# Generating link to mermaid.live and rendering image
if st.button("Generate link and Render Image"):
    if mermaid_code:
        mermaid_link = genPakoLink(mermaid_code)
        st.success("Here is the link for rendering on mermaid.live:")
        st.write(mermaid_link)
        
        st.success("Here is the rendered image:")
        mermaid_image_url = render_mermaid_image(mermaid_code)
        if mermaid_image_url:
            st.image(mermaid_image_url)
        else:
            st.warning("Failed to render Mermaid image")
    else:
        st.warning("Please enter Mermaid code to generate the link")
