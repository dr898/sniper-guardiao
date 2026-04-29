import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- CONFIGURAÇÃO ---
# Aqui vais colocar a tua API Key do Google AI Studio mais tarde
st.set_page_config(page_title="Sniper Guardião", page_icon="🎯")
st.title("🎯 Sniper Guardião")

api_key = st.text_input("Insere a tua API Key do Google AI:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    ativo = st.selectbox("Seleciona o ativo:", ["AUD/CAD", "USD/CNY", "USD/JPY", "AUD/USD"])
    zona_alvo = st.number_input("Zona de Interesse:", value=0.9600, format="%.4f")

    camera_file = st.camera_input("Aponta a câmara para o gráfico")

    if camera_file:
        img = Image.open(camera_file)
        st.image(img, caption="Gráfico capturado", use_column_width=True)
        
        with st.spinner("O Guardião está a analisar o gráfico..."):
            prompt = f"Lê o preço atual do ativo {ativo} neste gráfico. Responde apenas com o valor numérico."
            response = model.generate_content([prompt, img])
            
            try:
                preco_atual = float(response.text.strip())
                st.success(f"Preço detetado: {preco_atual}")
                
                # Lógica de Sniper
                if abs(preco_atual - zona_alvo) < (zona_alvo * 0.002):
                    st.balloons()
                    st.error("🎯 ALERTA SNIPER: O preço está na tua zona de valor!")
                else:
                    st.info("O preço ainda não está na zona. Mantém a paciência.")
            except:
                st.error("Não consegui ler o preço. Tenta tirar uma foto mais nítida do eixo do preço.")
