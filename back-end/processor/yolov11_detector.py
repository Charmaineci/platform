# processor/yolov11_detector.py
import cv2
import numpy as np
from ultralytics import YOLO
import torch
import os


class YOLOv11Detector:
    def __init__(self, model_path):
        """
        初始化YOLOv11检测器
        Args:
            model_path: 模型权重文件路径
        """
        self.model = YOLO(model_path)
        self.classes = ['scratches']

    def create_tiles(self, image, tile_size=640, overlap=0.2):
        """Divide an image into overlapping tiles and save them for debugging."""

        height, width = image.shape[:2]
        stride = int(tile_size * (1 - overlap))  # Calculate stride based on overlap
        tiles = []
        coordinates = []

        # Generate and save tiles
        tile_idx = 0
        for y in range(0, height, stride):
            for x in range(0, width, stride):
                # Ensure tile doesn't exceed image boundaries
                y_end = min(y + tile_size, height)
                x_end = min(x + tile_size, width)
                if (y_end - y) >= tile_size * 0.5 and (x_end - x) >= tile_size * 0.5:
                    tile = image[y:y_end, x:x_end]
                    # Pad tile to tile_size if smaller (e.g., at edges)
                    if tile.shape[0] < tile_size or tile.shape[1] < tile_size:
                        padded_tile = np.zeros((tile_size, tile_size, 3), dtype=np.uint8)
                        padded_tile[:tile.shape[0], :tile.shape[1]] = tile
                        tile = padded_tile
                    tiles.append(tile)
                    coordinates.append((x, y, x_end - x, y_end - y))  # Store (x, y, w, h)
                    tile_idx += 1
        
        return tiles, coordinates
    
    def merge_detections(self, detections, coordinates, image_shape, iou_threshold=0.2, conf_threshold=0.2):
        """Merge YOLO detections from tiles using NMS."""
        all_boxes = []
        all_scores = []
        all_classes = []

        # Process detections from each tile
        for tile_dets, (x_offset, y_offset, tile_w, tile_h) in zip(detections, coordinates):
            if tile_dets is None:
                continue
            for det in tile_dets.boxes:
                # Extract bounding box, confidence, and class
                x1, y1, x2, y2 = det.xyxy[0].cpu().numpy()
                score = det.conf[0].item()
                cls = int(det.cls[0].cpu().numpy())
                
                # Map coordinates back to original image
                x1 = x1 + x_offset
                y1 = y1 + y_offset
                x2 = x2 + x_offset
                y2 = y2 + y_offset
                
                # Clip to image boundaries
                x1 = max(0, min(x1, image_shape[1]))
                x2 = max(0, min(x2, image_shape[1]))
                y1 = max(0, min(y1, image_shape[0]))
                y2 = max(0, min(y2, image_shape[0]))
                
                if score >= conf_threshold:
                    all_boxes.append([x1, y1, x2, y2])
                    all_scores.append(score)
                    all_classes.append(cls)



        # Apply NMS to merged detections
        if all_boxes and all_scores:
            try:
                boxes = torch.tensor(all_boxes, dtype=torch.float32)
                scores = torch.tensor(all_scores, dtype=torch.float32)  # Ensure scalar values
                classes = torch.tensor(all_classes, dtype=torch.int64)
                indices = torch.ops.torchvision.nms(boxes, scores, iou_threshold)
                return boxes[indices].numpy(), scores[indices].numpy(), classes[indices].numpy()
            except Exception as e:
                print(f"Error during NMS: {e}")
                return np.array([]), np.array([]), np.array([])
        else:
            print("No valid detections to merge")
            return np.array([]), np.array([]), np.array([])
        

    def detect(self, image, conf_threshold=0.25, tile_size=640, overlap=0.3):
        """
        执行目标检测
        Args:
            image: 输入图像（OpenCV格式）
            conf_threshold: 置信度阈值
        Returns:
            detections: 检测结果列表
        """

        # Create tiles and save them
        tiles, coordinates = self.create_tiles(image, tile_size, overlap)

        # Run YOLO on each tile
        detections = []
        for tile in tiles:
            if torch.cuda.is_available():
                results = self.model.predict(tile, imgsz=tile_size, device="0", conf=conf_threshold)
            else:
                results = self.model.predict(tile, imgsz=tile_size, device="cpu", conf=conf_threshold)
            detections.append(results[0] if results else None)

        # Merge detections
        boxes, scores, classes = self.merge_detections(detections, coordinates, image.shape, iou_threshold=0.4, conf_threshold=0.3)
        
        
        # 构建检测结果
        detections = []

        for box, score, cls in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            class_name = self.model.names[cls] if cls in self.model.names else f"Class {cls}"

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

        annotated_image = image.copy()

        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            class_name = det['class']
            confidence = det['confidence']

            label = f"{class_name} {confidence:.2f}"

            # 绘制矩形框
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return annotated_image

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
        # 执行检测
        detections = self.detect(image, conf_threshold)
        
        # 可视化结果
        annotated_image = self.visualize(image, detections)

        return detections, annotated_image
