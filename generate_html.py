#!/usr/bin/env python3
"""
HTML 生成器 - 重新生成整个日报网页
"""

import json
from datetime import datetime, timedelta


def load_news_data(filepath='/Users/bytedance/daily_news_system/news_data.json'):
    """加载新闻数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def generate_news_js(news_data):
    """生成新闻 JavaScript 代码"""
    date = news_data['date']

    def format_news_list(news_list):
        items = []
        for news in news_list:
            translated = 'true' if news.get('translated') else 'false'
            tags = json.dumps(news.get('tags', []), ensure_ascii=False)
            items.append(f'''            {{
                title: "{news['title']}",
                summary: "{news['summary']}",
                source: "{news['source']}",
                date: "{news['date']}",
                translated: {translated},
                tags: {tags}
            }}''')
        return ',\n'.join(items)

    return f'''const newsDatabase = {{
    "{date}": {{
        ai: [
{format_news_list(news_data['ai'])}
        ],
        internet: [
{format_news_list(news_data['internet'])}
        ],
        tech: [
{format_news_list(news_data['tech'])}
        ],
        ev: [
{format_news_list(news_data['ev'])}
        ]
    }}
}};'''


def generate_html(news_data):
    """生成完整的 HTML 文件"""
    date = news_data['date']
    display_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y年%m月%d日")

    yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_ago = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
    three_days_ago = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=3)).strftime("%Y-%m-%d")

    news_js = generate_news_js(news_data)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球资讯日报 - {display_date}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; font-weight: 700; }}
        .header .date {{ font-size: 1.1em; opacity: 0.8; color: #a0a0a0; }}
        .date-filter {{
            background: white;
            border-radius: 16px;
            padding: 20px 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .date-filter label {{ font-weight: 600; color: #333; font-size: 1.1em; }}
        .date-filter input[type="date"] {{
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            outline: none;
            transition: border-color 0.3s;
            cursor: pointer;
        }}
        .date-filter input[type="date"]:focus {{ border-color: #45B7D1; }}
        .date-filter button, .export-btn {{
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .date-filter button:hover, .export-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        .export-section {{ text-align: center; margin-bottom: 20px; }}
        .export-btn {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
        .quick-dates {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }}
        .quick-date-btn {{
            padding: 8px 16px;
            background: #f0f0f0;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
        }}
        .quick-date-btn:hover {{ background: #e0e0e0; }}
        .quick-date-btn.active {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        .section {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid;
        }}
        .section-icon {{ font-size: 2em; margin-right: 12px; }}
        .section-title {{ font-size: 1.5em; font-weight: 700; }}
        .section.ai .section-header {{ border-color: #FF6B6B; }}
        .section.ai .section-title {{ color: #FF6B6B; }}
        .section.internet .section-header {{ border-color: #4ECDC4; }}
        .section.internet .section-title {{ color: #4ECDC4; }}
        .section.tech .section-header {{ border-color: #45B7D1; }}
        .section.tech .section-title {{ color: #45B7D1; }}
        .section.ev .section-header {{ border-color: #96CEB4; }}
        .section.ev .section-title {{ color: #96CEB4; }}
        .news-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }}
        .news-item:hover {{ transform: translateX(5px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .section.ai .news-item:hover {{ border-left-color: #FF6B6B; }}
        .section.internet .news-item:hover {{ border-left-color: #4ECDC4; }}
        .section.tech .news-item:hover {{ border-left-color: #45B7D1; }}
        .section.ev .news-item:hover {{ border-left-color: #96CEB4; }}
        .news-title {{ font-size: 1.15em; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; line-height: 1.4; }}
        .news-summary {{ font-size: 0.95em; color: #666; line-height: 1.6; margin-bottom: 10px; }}
        .translated-badge {{
            display: inline-block;
            background: transparent;
            color: #667eea;
            font-size: 0.7em;
            padding: 2px 8px;
            border-radius: 10px;
            margin-right: 6px;
            font-weight: 600;
            vertical-align: middle;
            border: 1.5px solid #667eea;
        }}
        .news-source {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 0.85em;
            color: #667eea;
            text-decoration: none;
            padding: 5px 12px;
            background: white;
            border-radius: 15px;
            border: 1px solid #e0e0e0;
            transition: all 0.2s;
            margin-left: auto;
        }}
        .news-source:hover {{ background: #667eea; color: white; border-color: #667eea; }}
        .news-footer {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}
        .news-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }}
        .news-tag {{
            display: inline-block;
            font-size: 0.75em;
            padding: 3px 10px;
            border-radius: 12px;
            background: #f0f0f0;
            color: #666;
            transition: all 0.2s;
        }}
        .news-tag:hover {{
            background: #e0e0e0;
            transform: translateY(-1px);
        }}
        .section.ai .news-tag {{ background: rgba(255, 107, 107, 0.1); color: #FF6B6B; }}
        .section.ai .news-tag:hover {{ background: rgba(255, 107, 107, 0.2); }}
        .section.internet .news-tag {{ background: rgba(78, 205, 196, 0.1); color: #4ECDC4; }}
        .section.internet .news-tag:hover {{ background: rgba(78, 205, 196, 0.2); }}
        .section.tech .news-tag {{ background: rgba(69, 183, 209, 0.1); color: #45B7D1; }}
        .section.tech .news-tag:hover {{ background: rgba(69, 183, 209, 0.2); }}
        .section.ev .news-tag {{ background: rgba(150, 206, 180, 0.1); color: #5a9c7a; }}
        .section.ev .news-tag:hover {{ background: rgba(150, 206, 180, 0.2); }}
        .loading {{
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            z-index: 1000;
        }}
        .loading.show {{ display: block; }}
        .footer {{ text-align: center; padding: 30px; color: #999; font-size: 0.9em; }}

        /* Desktop Styles - Large Screens */
        @media (min-width: 1024px) {{
            body {{ padding: 30px; }}
            .container {{ max-width: 1400px; }}
            .header {{
                padding: 60px;
                border-radius: 24px;
                margin-bottom: 30px;
            }}
            .header h1 {{ font-size: 3.5em; margin-bottom: 15px; }}
            .header .date {{ font-size: 1.3em; }}
            .date-filter {{
                padding: 25px 40px;
                margin-bottom: 30px;
                border-radius: 20px;
            }}
            .date-filter label {{ font-size: 1.2em; }}
            .date-filter input[type="date"] {{ padding: 12px 18px; font-size: 1.1em; }}
            .date-filter button, .export-btn {{ padding: 12px 25px; font-size: 1.1em; }}
            .quick-date-btn {{ padding: 10px 20px; font-size: 1em; }}

            /* Desktop: Two-column layout for news sections */
            #newsContainer {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 25px;
            }}
            .section {{
                padding: 30px;
                margin-bottom: 0;
                border-radius: 20px;
            }}
            .section-header {{ margin-bottom: 25px; padding-bottom: 18px; }}
            .section-icon {{ font-size: 2.5em; margin-right: 15px; }}
            .section-title {{ font-size: 1.6em; }}

            .news-item {{
                padding: 25px;
                margin-bottom: 18px;
                border-radius: 14px;
            }}
            .news-title {{ font-size: 1.25em; margin-bottom: 10px; }}
            .news-summary {{ font-size: 1em; line-height: 1.7; }}
            .news-tag {{ font-size: 0.8em; padding: 4px 12px; }}
            .news-source {{ font-size: 0.9em; padding: 6px 15px; }}
            .translated-badge {{ font-size: 0.75em; padding: 3px 10px; }}
        }}

        /* Tablet Styles - Medium Screens */
        @media (min-width: 768px) and (max-width: 1023px) {{
            .container {{ max-width: 100%; }}
            .header h1 {{ font-size: 2.8em; }}
            #newsContainer {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }}
            .section {{ margin-bottom: 0; }}
        }}

        @media (max-width: 600px) {{
            .header h1 {{ font-size: 1.8em; }}
            .section {{ padding: 20px; }}
            .section-title {{ font-size: 1.3em; }}
            .news-title {{ font-size: 1em; }}
            body {{ padding: 10px; }}
            .date-filter {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 全球资讯日报</h1>
            <div class="date" id="currentDate">{display_date}</div>
        </div>

        <div class="date-filter">
            <label>📅 选择日期：</label>
            <input type="date" id="datePicker" value="{date}" min="{three_days_ago}" max="{date}">
            <button onclick="loadNews()">查看日报</button>
            <div class="quick-dates">
                <button class="quick-date-btn active" onclick="setDate('{date}')">今天</button>
                <button class="quick-date-btn" onclick="setDate('{yesterday}')">昨天</button>
                <button class="quick-date-btn" onclick="setDate('{two_days_ago}')">前天</button>
            </div>
        </div>

        <div class="export-section">
            <button class="export-btn" onclick="exportImage()">
                <span>📸</span>
                <span>导出长图</span>
            </button>
        </div>

        <div id="exportArea"></div>
        <div id="newsContainer"></div>

        <div class="footer">
            Generated by Claude Code · 每日资讯日报 · 最后更新: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </div>
    </div>

    <div class="loading" id="loading">正在生成图片...</div>

    <script>
{news_js}

        const sections = {{
            ai: {{ icon: "🤖", title: "AI 人工智能" }},
            internet: {{ icon: "🌐", title: "互联网" }},
            tech: {{ icon: "💻", title: "科技" }},
            ev: {{ icon: "🚗", title: "新能源汽车" }}
        }};

        let currentDate = '{date}';

        function loadNews() {{
            currentDate = document.getElementById('datePicker').value;
            renderNews(currentDate);
        }}

        function renderNews(date) {{
            const container = document.getElementById('newsContainer');
            const currentDateEl = document.getElementById('currentDate');
            const dateObj = new Date(date);
            currentDateEl.textContent = `${{dateObj.getFullYear()}}年${{String(dateObj.getMonth() + 1).padStart(2, '0')}}月${{String(dateObj.getDate()).padStart(2, '0')}}日`;

            document.querySelectorAll('.quick-date-btn').forEach(btn => btn.classList.remove('active'));

            const newsData = newsDatabase[date];
            if (!newsData) {{
                container.innerHTML = '<div class="section" style="text-align:center;padding:60px;color:#999;"><div style="font-size:4em;margin-bottom:20px;">📭</div><div style="font-size:1.2em;">暂无 ' + date + ' 的资讯记录</div></div>';
                return;
            }}

            let html = '';
            for (const [key, config] of Object.entries(sections)) {{
                if (newsData[key] && newsData[key].length > 0) {{
                    html += `<div class="section ${{key}}"><div class="section-header"><span class="section-icon">${{config.icon}}</span><span class="section-title">${{config.title}}</span></div>`;
                    newsData[key].forEach(news => {{
                        const translatedBadge = news.translated ? '<span class="translated-badge">译</span>' : '';
                        const tagsHtml = news.tags && news.tags.length > 0 ? news.tags.map(tag => `<span class="news-tag">${{tag}}</span>`).join('') : '';
                        const footerContent = translatedBadge || tagsHtml ? `${{translatedBadge}}${{tagsHtml}}` : '';
                        html += `<div class="news-item"><div class="news-title">${{news.title}}</div><div class="news-summary">${{news.summary}}</div><div class="news-footer">${{footerContent}}<a href="${{news.source}}" target="_blank" class="news-source" onclick="event.stopPropagation()">🔗 查看来源</a></div></div>`;
                    }});
                    html += '</div>';
                }}
            }}
            container.innerHTML = html;
        }}

        function setDate(date) {{
            document.getElementById('datePicker').value = date;
            renderNews(date);
            document.querySelectorAll('.quick-date-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.textContent === '今天' && date === '{date}') btn.classList.add('active');
                if (btn.textContent === '昨天' && date === '{yesterday}') btn.classList.add('active');
                if (btn.textContent === '前天' && date === '{two_days_ago}') btn.classList.add('active');
            }});
        }}

        async function exportImage() {{
            const loading = document.getElementById('loading');
            const exportBtn = document.querySelector('.export-btn');
            try {{
                loading.classList.add('show');
                exportBtn.disabled = true;
                const newsData = newsDatabase[currentDate];
                if (!newsData) {{ alert('暂无该日期的资讯数据'); return; }}

                const exportArea = document.getElementById('exportArea');
                const dateObj = new Date(currentDate);
                const dateStr = `${{dateObj.getFullYear()}}年${{String(dateObj.getMonth() + 1).padStart(2, '0')}}月${{String(dateObj.getDate()).padStart(2, '0')}}日`;

                let exportHTML = `<div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:white;padding:50px 40px;text-align:center;"><h1 style="font-size:2.8em;margin-bottom:15px;font-weight:700;">📰 全球资讯日报</h1><div style="font-size:1.3em;opacity:0.9;color:#a0a0a0;">${{dateStr}}</div></div><div style="padding:30px;background:white;">`;

                for (const [key, config] of Object.entries(sections)) {{
                    if (newsData[key] && newsData[key].length > 0) {{
                        const sectionColor = {{ai:'#FF6B6B',internet:'#4ECDC4',tech:'#45B7D1',ev:'#96CEB4'}}[key];
                        exportHTML += `<div style="margin-bottom:30px;"><div style="display:flex;align-items:center;margin-bottom:20px;padding-bottom:15px;border-bottom:3px solid ${{sectionColor}};"><span style="font-size:2em;margin-right:12px;">${{config.icon}}</span><span style="font-size:1.5em;font-weight:700;color:${{sectionColor}};">${{config.title}}</span></div>`;
                        newsData[key].forEach(news => {{
                            const translatedBadge = news.translated ? '<span style="display:inline-block;background:transparent;color:#667eea;font-size:0.7em;padding:2px 8px;border-radius:10px;margin-right:6px;font-weight:600;vertical-align:middle;border:1.5px solid #667eea;">译</span>' : '';
                            const tagsText = news.tags && news.tags.length > 0 ? news.tags.map(tag => `<span style="font-size:0.75em;padding:3px 10px;border-radius:12px;background:rgba(102,126,234,0.1);color:#667eea;margin-right:6px;">${{tag}}</span>`).join('') : '';
                            const footerContent = translatedBadge || tagsText ? `${{translatedBadge}}${{tagsText}}` : '';
                            exportHTML += `<div style="background:#f8f9fa;border-radius:12px;padding:20px;margin-bottom:15px;border-left:4px solid ${{sectionColor}};"><div style="font-size:1.15em;font-weight:600;color:#1a1a2e;margin-bottom:8px;line-height:1.4;">${{news.title}}</div><div style="font-size:0.95em;color:#666;line-height:1.6;margin-bottom:10px;">${{news.summary}}</div><div style="display:flex;align-items:center;justify-content:space-between;margin-top:12px;">${{footerContent}}<span style="font-size:0.8em;color:#999;">来源: ${{new URL(news.source).hostname}}</span></div></div>`;
                        }});
                        exportHTML += '</div>';
                    }}
                }}

                exportHTML += '</div><div style="background:#f5f5f5;padding:20px;text-align:center;color:#999;font-size:0.9em;">Generated by Claude Code · 每日资讯日报</div>';
                exportArea.innerHTML = exportHTML;
                await new Promise(resolve => setTimeout(resolve, 100));

                const canvas = await html2canvas(exportArea, {{ scale: 2, useCORS: true, allowTaint: true, backgroundColor: '#ffffff', logging: false, windowWidth: 800, width: 800 }});
                const link = document.createElement('a');
                link.download = `全球资讯日报_${{currentDate}}.png`;
                link.href = canvas.toDataURL('image/png', 1.0);
                link.click();
                exportArea.innerHTML = '';
            }} catch (error) {{
                console.error('导出失败:', error);
                alert('导出失败，请重试');
            }} finally {{
                loading.classList.remove('show');
                exportBtn.disabled = false;
            }}
        }}

        window.onload = function() {{ renderNews(currentDate); }};
        document.getElementById('datePicker').addEventListener('change', function() {{ currentDate = this.value; renderNews(currentDate); }});
    </script>
</body>
</html>'''

    return html


def main():
    print("🔄 开始生成日报网页...")

    news_data = load_news_data()
    if not news_data:
        print("❌ 未找到新闻数据，请先运行 news_fetcher.py")
        return

    html = generate_html(news_data)

    output_path = '/Users/bytedance/daily_news.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 网页已生成: {output_path}")
    print(f"📅 日期: {news_data['date']}")
    total = sum(len(news_data[k]) for k in ['ai', 'internet', 'tech', 'ev'])
    print(f"📊 共 {total} 条资讯")


if __name__ == '__main__':
    main()
