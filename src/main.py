"""
主程序入口
Main Entry Point for Carbon Economic Competition Analysis
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from scrapers.carbon_scraper import CarbonEmissionScraper
from scrapers.ccer_analyzer import CCERAnalyzer
from visualization.charts import CarbonVisualization

def main():
    """主程序入口"""
    print("🌱 中国碳排放数据分析系统")
    print("=" * 50)
    
    # 创建数据目录
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    
    print("1. 开始数据生成...")
    
    # 生成碳排放数据
    print("   - 生成碳排放数据...")
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
    
    print("   - 生成CCER项目数据...")
    # 生成CCER数据
    analyzer = CCERAnalyzer()
    ccer_projects = analyzer.generate_ccer_projects_data()
    companies_data = analyzer.generate_photovoltaic_companies_data()
    
    # 分析CCER影响
    impact_results = analyzer.analyze_ccer_impact(companies_data)
    
    # 保存CCER数据
    analyzer.save_data(ccer_projects, "ccer_projects.csv")
    analyzer.save_data(companies_data, "photovoltaic_companies.csv")
    
    # 保存分析结果
    import json
    with open(data_dir / "ccer_impact_analysis.json", "w", encoding='utf-8') as f:
        json.dump(impact_results, f, ensure_ascii=False, indent=2)
    
    print("2. 数据生成完成！")
    print("\n主要研究发现：")
    print(f"   - 规模扩张效应: {impact_results['scale_expansion_effect']}")
    print(f"   - 绿色创新效应: {impact_results['green_innovation_effect']}")
    print(f"   - 研发强度效应: {impact_results['rd_intensity_effect']}")
    print(f"   - 国企研发效应: {impact_results['soe_rd_effect']}")
    print(f"   - 非国企研发效应: {impact_results['non_soe_rd_effect']}")
    
    print("\n3. 生成可视化图表...")
    
    # 生成可视化图表
    viz = CarbonVisualization()
    
    # 全国碳排放趋势
    fig1 = viz.plot_national_emission_trend(national_data)
    viz.save_figure(fig1, "national_emission_trend")
    
    # 省级对比（2023年）
    fig2 = viz.plot_provincial_comparison(provincial_data, 2023)
    viz.save_figure(fig2, "provincial_comparison_2023")
    
    # 行业排放结构
    fig3 = viz.plot_industry_emission_structure(industry_data, 2023)
    viz.save_figure(fig3, "industry_emission_structure")
    
    # 碳市场分析
    fig4 = viz.plot_carbon_market_analysis(market_data)
    viz.save_figure(fig4, "carbon_market_analysis")
    
    # CCER影响分析
    fig5 = viz.plot_ccer_impact_analysis(companies_data, impact_results)
    viz.save_figure(fig5, "ccer_impact_analysis")
    
    # 光伏行业概览
    fig6 = viz.plot_photovoltaic_industry_overview(companies_data)
    viz.save_figure(fig6, "photovoltaic_industry_overview")
    
    print("4. 可视化图表生成完成！")
    
    print("\n" + "=" * 50)
    print("🎉 系统初始化完成！")
    print("\n启动Web界面:")
    print("   streamlit run src/app.py")
    print("\n数据文件位置:")
    print(f"   {data_dir}")
    print("\n可视化图表位置:")
    print(f"   {data_dir}/*.html")

if __name__ == "__main__":
    main()