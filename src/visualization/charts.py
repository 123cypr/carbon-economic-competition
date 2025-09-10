"""
高级可视化模块
Advanced Visualization Module for Carbon Emission Analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置颜色主题
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'carbon': '#654321',
    'renewable': '#4CAF50'
}

class CarbonVisualization:
    """碳排放数据可视化类"""
    
    def __init__(self):
        self.fig_size = (12, 8)
        sns.set_style("whitegrid")
        
    def plot_national_emission_trend(self, data: pd.DataFrame) -> go.Figure:
        """绘制全国碳排放趋势图"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('总排放量趋势', '人均排放量趋势', '排放强度变化', '年度变化率'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 总排放量趋势
        fig.add_trace(
            go.Scatter(
                x=data['year'],
                y=data['total_emission'],
                mode='lines+markers',
                name='总排放量(百万吨CO₂)',
                line=dict(color=COLORS['carbon'], width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # 人均排放量趋势
        fig.add_trace(
            go.Scatter(
                x=data['year'],
                y=data['per_capita_emission'],
                mode='lines+markers',
                name='人均排放量(吨CO₂/人)',
                line=dict(color=COLORS['warning'], width=3),
                marker=dict(size=8)
            ),
            row=1, col=2
        )
        
        # 排放强度变化
        fig.add_trace(
            go.Scatter(
                x=data['year'],
                y=data['emission_intensity'],
                mode='lines+markers',
                name='排放强度',
                line=dict(color=COLORS['info'], width=3),
                marker=dict(size=8),
                fill='tonexty'
            ),
            row=2, col=1
        )
        
        # 年度变化率
        year_change = data['total_emission'].pct_change() * 100
        colors = ['red' if x > 0 else 'green' for x in year_change]
        
        fig.add_trace(
            go.Bar(
                x=data['year'][1:],
                y=year_change[1:],
                name='年度变化率(%)',
                marker_color=colors
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            title_text="中国碳排放趋势分析",
            title_x=0.5,
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def plot_provincial_comparison(self, data: pd.DataFrame, year: int = 2023) -> go.Figure:
        """绘制省份碳排放对比图"""
        year_data = data[data['year'] == year].copy()
        year_data = year_data.sort_values('total_emission', ascending=True)
        
        fig = go.Figure()
        
        # 水平柱状图
        fig.add_trace(go.Bar(
            y=year_data['province'],
            x=year_data['total_emission'],
            orientation='h',
            marker=dict(
                color=year_data['total_emission'],
                colorscale='RdYlBu_r',
                showscale=True,
                colorbar=dict(title="排放量(百万吨CO₂)")
            ),
            text=year_data['total_emission'].round(1),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>' +
                         '排放量: %{x:.1f} 百万吨CO₂<br>' +
                         'GDP排放比: %{customdata:.4f}<extra></extra>',
            customdata=year_data['gdp_emission_ratio']
        ))
        
        fig.update_layout(
            title=f'{year}年各省份碳排放量对比',
            xaxis_title='碳排放量 (百万吨CO₂)',
            yaxis_title='省份',
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def plot_industry_emission_structure(self, data: pd.DataFrame, year: int = 2023) -> go.Figure:
        """绘制行业排放结构图"""
        year_data = data[data['year'] == year]
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "domain"}, {"type": "xy"}]],
            subplot_titles=('行业排放占比', '行业排放趋势')
        )
        
        # 饼图 - 行业排放占比
        fig.add_trace(go.Pie(
            labels=year_data['industry'],
            values=year_data['total_emission'],
            hole=0.3,
            textinfo='label+percent',
            textposition='auto',
            marker=dict(colors=px.colors.qualitative.Set3)
        ), row=1, col=1)
        
        # 趋势图 - 主要行业
        major_industries = year_data.nlargest(5, 'total_emission')['industry'].tolist()
        trend_data = data[data['industry'].isin(major_industries)]
        
        for industry in major_industries:
            industry_data = trend_data[trend_data['industry'] == industry]
            fig.add_trace(go.Scatter(
                x=industry_data['year'],
                y=industry_data['total_emission'],
                mode='lines+markers',
                name=industry,
                line=dict(width=2),
                marker=dict(size=6)
            ), row=1, col=2)
        
        fig.update_layout(
            height=600,
            title_text=f'{year}年行业碳排放结构分析',
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def plot_carbon_market_analysis(self, data: pd.DataFrame) -> go.Figure:
        """绘制碳市场分析图"""
        # 按年月聚合数据
        data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('碳价格走势', '交易量变化', '交易金额趋势'),
            vertical_spacing=0.08
        )
        
        # 碳价格走势
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['carbon_price'],
            mode='lines',
            name='碳价格(元/吨)',
            line=dict(color=COLORS['primary'], width=2),
            fill='tonexty'
        ), row=1, col=1)
        
        # 交易量变化
        fig.add_trace(go.Bar(
            x=data['date'],
            y=data['trading_volume'],
            name='交易量(吨)',
            marker_color=COLORS['success'],
            opacity=0.7
        ), row=2, col=1)
        
        # 交易金额趋势
        fig.add_trace(go.Scatter(
            x=data['date'],
            y=data['trading_value'],
            mode='lines+markers',
            name='交易金额(百万元)',
            line=dict(color=COLORS['warning'], width=3),
            marker=dict(size=6)
        ), row=3, col=1)
        
        fig.update_layout(
            height=900,
            title_text="全国碳市场交易分析",
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def plot_ccer_impact_analysis(self, companies_data: pd.DataFrame, results: Dict) -> go.Figure:
        """绘制CCER影响分析图"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CCER参与对企业规模的影响', 'CCER参与对绿色创新的影响', 
                          '研发投入强度对比', '国企vs非国企差异'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 按年份和CCER参与情况分组
        grouped = companies_data.groupby(['year', 'ccer_participation']).agg({
            'total_assets': 'mean',
            'green_patents': 'mean',
            'rd_intensity': 'mean'
        }).reset_index()
        
        # 企业规模影响
        treatment_assets = grouped[grouped['ccer_participation'] == 1]
        control_assets = grouped[grouped['ccer_participation'] == 0]
        
        fig.add_trace(go.Scatter(
            x=treatment_assets['year'],
            y=treatment_assets['total_assets'],
            mode='lines+markers',
            name='CCER参与企业',
            line=dict(color=COLORS['success'], width=3)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=control_assets['year'],
            y=control_assets['total_assets'],
            mode='lines+markers',
            name='非CCER参与企业',
            line=dict(color=COLORS['danger'], width=3)
        ), row=1, col=1)
        
        # 绿色创新影响
        treatment_innovation = grouped[grouped['ccer_participation'] == 1]
        control_innovation = grouped[grouped['ccer_participation'] == 0]
        
        fig.add_trace(go.Scatter(
            x=treatment_innovation['year'],
            y=treatment_innovation['green_patents'],
            mode='lines+markers',
            name='CCER参与企业(创新)',
            line=dict(color=COLORS['success'], width=3),
            showlegend=False
        ), row=1, col=2)
        
        fig.add_trace(go.Scatter(
            x=control_innovation['year'],
            y=control_innovation['green_patents'],
            mode='lines+markers',
            name='非CCER参与企业(创新)',
            line=dict(color=COLORS['danger'], width=3),
            showlegend=False
        ), row=1, col=2)
        
        # 研发投入强度对比
        fig.add_trace(go.Scatter(
            x=treatment_innovation['year'],
            y=treatment_innovation['rd_intensity'],
            mode='lines+markers',
            name='CCER参与企业(研发)',
            line=dict(color=COLORS['success'], width=3),
            showlegend=False
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=control_innovation['year'],
            y=control_innovation['rd_intensity'],
            mode='lines+markers',
            name='非CCER参与企业(研发)',
            line=dict(color=COLORS['danger'], width=3),
            showlegend=False
        ), row=2, col=1)
        
        # 国企vs非国企差异
        effect_comparison = pd.DataFrame({
            'category': ['国有企业', '非国有企业'],
            'rd_effect': [results['soe_rd_effect'], results['non_soe_rd_effect']]
        })
        
        colors = ['red' if x < 0 else 'green' for x in effect_comparison['rd_effect']]
        
        fig.add_trace(go.Bar(
            x=effect_comparison['category'],
            y=effect_comparison['rd_effect'],
            marker_color=colors,
            text=[f'{x:.4f}' for x in effect_comparison['rd_effect']],
            textposition='auto',
            showlegend=False
        ), row=2, col=2)
        
        # 添加零线
        fig.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)
        
        fig.update_layout(
            height=800,
            title_text="CCER机制对光伏发电企业的双重影响分析",
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def plot_photovoltaic_industry_overview(self, companies_data: pd.DataFrame) -> go.Figure:
        """绘制光伏行业概览图"""
        # 按年份汇总数据
        annual_summary = companies_data.groupby('year').agg({
            'revenue': 'sum',
            'rd_investment': 'sum',
            'green_patents': 'sum',
            'ccer_participation': 'mean',
            'carbon_emission_intensity': 'mean'
        }).reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('行业营收增长', '研发投入趋势', '绿色专利积累', 'CCER参与度与碳强度'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": True}]]
        )
        
        # 行业营收增长
        fig.add_trace(go.Scatter(
            x=annual_summary['year'],
            y=annual_summary['revenue'],
            mode='lines+markers',
            name='总营收(亿元)',
            line=dict(color=COLORS['primary'], width=3),
            fill='tonexty'
        ), row=1, col=1)
        
        # 研发投入趋势
        fig.add_trace(go.Bar(
            x=annual_summary['year'],
            y=annual_summary['rd_investment'],
            name='研发投入(亿元)',
            marker_color=COLORS['info'],
            opacity=0.7
        ), row=1, col=2)
        
        # 绿色专利积累
        fig.add_trace(go.Scatter(
            x=annual_summary['year'],
            y=annual_summary['green_patents'].cumsum(),
            mode='lines+markers',
            name='累计绿色专利',
            line=dict(color=COLORS['success'], width=3),
            marker=dict(size=8)
        ), row=2, col=1)
        
        # CCER参与度与碳强度（双Y轴）
        fig.add_trace(go.Scatter(
            x=annual_summary['year'],
            y=annual_summary['ccer_participation'] * 100,
            mode='lines+markers',
            name='CCER参与度(%)',
            line=dict(color=COLORS['warning'], width=3)
        ), row=2, col=2)
        
        fig.add_trace(go.Scatter(
            x=annual_summary['year'],
            y=annual_summary['carbon_emission_intensity'],
            mode='lines+markers',
            name='碳排放强度',
            line=dict(color=COLORS['danger'], width=3),
            yaxis='y2'
        ), row=2, col=2)
        
        fig.update_layout(
            height=800,
            title_text="中国光伏发电行业发展概览",
            showlegend=True,
            template='plotly_white'
        )
        
        # 设置双Y轴
        fig.update_yaxes(title_text="CCER参与度(%)", row=2, col=2)
        fig.update_yaxes(title_text="碳排放强度", secondary_y=True, row=2, col=2)
        
        return fig
    
    def save_figure(self, fig, filename: str, format: str = 'html'):
        """保存图表"""
        if format == 'html':
            fig.write_html(f"src/data/{filename}.html")
        elif format == 'png':
            fig.write_image(f"src/data/{filename}.png", width=1200, height=800)
        elif format == 'pdf':
            fig.write_image(f"src/data/{filename}.pdf", width=1200, height=800)

if __name__ == "__main__":
    # 测试可视化功能
    viz = CarbonVisualization()
    print("可视化模块已就绪！")