import streamlit as st
import base64
import json
import zlib

def js_string_to_byte(data):
    return bytes(data, 'ascii')

def js_bytes_to_string(data):
    return data.decode('ascii')

def js_btoa(data):
    return base64.b64encode(data)

def pako_deflate(data):
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8,zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def genPakoLink(graphMarkdown: str):
    jGraph = {
            "code": graphMarkdown,
            "mermaid": {"theme": "default"}
        }
    byteStr = js_string_to_byte(json.dumps(jGraph))
    deflated = pako_deflate(byteStr)
    dEncode = js_btoa(deflated)
    link = 'http://mermaid.live/edit#pako:' + js_bytes_to_string(dEncode)
    return link

# Creazione dell'interfaccia utente
st.title("Mermaid Code Renderer")

# Input del codice Mermaid
mermaid_code = st.text_area("Inserisci il codice Mermaid qui")

# Generazione del link a mermaid.live
if st.button("Genera link"):
    if mermaid_code:
        mermaid_link = genPakoLink(mermaid_code)
        st.success("Ecco il link per il rendering su mermaid.live:")
        st.write(mermaid_link)
    else:
        st.warning("Inserisci il codice Mermaid per generare il link")
