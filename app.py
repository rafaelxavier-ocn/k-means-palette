import io
import streamlit as st
from pathlib import Path
from matplotlib.colors import to_hex
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans


def get(imagem_carregada,n_cores):
    # salvar a imagem do streamlit
    with open('imagem.jpg', 'wb') as file:
        file.write(imagem_carregada.getbuffer())
    # Ler a imagem
    image = Image.open('imagem.jpg')
    # Transformas os pixels em linhas de uma matriz
    N, M = image.size
    X = np.asarray(image).reshape((M*N, 3))
    # Criar e aplicar o k-means na imagem
    model = KMeans(n_clusters=n_cores, random_state=42).fit(X)

    # Capturar os centros (cores médias dos grupos)
    cores = model.cluster_centers_.astype('uint8')[np.newaxis]
    

    # Apagar imagem salva
    Path('imagem.jpg').unlink()
    # Gerar paleta
    cores_hex = [to_hex(cor/255) for cor in cores[0]]
    return cores, cores_hex

def show(cores):
    fig = plt.figure()
    plt.imshow(cores)
    plt.axis('off')
    return fig

def save(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    plt.axis("off")
    return img

st.title("Gerador de paletas")
imagem = st.file_uploader("Envie sua imagem", ["jpg","jpeg"])

col1, col2 = st.columns(2)

if imagem:
    col1.image(imagem)
    n_cores = col2.slider(
            "Quantidade de cores",
            min_value=2,
            max_value=10,
            value=5
    )
    botao_gerar_paleta = col2.button("Gerar paleta")
        
    if botao_gerar_paleta:
        cores, cores_hex = get(imagem, n_cores)
        figura = show(cores)
        col2.pyplot(fig=figura)
        col2.code(f"{cores_hex}")
        
        col2.download_button(
        "Download",
        save(figura),
        "paleta.png",
        "image/png"
        )