import os
import shutil
import yaml
from pathlib import Path
import cv2
import numpy as np

class NEUDataProcessor:
    def __init__(self, data_dir, output_dir):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
        
    def create_yolo_structure(self):
        """创建YOLO格式的目录结构"""
        # 创建训练、验证和测试目录
        for split in ['train', 'val', 'test']:
            (self.output_dir / split / 'images').mkdir(parents=True, exist_ok=True)
            (self.output_dir / split / 'labels').mkdir(parents=True, exist_ok=True)
            
    def process_dataset(self, train_ratio=0.7, val_ratio=0.2):
        """处理数据集并转换为YOLO格式"""
        self.create_yolo_structure()
        
        # 获取所有图像文件
        all_images = []
        for class_name in self.classes:
            class_dir = self.data_dir / class_name
            if class_dir.exists():
                images = list(class_dir.glob('*.jpg'))
                all_images.extend([(img, class_name) for img in images])
        
        # 随机打乱数据
        np.random.shuffle(all_images)
        
        # 划分数据集
        n_samples = len(all_images)
        n_train = int(n_samples * train_ratio)
        n_val = int(n_samples * val_ratio)
        
        train_data = all_images[:n_train]
        val_data = all_images[n_train:n_train + n_val]
        test_data = all_images[n_train + n_val:]
        
        # 处理每个数据集
        self._process_split(train_data, 'train')
        self._process_split(val_data, 'val')
        self._process_split(test_data, 'test')
        
        # 创建数据集配置文件
        self._create_dataset_yaml()
        
    def _process_split(self, data_split, split_name):
        """处理特定数据集划分"""
        for img_path, class_name in data_split:
            # 复制图像
            img_name = img_path.name
            shutil.copy2(img_path, self.output_dir / split_name / 'images' / img_name)
            
            # 创建标签文件
            label_path = self.output_dir / split_name / 'labels' / f"{img_path.stem}.txt"
            class_id = self.classes.index(class_name)
            
            # 读取图像获取尺寸
            img = cv2.imread(str(img_path))
            height, width = img.shape[:2]
            
            # 创建YOLO格式的标签（这里假设缺陷占据整个图像）
            with open(label_path, 'w') as f:
                # 格式：class_id x_center y_center width height
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")
                
    def _create_dataset_yaml(self):
        """创建数据集配置文件"""
        data_yaml = {
            'path': str(self.output_dir),
            'train': 'train/images',
            'val': 'val/images',
            'test': 'test/images',
            'names': {i: name for i, name in enumerate(self.classes)}
        }
        
        with open(self.output_dir / 'dataset.yaml', 'w') as f:
            yaml.dump(data_yaml, f, default_flow_style=False)
            
if __name__ == '__main__':
    # 使用示例
    processor = NEUDataProcessor(
        data_dir='data/NEU-DET',
        output_dir='data/processed'
    )
    processor.process_dataset() 