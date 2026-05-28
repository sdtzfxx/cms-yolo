# CMS-YOLOv7: 融合多重注意力机制的目标检测

本项目基于 [YOLOv7](https://github.com/WongKinYiu/yolov7) 进行改进，针对**小目标检测**场景，在骨干网络和颈部网络中引入多种先进的注意力机制，显著提升模型在密集小目标场景下的检测能力。

## 特性

- **多重注意力机制融合** — 集成 ACmix、BiFormer、MSDA、ODConv 等多种注意力模块
- **针对小目标检测优化** — 在 VisDrone2019、WiderPerson、TinyPerson 等数据集上验证
- **即插即用** — 注意力模块可直接替换标准卷积层，支持丰富的网络配置组合
- **基于 YOLOv7** — 继承 YOLOv7 的高效网络结构和训练 pipeline

## 模型架构改进

### 注意力模块

| 模块 | 文件 | 说明 |
|------|------|------|
| **ACmix** | `models/ACmix.py` | 自注意力与卷积的混合模块，兼顾全局上下文与局部特征 |
| **BiFormer** | `models/biformer.py` | 双层路由注意力（Bi-Level Routing Attention），实现稀疏高效的全局交互 |
| **MSDA** | `models/MSDA.py` | 多尺度膨胀注意力（Multi-Scale Dilated Attention），通过不同膨胀率捕获多尺度特征 |
| **ODConv** | `models/ODConv.py` | 全维动态卷积，沿核空间四个维度学习注意力权重 |
| **RFAConv** | `models/common.py` | 感受野注意力卷积，自适应调整有效感受野 |

### 其他改进

- **SPPCSPC** 增强版 — 引入 RFAConv 替换部分标准卷积
- **BiLevelRoutingAttention** — 用于特征融合阶段的 Concat_att 操作
- **CBAM** — 通道-空间注意力模块
- **多种 CSP 结构变体** — 支持 RepVGG、SwinTransformer、GhostNet 等结构

## 环境要求

- Python >= 3.8
- PyTorch >= 1.7.0
- torchvision >= 0.8.1

安装依赖：

```bash
pip install -r requirements.txt
```

## 数据集

项目已配置以下小目标检测数据集：

- **[VisDrone2019](https://github.com/VisDrone/VisDrone-Dataset)** — 无人机视角目标检测，10 个类别 — `data/VD2019.yaml`
- **[WiderPerson](http://www.cbsr.ia.ac.cn/users/sfzhang/WiderPerson/)** — 密集行人检测，1 个类别 — `data/WP.yaml`
- **[TinyPerson](https://github.com/ucas-vg/TinyPerson)** — 极小尺度行人检测，2 个类别 — `data/Tinyperson.yaml`

## 训练

### 从头训练

```bash
python train.py --data data/VD2019.yaml --cfg cfg/training/yolov7-cms.yaml --epochs 300 --batch-size 16 --img 640
```

### 使用辅助损失训练（推荐）

```bash
python train_aux.py --data data/VD2019.yaml --cfg cfg/training/yolov7-cms.yaml --epochs 300 --batch-size 16 --img 640
```

## 推理

```bash
python detect.py --weights runs/train/exp/weights/best.pt --source inference/images/ --img 640 --conf 0.25 --iou 0.45
```

## 测试与评估

```bash
python test.py --weights runs/train/exp/weights/best.pt --data data/VD2019.yaml --img 640
```

## 工具脚本

| 脚本 | 说明 |
|------|------|
| `keshihua.py` | 可视化 YOLO 格式标注的边界框 |
| `write_txt.py` | 生成数据集图片路径列表文件 |
| `jisuananchors.py` | 计算自定义数据集的锚框 |
| `export.py` | 导出 ONNX / TensorRT 等部署格式 |

## 项目结构

```
├── cfg/                  # 模型配置文件
│   ├── deploy/           # 部署配置
│   └── baseline/         # 基线模型配置
├── data/                 # 数据集配置
├── models/               # 模型定义
│   ├── common.py         # 基础模块（Conv, Bottleneck, SPP等）
│   ├── yolo.py           # YOLO检测头与模型组装
│   ├── ACmix.py          # 注意力-卷积混合模块
│   ├── biformer.py       # BiFormer注意力
│   ├── MSDA.py           # 多尺度膨胀注意力
│   └── ODConv.py         # 全维动态卷积
├── utils/                # 工具函数
├── train.py              # 训练入口
├── train_aux.py          # 辅助损失训练入口
├── detect.py             # 推理入口
└── test.py               # 测试评估
```

## 引用

本项目基于以下工作：

```bibtex
@article{wang2022yolov7,
  title={YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors},
  author={Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark},
  journal={arXiv preprint arXiv:2207.02696},
  year={2022}
}
```

## 许可

本项目遵循 [GPL-3.0](LICENSE.md) 协议。
