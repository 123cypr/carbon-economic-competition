#!/bin/bash
# 启动脚本 - Launch Script

echo "🌱 中国碳排放数据分析系统启动中..."
echo "Starting China Carbon Emission Data Analysis System..."

# 检查是否已生成数据
if [ ! -f "src/data/national_carbon_emissions.csv" ]; then
    echo "正在生成数据..."
    python src/main.py
fi

echo "启动Web界面..."
echo "Starting Web Interface at http://localhost:8501"

# 启动Streamlit应用
streamlit run src/app.py --server.headless true --server.port 8501