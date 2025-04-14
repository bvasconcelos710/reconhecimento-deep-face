"""import cv2
from deepface import DeepFace

def reconhecer_usuario(imagem, base_fotos):
    for usuario in base_fotos:
        resultado = DeepFace.verify(img1_path=imagem, img2_path=usuario.foto.path, model_name='VGG-Face')
        if resultado['verified']:
            return usuario
    return None
"""
import cv2
import numpy as np
from deepface import DeepFace

def reconhecer_usuario(imagem_upload, usuarios):
    print("Tipo da imagem recebida:", type(imagem_upload))  # Deve ser InMemoryUploadedFile
    # Lê o conteúdo da imagem em memória
    imagem_bytes = imagem_upload.read()
    np_array = np.frombuffer(imagem_bytes, np.uint8)
    imagem_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    print("Formato da imagem convertida:", imagem_np.shape)

    for usuario in usuarios:
        try:
            resultado = DeepFace.verify(
                img1_path=usuario.foto.path,  # caminho da imagem do usuário cadastrado
                img2_path=imagem_np,          # imagem capturada via webcam convertida
              
            )
            print(f"Resultado com {usuario.nome}: {resultado}")
            if resultado['verified']:
                return usuario
        except Exception as e:
            print(f"Erro na comparação: {e}")
            continue

    return None
