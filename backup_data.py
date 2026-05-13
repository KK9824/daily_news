#!/usr/bin/env python3
"""
备用新闻数据
当 RSS 抓取失败时使用
"""

from datetime import datetime


def get_backup_news():
    """获取备用新闻数据"""
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "date": today,
        "ai": [
            {
                "title": "RSS 源暂时不可用",
                "summary": "请检查网络连接或稍后再试。您可以访问以下网站获取最新 AI 资讯：机器之心、量子位、OpenAI Blog",
                "source": "https://www.jiqizhixin.com",
                "date": today
            }
        ],
        "internet": [
            {
                "title": "RSS 源暂时不可用",
                "summary": "请检查网络连接或稍后再试。您可以访问以下网站获取最新互联网资讯：36kr、虎嗅、晚点LatePost",
                "source": "https://36kr.com",
                "date": today
            }
        ],
        "tech": [
            {
                "title": "RSS 源暂时不可用",
                "summary": "请检查网络连接或稍后再试。您可以访问以下网站获取最新科技资讯：爱范儿、少数派、TechCrunch",
                "source": "https://www.ifanr.com",
                "date": today
            }
        ],
        "ev": [
            {
                "title": "RSS 源暂时不可用",
                "summary": "请检查网络连接或稍后再试。您可以访问以下网站获取最新新能源资讯：42号车库、Electrek、InsideEVs",
                "source": "https://www.42how.com",
                "date": today
            }
        ]
    }
