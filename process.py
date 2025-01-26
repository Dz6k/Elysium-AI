from utils import config
import torch
class ProcessImg:

    @torch.inference_mode()
    def process(self, model, image):
        return model(
            source=image,
            conf=config.confidence,
            imgsz=640,
            iou=0.7,
            nms = False,
            classes=[0],
            max_det=3,
            agnostic_nms=False,
            augment=False   ,
            vid_stride=True,
            visualize=False,
            verbose=False,
            show_boxes=False,
            show_labels=False, 
            show_conf=False,
            save=False,  
            show=False
        )
# import numpy as np
# from utils import config
# class ProcessImg:
#     def process(self, model, image, input_name=None, output_names=None):
#         """
#         Processa a imagem com o modelo ONNX.

#         Args:
#             model: Sessão do modelo ONNX (InferenceSession).
#             image: Imagem de entrada (como um array numpy).
#             input_name: Nome do tensor de entrada no modelo ONNX.
#             output_names: Lista com os nomes dos tensores de saída (se não fornecido, pega todas as saídas).

#         Returns:
#             Saídas da inferência como uma lista.
#         """
#         # Verificar nomes de entrada e saída do modelo
#         input_name = model.get_inputs()[0].name if input_name is None else input_name
#         output_names = [out.name for out in model.get_outputs()] if output_names is None else output_names

#         # Certifique-se de que a imagem está no formato correto (tensor NCHW)
#         # Supondo que a imagem já esteja no formato Numpy Array
#         image = np.expand_dims(image, axis=0).astype(np.float32)

#         # Realizar a inferência com .run()
#         outputs = model.run(None, {input_name: config.frame})
        
#         return outputs[0].squeeze(0)
    
    
# import cv2
# import numpy as np
# import onnxruntime as ort
# import matplotlib.pyplot as plt

# session = ort.InferenceSession("models\w3.onnx")
# image = cv2.imread("122.png")  # Carregar a imagem
# image_resized = cv2.resize(image, (640, 640))  # Redimensionar (ajustar para o tamanho esperado pelo modelo)
# image_resized = image_resized.transpose(2, 0, 1)  # Converter HWC -> CHW
# image_resized = image_resized / 255.0  # Normalizar a imagem para a faixa [0, 1]
# input_data = np.expand_dims(image_resized, axis=0).astype(np.float32)  # Adicionar o batch size

# # 3. Realizar a inferência
# inputs = {session.get_inputs()[0].name: input_data}
# outputs = session.run(None, inputs)
# input(outputs)
# # 4. Verificar e exibir os resultados
# # Supondo que o modelo seja de detecção, a saída pode ter as caixas delimitadoras e classes detectadas.
# # Esse exemplo pode variar dependendo do tipo de modelo ONNX (detecção, classificação, etc.)

# # Exemplo de pós-processamento (ajustar conforme o modelo)
# # Caso o modelo de detecção de objetos retorne as caixas, pontuações e rótulos
# boxes, scores, labels = outputs  # Isso pode variar, veja a documentação do seu modelo

# # Exibir as caixas e rótulos
# for i in range(len(boxes)):
#     if scores[i] > 0.5:  # Filtrar detecções com uma pontuação maior que 0.5
#         x1, y1, x2, y2 = boxes[i]  # Obter coordenadas da caixa delimitadora
#         label = labels[i]
#         cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Desenhar a caixa
#         cv2.putText(image, f"Class: {label}, Score: {scores[i]:.2f}", (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # Exibir a imagem com as caixas delimitadoras
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convertendo de BGR para RGB para exibição no matplotlib
# plt.axis("off")
# plt.show()


# import onnxruntime as ort
# print(ort.get_available_providers())