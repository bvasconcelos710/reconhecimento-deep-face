import cv2
import numpy as np
from deepface import DeepFace

def reconhecer_reu(imagem_upload, reus):
    # Lê o conteúdo da imagem em memória
    imagem_bytes = imagem_upload.read()
    np_array = np.frombuffer(imagem_bytes, np.uint8)
    imagem_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    print("Formato da imagem convertida:", imagem_np.shape)

    for reu in reus:
        try:
            resultado = DeepFace.verify(
                img1_path=reu.foto.path, 
                img2_path=imagem_np,          
              
            )
            print(f"Resultado com {reu.nome}: {resultado}")
            if resultado['verified']:
                return reu
        except Exception as e:
            print(f"Erro na comparação: {e}")
            continue

    return None
