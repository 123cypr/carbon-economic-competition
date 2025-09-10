# 中国碳排放量数据分析系统
# China Carbon Emission Data Analysis System

这是一个专为能源经济比赛设计的中国碳排放数据爬取和可视化系统，重点研究中国核证自愿减排机制(CCER)对光伏发电企业的双重影响。

## 项目概述

本项目研究CCER机制对光伏发电企业的影响，包括：
- 对企业规模扩张的促进作用
- 对绿色创新的抑制效应
- 不同企业类型的异质性表现
- 管理者能力的调节效应

## 功能特性

- 🔍 **数据爬取**: 自动爬取中国碳排放相关数据
- 📊 **高级可视化**: 提供多种图表类型和交互式展示
- 🏭 **企业分析**: 专注于光伏发电企业的CCER参与分析
- 📈 **趋势分析**: 碳排放趋势和减排效果评估
- 🔬 **学术研究**: 支持双重差分模型等高级分析方法

## 项目结构

```
carbon-economic-competition/
├── src/
│   ├── scrapers/          # 数据爬取模块
│   ├── analysis/          # 数据分析模块
│   ├── visualization/     # 可视化模块
│   └── data/             # 数据存储
├── tests/                # 测试文件
├── docs/                 # 文档
├── requirements.txt      # 依赖包
└── README.md            # 项目说明
```

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行主程序
```bash
python src/main.py
```

3. 启动Web界面
```bash
streamlit run src/app.py
```

## 研究重点

### CCER机制分析
- 861个CCER备案项目信息分析
- 24家A股上市光伏企业面板数据
- 双重差分模型构建

### 主要发现
- CCER参与显著促进光伏发电企业规模扩张
- 同时抑制企业绿色创新能力
- 对非国企研发投入产生显著抑制作用
- 企业管理者能力产生负向调节效应

## 技术栈

- **数据爬取**: Requests, BeautifulSoup, Scrapy, Selenium
- **数据处理**: Pandas, NumPy
- **可视化**: Matplotlib, Seaborn, Plotly, Streamlit
- **金融数据**: Akshare, yfinance
- **分析工具**: 双重差分模型, 稳健性检验

## 许可证

MIT License