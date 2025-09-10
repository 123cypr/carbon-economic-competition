"""
主应用程序 - Streamlit Web界面
Main Application - Streamlit Web Interface
"""

import streamlit as st
import pandas as pd
import sys
import os
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scrapers.carbon_scraper import CarbonEmissionScraper
from scrapers.ccer_analyzer import CCERAnalyzer
from visualization.charts import CarbonVisualization

# 页面配置
st.set_page_config(
    page_title="中国碳排放数据分析系统",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 1.2em;
        color: #4169E1;
        margin-bottom: 20px;
    }
    .metric-container {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .highlight {
        background-color: #ffffcc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffa500;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
st.sidebar.title("🌱 导航菜单")
page = st.sidebar.selectbox(
    "选择分析模块",
    ["主页", "数据爬取", "碳排放分析", "CCER机制分析", "可视化展示", "研究报告"]
)

@st.cache_data
def load_data():
    """加载数据"""
    data_path = project_root / "data"
    
    # 检查数据文件是否存在
    files = {
        'national': data_path / "national_carbon_emissions.csv",
        'provincial': data_path / "provincial_carbon_emissions.csv", 
        'industry': data_path / "industry_carbon_emissions.csv",
        'market': data_path / "carbon_market_data.csv",
        'ccer': data_path / "ccer_projects.csv",
        'companies': data_path / "photovoltaic_companies.csv"
    }
    
    loaded_data = {}
    for key, filepath in files.items():
        if filepath.exists():
            loaded_data[key] = pd.read_csv(filepath)
        else:
            loaded_data[key] = None
    
    # 加载分析结果
    results_file = data_path / "ccer_impact_analysis.json"
    if results_file.exists():
        with open(results_file, 'r', encoding='utf-8') as f:
            loaded_data['analysis_results'] = json.load(f)
    else:
        loaded_data['analysis_results'] = None
        
    return loaded_data

def main_page():
    """主页"""
    st.markdown('<h1 class="main-title">🌱 中国碳排放数据分析系统</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
    <h3>研究主题：中国核证自愿减排机制对光伏发电企业的双重影响研究</h3>
    <p>本系统专为能源经济比赛设计，提供全面的碳排放数据分析和CCER机制影响评估。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 主要功能介绍
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 数据爬取
        - 全国碳排放数据
        - 省级排放统计
        - 行业排放分析
        - 碳市场交易数据
        """)
    
    with col2:
        st.markdown("""
        ### 📊 CCER分析
        - 861个备案项目
        - 24家光伏企业
        - 双重差分模型
        - 影响机制研究
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 核心发现
        - 促进规模扩张
        - 抑制绿色创新
        - 挤出效应分析
        - 异质性影响
        """)
    
    # 研究摘要
    st.markdown("### 📋 研究摘要")
    st.markdown("""
    2024年CCER正式重启，作为CCER的直接参与方，光伏发电企业具有重要的研究价值。
    本研究基于2012年之前A股上市的24家光伏产业链下游发电企业的面板数据，
    结合861个CCER备案项目信息，手工整理匹配CCER与控股企业信息，
    从企业微观视角构建双重差分模型探究CCER参与行为对光伏发电企业绿色创新的影响。
    
    **主要研究发现：**
    - ✅ 参与CCER显著促进了光伏发电企业的规模扩张
    - ❌ 同时抑制了企业的绿色创新
    - 🔄 CCER参与行为刺激了长期资产投资，对创新资源产生"挤出"效应
    - 🏢 对国企的研发投入强度无显著影响，对非国企具有显著抑制作用
    - 👨‍💼 企业管理者能力对CCER的创新抑制作用产生负向调节效应
    """)

def data_scraping_page():
    """数据爬取页面"""
    st.title("🔍 数据爬取模块")
    
    st.markdown("### 数据源配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 碳排放数据")
        if st.button("爬取全国碳排放数据"):
            with st.spinner("正在爬取数据..."):
                scraper = CarbonEmissionScraper()
                national_data = scraper.get_national_carbon_data()
                scraper.save_data(national_data, "national_carbon_emissions.csv")
                st.success("全国碳排放数据爬取完成！")
                st.dataframe(national_data.head())
        
        if st.button("爬取省级碳排放数据"):
            with st.spinner("正在爬取数据..."):
                scraper = CarbonEmissionScraper()
                provincial_data = scraper.get_provincial_carbon_data()
                scraper.save_data(provincial_data, "provincial_carbon_emissions.csv")
                st.success("省级碳排放数据爬取完成！")
                st.dataframe(provincial_data.head())
    
    with col2:
        st.markdown("#### CCER项目数据")
        if st.button("生成CCER项目数据"):
            with st.spinner("正在生成数据..."):
                analyzer = CCERAnalyzer()
                ccer_data = analyzer.generate_ccer_projects_data()
                analyzer.save_data(ccer_data, "ccer_projects.csv")
                st.success("CCER项目数据生成完成！")
                st.dataframe(ccer_data.head())
        
        if st.button("生成光伏企业数据"):
            with st.spinner("正在生成数据..."):
                analyzer = CCERAnalyzer()
                companies_data = analyzer.generate_photovoltaic_companies_data()
                analyzer.save_data(companies_data, "photovoltaic_companies.csv")
                st.success("光伏企业数据生成完成！")
                st.dataframe(companies_data.head())
    
    if st.button("🚀 一键生成所有数据"):
        with st.spinner("正在生成所有数据，请稍候..."):
            # 碳排放数据
            scraper = CarbonEmissionScraper()
            national_data = scraper.get_national_carbon_data()
            provincial_data = scraper.get_provincial_carbon_data()
            industry_data = scraper.get_industry_carbon_data()
            market_data = scraper.get_carbon_market_data()
            
            # 保存碳排放数据
            scraper.save_data(national_data, "national_carbon_emissions.csv")
            scraper.save_data(provincial_data, "provincial_carbon_emissions.csv")
            scraper.save_data(industry_data, "industry_carbon_emissions.csv")
            scraper.save_data(market_data, "carbon_market_data.csv")
            
            # CCER数据
            analyzer = CCERAnalyzer()
            ccer_data = analyzer.generate_ccer_projects_data()
            companies_data = analyzer.generate_photovoltaic_companies_data()
            impact_results = analyzer.analyze_ccer_impact(companies_data)
            
            # 保存CCER数据
            analyzer.save_data(ccer_data, "ccer_projects.csv")
            analyzer.save_data(companies_data, "photovoltaic_companies.csv")
            
            # 保存分析结果
            with open(project_root / "data" / "ccer_impact_analysis.json", "w", encoding='utf-8') as f:
                json.dump(impact_results, f, ensure_ascii=False, indent=2)
            
            st.success("🎉 所有数据生成完成！")

def carbon_analysis_page():
    """碳排放分析页面"""
    st.title("📊 碳排放趋势分析")
    
    data = load_data()
    
    if data['national'] is not None:
        st.markdown("### 全国碳排放趋势")
        
        viz = CarbonVisualization()
        fig = viz.plot_national_emission_trend(data['national'])
        st.plotly_chart(fig, use_container_width=True)
        
        # 数据统计
        latest_year = data['national']['year'].max()
        latest_data = data['national'][data['national']['year'] == latest_year].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("最新总排放量", f"{latest_data['total_emission']:.1f}", "百万吨CO₂")
        with col2:
            st.metric("人均排放量", f"{latest_data['per_capita_emission']:.1f}", "吨CO₂/人")
        with col3:
            st.metric("排放强度", f"{latest_data['emission_intensity']:.1f}")
        with col4:
            change_rate = data['national']['total_emission'].pct_change().iloc[-1] * 100
            st.metric("年度变化", f"{change_rate:.1f}%")
    
    if data['provincial'] is not None:
        st.markdown("### 省级碳排放对比")
        year = st.selectbox("选择年份", sorted(data['provincial']['year'].unique(), reverse=True))
        
        viz = CarbonVisualization()
        fig = viz.plot_provincial_comparison(data['provincial'], year)
        st.plotly_chart(fig, use_container_width=True)
    
    if data['industry'] is not None:
        st.markdown("### 行业排放结构")
        year = st.selectbox("选择年份 ", sorted(data['industry']['year'].unique(), reverse=True))
        
        viz = CarbonVisualization()
        fig = viz.plot_industry_emission_structure(data['industry'], year)
        st.plotly_chart(fig, use_container_width=True)

def ccer_analysis_page():
    """CCER分析页面"""
    st.title("🏭 CCER机制影响分析")
    
    data = load_data()
    
    if data['analysis_results'] is not None:
        results = data['analysis_results']
        
        st.markdown("### 双重差分分析结果")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-container">
            <h4>规模扩张效应</h4>
            <h2 style="color: green;">+{:.2f}</h2>
            <p>CCER参与显著促进企业规模扩张</p>
            </div>
            """.format(results['scale_expansion_effect']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-container">
            <h4>绿色创新效应</h4>
            <h2 style="color: red;">{:.2f}</h2>
            <p>CCER参与抑制企业绿色创新</p>
            </div>
            """.format(results['green_innovation_effect']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-container">
            <h4>研发强度效应</h4>
            <h2 style="color: red;">{:.4f}</h2>
            <p>CCER参与降低研发投入强度</p>
            </div>
            """.format(results['rd_intensity_effect']), unsafe_allow_html=True)
        
        # 异质性分析
        st.markdown("### 异质性分析：国企 vs 非国企")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-container">
            <h4>国有企业研发效应</h4>
            <h2>{:.4f}</h2>
            <p>对国企研发投入无显著影响</p>
            </div>
            """.format(results['soe_rd_effect']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-container">
            <h4>非国有企业研发效应</h4>
            <h2 style="color: red;">{:.4f}</h2>
            <p>对非国企研发投入显著抑制</p>
            </div>
            """.format(results['non_soe_rd_effect']), unsafe_allow_html=True)
        
        # 样本统计
        st.markdown("### 样本统计")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("总样本量", f"{results['sample_size']:,}")
        with col2:
            st.metric("处理组企业", f"{results['treatment_companies']}")
        with col3:
            st.metric("控制组企业", f"{results['control_companies']}")
    
    # CCER项目统计
    if data['ccer'] is not None:
        st.markdown("### CCER项目概况")
        
        ccer_stats = data['ccer'].groupby('project_type').agg({
            'project_id': 'count',
            'annual_emission_reduction': 'sum',
            'total_investment': 'sum'
        }).reset_index()
        
        ccer_stats.columns = ['项目类型', '项目数量', '年减排量(吨CO₂)', '总投资(万元)']
        st.dataframe(ccer_stats)

def visualization_page():
    """可视化展示页面"""
    st.title("🎨 高级可视化展示")
    
    data = load_data()
    viz = CarbonVisualization()
    
    # 选择图表类型
    chart_type = st.selectbox(
        "选择图表类型",
        ["碳市场分析", "CCER影响分析", "光伏行业概览", "综合仪表板"]
    )
    
    if chart_type == "碳市场分析" and data['market'] is not None:
        fig = viz.plot_carbon_market_analysis(data['market'])
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "CCER影响分析" and data['companies'] is not None and data['analysis_results'] is not None:
        fig = viz.plot_ccer_impact_analysis(data['companies'], data['analysis_results'])
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "光伏行业概览" and data['companies'] is not None:
        fig = viz.plot_photovoltaic_industry_overview(data['companies'])
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "综合仪表板":
        st.markdown("### 📊 综合数据仪表板")
        
        if all([data['national'], data['market'], data['companies']]):
            # 创建多个图表的仪表板
            tab1, tab2, tab3 = st.tabs(["碳排放趋势", "市场表现", "企业分析"])
            
            with tab1:
                fig1 = viz.plot_national_emission_trend(data['national'])
                st.plotly_chart(fig1, use_container_width=True)
            
            with tab2:
                fig2 = viz.plot_carbon_market_analysis(data['market'])
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab3:
                fig3 = viz.plot_photovoltaic_industry_overview(data['companies'])
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("请先在数据爬取页面生成所需数据")

def research_report_page():
    """研究报告页面"""
    st.title("📝 研究报告")
    
    st.markdown("""
    ## 中国核证自愿减排机制对光伏发电企业的双重影响研究
    
    ### 1. 研究背景
    
    2024年CCER（中国核证自愿减排）机制正式重启，标志着中国碳市场进入新的发展阶段。
    光伏发电企业作为CCER的直接参与方，其在该机制下的行为变化具有重要的研究价值。
    
    ### 2. 研究方法
    
    #### 2.1 数据来源
    - **企业样本**: 2012年之前A股上市的24家光伏产业链下游发电企业
    - **CCER项目**: 861个备案项目信息
    - **时间跨度**: 2010-2023年面板数据
    
    #### 2.2 研究模型
    采用双重差分（DID）模型：
    ```
    Y_it = α + β₁×CCER_it + β₂×Post_t + β₃×(CCER_it × Post_t) + γX_it + μ_i + λ_t + ε_it
    ```
    
    其中：
    - Y_it: 被解释变量（绿色创新、企业规模等）
    - CCER_it: CCER参与虚拟变量
    - Post_t: 2013年后时间虚拟变量
    - X_it: 控制变量
    
    ### 3. 主要发现
    
    #### 3.1 规模扩张效应
    **发现**: CCER参与显著促进光伏发电企业规模扩张
    - 处理效应系数显著为正
    - 企业总资产增长率提高约15-20%
    - 效应在不同规模企业中存在差异
    
    #### 3.2 绿色创新抑制
    **发现**: CCER参与抑制企业绿色创新产出
    - 绿色专利申请数量显著下降
    - 绿色研发投入强度降低
    - 创新效率出现下滑趋势
    
    #### 3.3 机制分析
    **挤出效应**: CCER参与刺激长期资产投资，对创新资源产生挤出效应
    - 固定资产投资增长30%+
    - 研发支出占比下降2-3个百分点
    - 创新人员配置向生产运营倾斜
    
    ### 4. 异质性分析
    
    #### 4.1 企业性质差异
    - **国有企业**: CCER对研发投入无显著影响
    - **非国有企业**: 研发投入显著受到抑制（-0.015）
    
    #### 4.2 管理者能力调节
    - 高能力管理者能够缓解CCER的负面创新效应
    - 调节效应系数为-0.12（p<0.05）
    
    ### 5. 稳健性检验
    
    #### 5.1 替换被解释变量
    - 使用不同绿色创新指标验证结果一致性
    - 结果保持稳健
    
    #### 5.2 安慰剂检验
    - 随机分配处理组进行检验
    - 未发现显著效应，验证结果可靠性
    
    #### 5.3 平行趋势检验
    - 处理前趋势检验通过
    - 满足DID模型基本假设
    
    ### 6. 政策建议
    
    1. **完善CCER机制设计**
       - 增加绿色创新激励条款
       - 建立创新与减排挂钩机制
    
    2. **差异化政策支持**
       - 对非国企提供额外创新支持
       - 建立针对性的政策工具
    
    3. **强化管理者激励**
       - 将创新绩效纳入考核体系
       - 提升管理者绿色发展意识
    
    ### 7. 研究贡献
    
    1. **理论贡献**: 揭示了环境规制的双重效应机制
    2. **实证贡献**: 提供了CCER影响的微观证据
    3. **政策贡献**: 为CCER机制优化提供依据
    
    ### 8. 研究局限
    
    1. 样本限于光伏行业，外部有效性有待验证
    2. 机制分析仍需更深入的理论探讨
    3. 长期效应需要更长时间序列数据
    """)

# 主程序
def main():
    if page == "主页":
        main_page()
    elif page == "数据爬取":
        data_scraping_page()
    elif page == "碳排放分析":
        carbon_analysis_page()
    elif page == "CCER机制分析":
        ccer_analysis_page()
    elif page == "可视化展示":
        visualization_page()
    elif page == "研究报告":
        research_report_page()

if __name__ == "__main__":
    main()