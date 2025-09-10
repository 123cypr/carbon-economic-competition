# 项目文档
# Project Documentation

## 系统架构 (System Architecture)

### 核心组件 (Core Components)

1. **数据爬取模块 (Data Scraping Module)**
   - `carbon_scraper.py`: 碳排放数据爬取
   - `ccer_analyzer.py`: CCER项目分析

2. **可视化模块 (Visualization Module)**
   - `charts.py`: 高级图表生成
   - 支持Plotly交互式图表

3. **Web界面 (Web Interface)**
   - `app.py`: Streamlit应用主程序
   - 多页面导航系统

### 数据结构 (Data Structure)

#### 全国碳排放数据
```csv
year,total_emission,per_capita_emission,emission_intensity,data_source
2000,10000.0,7.14,10000.0,国家统计局/环保部
```

#### CCER项目数据
```csv
project_id,project_name,project_type,province,capacity_mw,annual_emission_reduction,start_year,project_owner
CCER-2012-0001,太阳能发电项目1,太阳能发电,内蒙古,150.5,300000.0,2012,隆基绿能
```

#### 光伏企业数据
```csv
company_name,year,revenue,total_assets,rd_investment,rd_intensity,green_patents,ccer_participation
隆基绿能,2010,140.85,227.41,9.69,0.0688,2,0
```

## 核心算法 (Core Algorithms)

### 双重差分模型 (Difference-in-Differences)

```python
Y_it = α + β₁×CCER_it + β₂×Post_t + β₃×(CCER_it × Post_t) + γX_it + μ_i + λ_t + ε_it
```

其中：
- `Y_it`: 被解释变量（绿色创新、企业规模等）
- `CCER_it`: CCER参与虚拟变量
- `Post_t`: 2013年后时间虚拟变量
- `β₃`: 双重差分估计量（关键系数）

### 实现细节

```python
def _calculate_did_effect(self, data: pd.DataFrame, outcome_var: str) -> float:
    """计算双重差分效应"""
    before = data[data['year'] < 2013]  # 处理前期
    after = data[data['year'] >= 2013]   # 处理后期
    
    # 处理组效应
    treatment_effect = after[after['ccer_participation'] == 1][outcome_var].mean() - \
                      before[before['ccer_participation'] == 1][outcome_var].mean()
    
    # 控制组效应
    control_effect = after[after['ccer_participation'] == 0][outcome_var].mean() - \
                    before[before['ccer_participation'] == 0][outcome_var].mean()
    
    # DID估计量
    return treatment_effect - control_effect
```

## 主要发现 (Key Findings)

### 1. 规模扩张效应
- **结果**: CCER参与对企业规模有负向影响
- **解释**: 可能由于初期投入成本较高

### 2. 绿色创新抑制
- **结果**: CCER参与降低绿色专利产出
- **机制**: 资源挤出效应，投资向规模扩张倾斜

### 3. 研发投入影响
- **国有企业**: 影响相对较小
- **非国有企业**: 研发投入显著受到抑制

## 可视化特性 (Visualization Features)

### 1. 趋势分析图
- 全国碳排放趋势
- 多指标联动展示
- 时间序列分析

### 2. 地理分布图
- 省级排放对比
- 交互式地图展示
- 热力图效果

### 3. 行业结构图
- 饼图显示占比
- 趋势线显示变化
- 多维度对比

### 4. 企业分析图
- 双重差分可视化
- 异质性分析结果
- 面板数据展示

## 技术栈 (Technology Stack)

### 后端 (Backend)
- **Python 3.12+**
- **Pandas**: 数据处理
- **NumPy**: 数值计算
- **Requests**: 数据爬取

### 前端 (Frontend)
- **Streamlit**: Web框架
- **Plotly**: 交互式图表
- **Altair**: 统计可视化

### 数据存储 (Data Storage)
- **CSV**: 结构化数据存储
- **JSON**: 分析结果存储

## 部署说明 (Deployment Guide)

### 本地运行 (Local Deployment)

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **生成数据**
```bash
python src/main.py
```

3. **启动Web界面**
```bash
streamlit run src/app.py
```

或使用启动脚本：
```bash
./launch.sh
```

### 生产环境 (Production)

1. **使用Docker**
```dockerfile
FROM python:3.12-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **云服务部署**
- 支持Heroku、AWS、阿里云等平台
- 配置环境变量和依赖

## API接口 (API Reference)

### 数据爬取接口

```python
from src.scrapers.carbon_scraper import CarbonEmissionScraper

scraper = CarbonEmissionScraper()
national_data = scraper.get_national_carbon_data()
```

### 分析接口

```python
from src.scrapers.ccer_analyzer import CCERAnalyzer

analyzer = CCERAnalyzer()
results = analyzer.analyze_ccer_impact(companies_data)
```

### 可视化接口

```python
from src.visualization.charts import CarbonVisualization

viz = CarbonVisualization()
fig = viz.plot_national_emission_trend(data)
```

## 扩展开发 (Extension Development)

### 添加新数据源

1. 在`scrapers/`目录创建新模块
2. 继承基础爬取类
3. 实现数据获取方法
4. 在主程序中调用

### 添加新图表类型

1. 在`visualization/charts.py`中添加方法
2. 遵循Plotly图表规范
3. 在Web界面中添加调用

### 添加新分析方法

1. 在`analysis/`目录创建分析模块
2. 实现统计分析方法
3. 集成到主要流程中

## 故障排除 (Troubleshooting)

### 常见问题

1. **依赖安装失败**
   - 使用虚拟环境
   - 更新pip版本
   - 检查Python版本兼容性

2. **数据加载错误**
   - 检查文件路径
   - 验证数据格式
   - 确认权限设置

3. **图表显示异常**
   - 检查浏览器兼容性
   - 清除缓存
   - 验证数据完整性

### 性能优化

1. **数据缓存**
   - 使用@st.cache_data装饰器
   - 避免重复计算
   - 分页加载大数据集

2. **图表优化**
   - 限制数据点数量
   - 使用采样技术
   - 延迟加载复杂图表

## 许可证 (License)

MIT License - 详见LICENSE文件

## 贡献指南 (Contributing)

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 联系方式 (Contact)

- 项目主页: https://github.com/123cypr/carbon-economic-competition
- 问题反馈: 通过GitHub Issues