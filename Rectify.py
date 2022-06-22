import cv2
import numpy as np


class Rectify:
    def __init__(self, frame):
        self.frame = frame

    def Rectify(self):
        try:
            areas, list_points, area_aux, points_aux, point1, point4, aux1, aux2 = [], [], 0, 0, 0, 0, [], []

            # Pré-processamentos necessários para destacar borda e retificar a imagem.
            image_blur = cv2.GaussianBlur(self.frame, (7, 7), 1)
            image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
            image_canny = cv2.Canny(image_gray, 15, 15, 3)
            kernel = np.ones((5, 5))
            image_dilate = cv2.dilate(image_canny, kernel, iterations=1)

            contours, hierarchy = cv2.findContours(image_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                area = cv2.contourArea(c)
                areas.append(area)
                perimeter = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
                list_points.append(approx)

            i = 0
            for n in areas:
                if n > area_aux:
                    area_aux = n

                    if len(list_points[i]) == 4:
                        points_aux = list_points[i]

                i = i + 1

            sum0 = points_aux[0, 0, 0] + points_aux[0, 0, 1]
            sum1 = points_aux[1, 0, 0] + points_aux[1, 0, 1]
            sum2 = points_aux[2, 0, 0] + points_aux[2, 0, 1]
            sum3 = points_aux[3, 0, 0] + points_aux[3, 0, 1]

            bigger = max([sum0, sum1, sum2, sum3])
            smaller = min([sum0, sum1, sum2, sum3])

            if bigger == sum0:
                point4 = [points_aux[0, 0, 0], points_aux[0, 0, 1]]
                sum0 = 0
            elif bigger == sum1:
                point4 = [points_aux[1, 0, 0], points_aux[1, 0, 1]]
                sum1 = 0
            elif bigger == sum2:
                point4 = [points_aux[2, 0, 0], points_aux[2, 0, 1]]
                sum2 = 0
            elif bigger == sum3:
                point4 = [points_aux[3, 0, 0], points_aux[3, 0, 1]]
                sum3 = 0

            if smaller == sum0:
                point1 = [points_aux[0, 0, 0], points_aux[0, 0, 1]]
                sum0 = 0
            elif smaller == sum1:
                point1 = [points_aux[1, 0, 0], points_aux[1, 0, 1]]
                sum1 = 0
            elif smaller == sum2:
                point1 = [points_aux[2, 0, 0], points_aux[2, 0, 1]]
                sum2 = 0
            elif smaller == sum3:
                point1 = [points_aux[3, 0, 0], points_aux[3, 0, 1]]
                sum3 = 0

            list_sum = [sum0, sum1, sum2, sum3]

            j = 0
            for n in list_sum:
                if n == 0:
                    list_sum.remove(n)
                j += 1

            if list_sum[0] == sum0:
                aux1 = [points_aux[0, 0, 0], points_aux[0, 0, 1]]
            elif list_sum[0] == sum1:
                aux1 = [points_aux[1, 0, 0], points_aux[1, 0, 1]]
            elif list_sum[0] == sum2:
                aux1 = [points_aux[2, 0, 0], points_aux[2, 0, 1]]
            elif list_sum[0] == sum3:
                aux1 = [points_aux[3, 0, 0], points_aux[3, 0, 1]]

            if list_sum[1] == sum0:
                aux2 = [points_aux[0, 0, 0], points_aux[0, 0, 1]]
            elif list_sum[1] == sum1:
                aux2 = [points_aux[1, 0, 0], points_aux[1, 0, 1]]
            elif list_sum[1] == sum2:
                aux2 = [points_aux[2, 0, 0], points_aux[2, 0, 1]]
            elif list_sum[1] == sum3:
                aux2 = [points_aux[3, 0, 0], points_aux[3, 0, 1]]

            if aux1[0] > aux2[0]:
                point2 = aux1
                point3 = aux2
            else:
                point3 = aux1
                point2 = aux2

            list_out = [point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], point4[0], point4[1]]

            points_in = np.float32([[list_out[0], list_out[1]], [list_out[2], list_out[3]],
                                    [list_out[4], list_out[5]], [list_out[6], list_out[7]]])

            points_out = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])

            matrix = cv2.getPerspectiveTransform(points_in, points_out)
            rectify = cv2.warpPerspective(self.frame, matrix, (1920, 1080))

            return rectify
        except(Exception,):
            return self.frame