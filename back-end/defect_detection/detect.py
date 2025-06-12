from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import torch

class DefectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
        
    def detect(self, image_path, conf_threshold=0.25):
        """
        检测图像中的缺陷
        Args:
            image_path: 图像路径
            conf_threshold: 置信度阈值
        Returns:
            results: 检测结果列表，每个结果包含类别、置信度和边界框
            annotated_image: 标注后的图像
        """
        # 读取图像
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")
            
        # 执行检测
        results = self.model(image, conf=conf_threshold)[0]
        
        # 处理检测结果
        detections = []
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            detections.append({
                'class': self.classes[int(class_id)],
                'confidence': float(score),
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
            
        # 绘制检测结果
        annotated_image = self._draw_detections(image, detections)
        
        return detections, annotated_image
    
    def _draw_detections(self, image, detections):
        """在图像上绘制检测结果"""
        annotated_image = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            label = f"{det['class']}: {det['confidence']:.2f}"
            
            # 绘制边界框
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 绘制标签
            cv2.putText(annotated_image, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        return annotated_image
    
    def batch_detect(self, image_dir, output_dir, conf_threshold=0.25):
        """
        批量检测目录中的图像
        Args:
            image_dir: 输入图像目录
            output_dir: 输出图像目录
            conf_threshold: 置信度阈值
        """
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for image_path in image_dir.glob('*.jpg'):
            try:
                detections, annotated_image = self.detect(image_path, conf_threshold)
                
                # 保存标注后的图像
                output_path = output_dir / f"detected_{image_path.name}"
                cv2.imwrite(str(output_path), annotated_image)
                
                # 保存检测结果
                result_path = output_dir / f"results_{image_path.stem}.txt"
                with open(result_path, 'w') as f:
                    for det in detections:
                        f.write(f"{det['class']}: {det['confidence']:.2f}\n")
                        
            except Exception as e:
                print(f"处理图像 {image_path} 时出错: {str(e)}")

if __name__ == '__main__':
    # 使用示例
    detector = DefectDetector('defect_model/defect_detector/weights/best.pt')
    
    # 单张图像检测
    detections, annotated_image = detector.detect('test_image.jpg')
    cv2.imwrite('detected_image.jpg', annotated_image)
    
    # 批量检测
    detector.batch_detect('test_images', 'detection_results') 