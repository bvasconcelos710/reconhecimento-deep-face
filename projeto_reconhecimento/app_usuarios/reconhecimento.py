import cv2
from deepface import DeepFace

def reconhecer_usuario(imagem, base_fotos):
    for usuario in base_fotos:
        resultado = DeepFace.verify(img1_path=imagem, img2_path=usuario.foto.path, model_name='VGG-Face')
        if resultado['verified']:
            return usuario
    return None
