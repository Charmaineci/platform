# processor/yolov11_detector.py
import cv2
import numpy as np
from ultralytics import YOLO


class YOLOv11Detector:
    def __init__(self, model_path):
        """
        初始化YOLOv8检测器
        Args:
            model_path: 模型权重文件路径
        """
        self.model = YOLO(model_path)
        self.classes = 'scratch'

    def detect(self, image, conf_threshold=0.25):
        """
        执行目标检测
        Args:
            image: 输入图像（OpenCV格式）
            conf_threshold: 置信度阈值
        Returns:
            detections: 检测结果列表
        """
        # 使用YOLO模型进行推理
        results = self.model(image, conf=conf_threshold)[0]

        # 构建检测结果
        detections = []
        boxes = results.boxes.data.tolist()
        for box in boxes:
            x1, y1, x2, y2, score, class_id = box
            class_name = self.classes[int(class_id)]
            detections.append({
                'class': class_name,
                'confidence': float(score),
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'size': {
                    'width': int(x2 - x1),
                    'height': int(y2 - y1)
                }
            })

        return detections

    def visualize(self, image, detections):
        # """
        # 可视化检测结果
        # Args:
        #     image: 输入图像
        #     detections: 检测结果列表
        # Returns:
        #     annotated_image: 标注后的图像
        # """
        # # 使用YOLO的绘图函数

        """
        使用YOLOv8的内置绘图函数来可视化图像。
        注意：此方法依赖于模型的结果，因此忽略外部detections。
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(image_rgb)
        annotated_rgb = results[0].plot()
        annotated_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)
        return annotated_bgr

        # for det in detections:
        #     x1, y1, x2, y2 = det['bbox']
        #     class_name = det['class']
        #     confidence = det['confidence']

        #     label = f"{class_name} {confidence:.2f}"

        #     # 绘制矩形框
        #     cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #     # 绘制标签背景
        #     (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        #     cv2.rectangle(annotated_image, (x1, y1 - text_h - 4), (x1 + text_w, y1), (0, 255, 0), -1)

        #     # 绘制标签文字
        #     cv2.putText(annotated_image, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # return annotated_image

    def process_image(self, image, conf_threshold=0.25):
        """
        处理图像：执行检测并可视化
        Args:
            image: 输入图像（OpenCV格式）
            conf_threshold: 置信度阈值
        Returns:
            detections: 检测结果列表
            annotated_image: 标注后的图像
        """
        # # 执行检测
        # detections = self.detect(image, conf_threshold)

        # # 可视化结果
        # annotated_image = self.visualize(image, detections)

        # return detections, annotated_image
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # YOLO 推理（只用一次）
        results = self.model(image_rgb, conf=conf_threshold)
        detections = []
        boxes = results[0].boxes
        for box, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            x1, y1, x2, y2 = map(int, box.tolist())
            score = float(conf)
            class_id = int(cls)
            class_name = self.classes[class_id]
            detections.append({
                'class': class_name,
                'confidence': score,
                'bbox': [x1, y1, x2, y2],
                'size': {
                    'width': x2 - x1,
                    'height': y2 - y1
                }
            })

        annotated_rgb = results[0].plot()
        annotated_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)

        return detections, annotated_bgr
