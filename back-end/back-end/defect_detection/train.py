from ultralytics import YOLO
import os
from pathlib import Path

def train_defect_detector():
    # 加载预训练模型
    model = YOLO('yolov8n.pt')
    
    # 训练配置
    config = {
        'data': 'data/processed/dataset.yaml',
        'epochs': 100,
        'imgsz': 640,
        'batch': 16,
        'patience': 50,
        'device': '0',  # 使用GPU，如果没有GPU则改为'cpu'
        'workers': 8,
        'project': 'defect_model',
        'name': 'defect_detector',
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'auto',
        'verbose': True,
        'seed': 42,
        'deterministic': True
    }
    
    # 开始训练
    results = model.train(**config)
    
    # 验证模型
    model.val()
    
    # 导出模型
    model.export(format='onnx')  # 导出为ONNX格式
    
    return results

if __name__ == '__main__':
    # 确保输出目录存在
    os.makedirs('defect_model', exist_ok=True)
    
    # 开始训练
    results = train_defect_detector()
    print("Training completed!") 