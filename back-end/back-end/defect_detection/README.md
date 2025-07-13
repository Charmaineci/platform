# 金属表面缺陷检测模块

基于YOLOv8的金属表面缺陷检测系统，使用NEU-DET数据集训练。

## 目录结构
```
defect_detection/
├── models/              # 模型相关文件
│   ├── yolov8n.pt      # YOLOv8预训练模型
│   └── defect_model/   # 训练好的缺陷检测模型
├── data/               # 数据集
│   ├── NEU-DET/       # NEU-DET数据集
│   └── processed/     # 处理后的数据集
├── utils/             # 工具函数
├── train.py           # 训练脚本
└── detect.py          # 检测脚本
```

## 数据集说明
NEU-DET数据集包含6种金属表面缺陷：
- 裂纹 (Crazing)
- 夹杂 (Inclusion)
- 斑块 (Patches)
- 点蚀 (Pitted Surface)
- 轧制氧化皮 (Rolled-in Scale)
- 划痕 (Scratches)

## 使用方法
1. 准备数据集
2. 训练模型
3. 进行检测 