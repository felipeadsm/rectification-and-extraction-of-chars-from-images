# A princípio foi determinado a escolha da melhor posição do braço robótico para que a influência da luz externa
# não criasse reflexão e o angulo fosse compatível com a angulação da tela do terminal. Desta forma minimizamos a
# interferência desses fatores, diminuindo a necessidade de mais processos que melhorem a eficiência do OCR.
# Foi utilizado o easyocr, pois durante a fase de estudo apresentou melhores resultados em relação ao tesseract.
# O opencv e o numpy foram utilizados no código para o tratamento e processamento das imagens.

import easyocr
import cv2
import numpy as np
from Rectify import Rectify


# Criar função para destacar arestas e pegar a área da tela
def detect_contours(image_source, image_contour):
    n = 0

    contours, hierarchy = cv2.findContours(image_source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = 11000
        if area > areaMin:
            cv2.drawContours(image_contour, cnt, -1, (255, 0, 255), 7)
            perimeter = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

            n = approx.ravel()
            i = 0

            for _ in n:
                if i % 2 == 0:
                    x = n[i]
                    y = n[i + 1]
                    string = str(x) + " " + str(y)

                    if i == 0:
                        cv2.putText(image_contour, "Arrow tip", (x, y),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
                    else:
                        cv2.putText(image_contour, string, (x, y),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                i = i + 1
    print(n)
    return n


# Criar função para retificar a imagem de acordo com a área da tela
def rectify_AOI(image_source):
    final = Rectify(image_source).Rectify()

    return final


# Criar função para realizar o pré-processamento
def preProcessing(image_source):
    image_blur = cv2.medianBlur(image_source, 5)
    image_pre_process = cv2.adaptiveThreshold(image_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
    imageBilateral = cv2.bilateralFilter(image_pre_process, 20, 200, 250)

    return imageBilateral


# Criar função para aplicar o easy OCR e retornar o que foi lido
def apply_easy_OCR(image_source):
    reader = easyocr.Reader(['pt', 'en'])
    result = reader.readtext(image_source, detail=0)

    return result


# Criar função para escrever a saída do OCR em um arquivo
def generate_relatory(text_read):
    nameOutputArchive = r'Output.txt'  # mudar o caminho para o pc de execução
    outputArchive = open(nameOutputArchive, 'w')
    outputArchive.write(str(text_read))
    outputArchive.close()


# Primeiro fazemos a leitura da imagem baixada através desse link
# https://drive.google.com/drive/folders/1_tO59D1lwHeezLvmAQQY5xCk9yWhMblH?usp=sharing
# Lembrar de baixar a imagem e colocar na pasta resources
image = cv2.imread('Resources/P4.7.jpg', 1)  # Mudar o caminho da fot6

# Redefinimos o tamanho da imagem, pois isso melhorou a eficiència do OCR para nossa imagem
image = cv2.resize(image, (900, 600))

# Criamos uma cópia da imagem para não alterar a imagem original
imageContour = image.copy()

# Aplicamos um filtro de borramento Gaussiano para reduzir o ruído
imageBlur = cv2.GaussianBlur(image, (7, 7), 1)

# Transformamos o espaço de cor da imagem original para GRAY para poder aplicar o detector de bordas de Canny.
imageGray = cv2.cvtColor(imageBlur, cv2.COLOR_BGR2GRAY)

# Canny foi utilizado, pois, apresentaram melhores resultado em comparação com o Sobel.
imageCanny = cv2.Canny(imageGray, 70, 210, 3)

# Foi utilizado uma dilatação para melhorar as bordas
kernel = np.ones((5, 5))
imageDilate = cv2.dilate(imageCanny, kernel, iterations=1)

# Função utilizada para definir a área da tela e os pontos de interesse
frame = detect_contours(imageDilate, imageContour)

# Aqui nós passamos os pontos de interesse da tela para fazer a retificação da imagem para melhorar ainda mais
# a eficiência do OCR.
rectifyImage = rectify_AOI(image)

rectifyImage = cv2.resize(rectifyImage, (1380, 300))

# Com a imagem retifcada nós passamos ela para gray para aplicarmos a função de pré-processamento definida após
# alguns testes
rectifyImage = cv2.cvtColor(rectifyImage, cv2.COLOR_BGR2GRAY)

# Primeiro é feito um borramento para suavização, depois uma binarização da imagem e em seguida aplicamos um filtro
# lateral para retirar mais ruído, preservando as bordas
imagePreProcess = preProcessing(rectifyImage)

# Por fim, aplicamos o Easyocr
textReader = apply_easy_OCR(imagePreProcess)

# E escrevemos o seu resultado em um arquivo txt
generate_relatory(textReader)
print(textReader)

# Visando o chão de fábrica nós precisamos apenas que o OCR consiga extrair corretamente
# o título que aparece na tela para podermos comparar com a entrada.
while True:
    cv2.imshow('Input', rectifyImage)
    cv2.imshow('Output', imagePreProcess)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
