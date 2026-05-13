#!/usr/bin/env python3
"""
HTML 更新器 - 将最新新闻数据更新到网页
"""

import json
import re
from datetime import datetime


def load_news_data(filepath='/Users/bytedance/daily_news_system/news_data.json'):
    """加载新闻数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 未找到新闻数据文件")
        return None


def generate_news_javascript(news_data):
    """生成 JavaScript 新闻数据代码"""
    date = news_data['date']

    js_code = f'''        // 每日最新资讯数据库 - 最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        const newsDatabase = {{
            "{date}": {{
                "ai": ['''

    # 添加 AI 新闻
    for i, news in enumerate(news_data['ai']):
        if i > 0:
            js_code += ","
        js_code += f'''
                    {{ title: "{news['title']}", summary: "{news['summary']}", source: "{news['source']}", date: "{news['date']}" }}'''

    js_code += '''
                ],
                "internet": ['''

    # 添加互联网新闻
    for i, news in enumerate(news_data['internet']):
        if i > 0:
            js_code += ","
        js_code += f'''
                    {{ title: "{news['title']}", summary: "{news['summary']}", source: "{news['source']}", date: "{news['date']}" }}'''

    js_code += '''
                ],
                "tech": ['''

    # 添加科技新闻
    for i, news in enumerate(news_data['tech']):
        if i > 0:
            js_code += ","
        js_code += f'''
                    {{ title: "{news['title']}", summary: "{news['summary']}", source: "{news['source']}", date: "{news['date']}" }}'''

    js_code += '''
                ],
                "ev": ['''

    # 添加新能源新闻
    for i, news in enumerate(news_data['ev']):
        if i > 0:
            js_code += ","
        js_code += f'''
                    {{ title: "{news['title']}", summary: "{news['summary']}", source: "{news['source']}", date: "{news['date']}" }}'''

    js_code += '''
                ]
            }
        };'''

    return js_code


def update_html_page(news_data, html_path='/Users/bytedance/daily_news.html'):
    """更新 HTML 文件中的新闻数据"""

    # 读取现有 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 生成新的 JavaScript 数据
    new_js_data = generate_news_javascript(news_data)

    # 替换日期范围
    today = news_data['date']
    yesterday = (datetime.strptime(today, "%Y-%m-%d") - __import__('datetime').timedelta(days=1)).strftime("%Y-%m-%d")
    four_days_ago = (datetime.strptime(today, "%Y-%m-%d") - __import__('datetime').timedelta(days=3)).strftime("%Y-%m-%d")

    # 替换日期选择器的 min 和 max
    html_content = re.sub(
        r'<input type="date" id="datePicker" value="[^"]*" min="[^"]*" max="[^"]*">',
        f'<input type="date" id="datePicker" value="{today}" min="{four_days_ago}" max="{today}">',
        html_content
    )

    # 替换快捷按钮的日期
    html_content = re.sub(
        r"onclick=\"setDate\('\d{4}-\d{2}-\d{2}'\)\"\>今天\<",
        f"onclick=\"setDate('{today}')\">今天<",
        html_content
    )
    html_content = re.sub(
        r"onclick=\"setDate\('\d{4}-\d{2}-\d{2}'\)\"\>昨天\<",
        f"onclick=\"setDate('{yesterday}')\">昨天<",
        html_content
    )

    # 替换新闻数据库（使用正则表达式找到并替换）
    pattern = r'// 每日最新资讯数据库.*?const newsDatabase = \{[\s\S]*?\};'
    if re.search(pattern, html_content):
        html_content = re.sub(pattern, new_js_data, html_content)
    else:
        # 如果没找到，尝试替换旧的静态数据
        pattern2 = r'// 模拟数据库.*?const newsDatabase = \{[\s\S]*?\};'
        if re.search(pattern2, html_content):
            html_content = re.sub(pattern2, new_js_data, html_content)
        else:
            print("⚠️ 未找到新闻数据库标记，请手动检查")
            return False

    # 保存更新后的 HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML 已更新: {html_path}")
    print(f"📅 当前日期: {today}")
    return True


def main():
    print("🔄 开始更新日报网页...")

    # 加载新闻数据
    news_data = load_news_data()
    if not news_data:
        print("❌ 更新失败: 没有新闻数据")
        return

    # 验证数据日期
    today = datetime.now().strftime("%Y-%m-%d")
    if news_data['date'] != today:
        print(f"⚠️ 警告: 新闻数据日期 ({news_data['date']}) 不是今天 ({today})")
        print("   建议先运行 news_fetcher.py 获取今日最新资讯")

    # 更新 HTML
    success = update_html_page(news_data)

    if success:
        print("\n✨ 更新完成!")
        print(f"   共更新 {len(news_data['ai']) + len(news_data['internet']) + len(news_data['tech']) + len(news_data['ev'])} 条资讯")


if __name__ == '__main__':
    main()
