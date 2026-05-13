#!/usr/bin/env python3
"""
RSS 新闻抓取器
自动从各领域的 RSS 源获取最新资讯
"""

import feedparser
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
import time
from deep_translator import GoogleTranslator
import jieba
import jieba.analyse


class RSSFetcher:
    """RSS 抓取器"""

    # 各领域 RSS 源配置
    RSS_SOURCES = {
        'ai': [
            {
                'name': '机器之心',
                'url': 'https://www.jiqizhixin.com/rss',
                'language': 'zh',
                'weight': 10  # 权重，越高越优先
            },
            {
                'name': '量子位',
                'url': 'https://www.qbitai.com/rss',
                'language': 'zh',
                'weight': 9
            },
            {
                'name': 'PaperWeekly',
                'url': 'https://www.paperweekly.site/rss',
                'language': 'zh',
                'weight': 8
            },
            {
                'name': 'OpenAI Blog',
                'url': 'https://openai.com/blog/rss.xml',
                'language': 'en',
                'weight': 10
            }
        ],
        'internet': [
            {
                'name': '36kr',
                'url': 'https://36kr.com/feed',
                'language': 'zh',
                'weight': 10
            },
            {
                'name': '虎嗅',
                'url': 'https://www.huxiu.com/rss',
                'language': 'zh',
                'weight': 9
            },
            {
                'name': '晚点LatePost',
                'url': 'https://www.latepost.com/rss',
                'language': 'zh',
                'weight': 8
            }
        ],
        'tech': [
            {
                'name': '爱范儿',
                'url': 'https://www.ifanr.com/feed',
                'language': 'zh',
                'weight': 10
            },
            {
                'name': '少数派',
                'url': 'https://sspai.com/feed',
                'language': 'zh',
                'weight': 9
            },
            {
                'name': 'Solidot',
                'url': 'https://www.solidot.org/index.rss',
                'language': 'zh',
                'weight': 7
            },
            {
                'name': 'TechCrunch',
                'url': 'https://techcrunch.com/feed/',
                'language': 'en',
                'weight': 8
            }
        ],
        'ev': [
            {
                'name': '42号车库',
                'url': 'https://www.42how.com/rss',
                'language': 'zh',
                'weight': 10
            },
            {
                'name': 'Electrek',
                'url': 'https://electrek.co/feed/',
                'language': 'en',
                'weight': 9
            },
            {
                'name': 'InsideEVs',
                'url': 'https://insideevs.com/rss/news/all/',
                'language': 'en',
                'weight': 8
            }
        ]
    }

    def __init__(self):
        self.today = datetime.now()
        self.today_str = self.today.strftime("%Y-%m-%d")
        self.yesterday = (self.today - timedelta(days=1)).strftime("%Y-%m-%d")
        self.translator = GoogleTranslator(source='en', target='zh-CN')
        self._translation_cache = {}  # 缓存翻译结果避免重复翻译

    def _extract_keywords(self, title, summary, source_name, category):
        """提取文章关键词标签"""
        tags = []

        # 1. 添加来源标签
        source_tag_map = {
            '36kr': '36氪',
            '虎嗅': '虎嗅',
            '晚点LatePost': '晚点',
            '机器之心': '机器之心',
            '量子位': '量子位',
            'OpenAI Blog': 'OpenAI',
            '爱范儿': '爱范儿',
            '少数派': '少数派',
            'Solidot': 'Solidot',
            'TechCrunch': 'TechCrunch',
            '42号车库': '42号车库',
            'Electrek': 'Electrek',
            'InsideEVs': 'InsideEVs',
            'PaperWeekly': 'PaperWeekly'
        }
        if source_name in source_tag_map:
            tags.append(f"#{source_tag_map[source_name]}")

        # 2. 根据分类添加领域标签
        category_tags = {
            'ai': ['#AI', '#人工智能'],
            'internet': ['#互联网', '#商业'],
            'tech': ['#科技', '#数码'],
            'ev': ['#新能源', '#汽车']
        }
        if category in category_tags:
            tags.append(category_tags[category][0])

        # 3. 从标题提取关键词（使用 jieba）
        text = f"{title} {summary}"
        # 提取前 2 个关键词
        keywords = jieba.analyse.extract_tags(text, topK=2, withWeight=False)
        for kw in keywords:
            if len(kw) >= 2 and kw not in ['nbsp', '作者', '编辑', '获悉']:
                tags.append(f"#{kw}")
                break  # 只取 1 个内容关键词，避免标签太多

        return tags[:3]  # 最多返回 3 个标签

    def fetch_feed(self, url, name):
        """获取单个 RSS Feed"""
        try:
            print(f"  📡 正在获取: {name}...")
            feed = feedparser.parse(url)

            if feed.bozo:
                print(f"  ⚠️  {name} 解析警告: {feed.get('bozo_exception', 'Unknown')}")

            entries = []
            for entry in feed.entries[:10]:  # 只取前10条
                # 解析发布时间
                published = self._parse_date(entry)

                # 只保留今天和昨天的文章
                if published and published >= self.yesterday:
                    entries.append({
                        'title': entry.get('title', '无标题'),
                        'summary': self._clean_summary(entry.get('summary', entry.get('description', '暂无摘要'))),
                        'link': entry.get('link', ''),
                        'published': published,
                        'source_name': name
                    })

            print(f"  ✅ {name}: 获取 {len(entries)} 条今日文章")
            return entries

        except Exception as e:
            print(f"  ❌ {name} 获取失败: {str(e)[:50]}")
            return []

    def _parse_date(self, entry):
        """解析 RSS 日期"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']

        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    dt = datetime(*getattr(entry, field)[:6])
                    return dt.strftime("%Y-%m-%d")
                except:
                    continue

        # 尝试从字符串解析
        date_strings = ['published', 'updated', 'created', 'pubDate']
        for field in date_strings:
            if hasattr(entry, field):
                date_str = getattr(entry, field)
                try:
                    # 常见 RSS 日期格式
                    for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                        try:
                            dt = datetime.strptime(date_str[:19], fmt[:19])
                            return dt.strftime("%Y-%m-%d")
                        except:
                            continue
                except:
                    continue

        # 默认返回今天
        return self.today_str

    def _translate_text(self, text, max_length=4000):
        """翻译文本，带缓存和长度限制"""
        if not text or len(text.strip()) < 5:
            return text

        # 使用缓存
        cache_key = text[:100]  # 前100字符作为缓存键
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]

        try:
            # 截断过长的文本
            text_to_translate = text[:max_length] if len(text) > max_length else text
            translated = self.translator.translate(text_to_translate)
            self._translation_cache[cache_key] = translated
            return translated
        except Exception as e:
            print(f"  ⚠️  翻译失败: {str(e)[:30]}")
            return text

    def _clean_summary(self, summary):
        """清理摘要文本"""
        if not summary:
            return "暂无摘要"

        # 移除 HTML 标签
        clean = re.sub('<.*?>', '', summary)
        # 移除多余空白
        clean = ' '.join(clean.split())
        # 限制长度
        if len(clean) > 150:
            clean = clean[:147] + '...'

        return clean

    def fetch_all_news(self):
        """获取所有领域的 RSS 新闻"""
        all_news = {
            'date': self.today_str,
            'ai': [],
            'internet': [],
            'tech': [],
            'ev': []
        }

        print(f"\n🔍 开始获取 {self.today_str} 的 RSS 资讯...\n")

        for category, sources in self.RSS_SOURCES.items():
            print(f"\n📂 {category.upper()} 领域:")
            category_news = []

            for source in sorted(sources, key=lambda x: x['weight'], reverse=True):
                entries = self.fetch_feed(source['url'], source['name'])

                for entry in entries:
                    # 判断是否需要翻译（英文来源）
                    needs_translation = source.get('language') == 'en'

                    # 如果是英文来源，翻译标题和摘要
                    title = entry['title']
                    summary = entry['summary']
                    if needs_translation:
                        print(f"    🔄 翻译: {title[:30]}...")
                        title = self._translate_text(title)
                        summary = self._translate_text(summary)

                    # 提取关键词标签
                    tags = self._extract_keywords(title, summary, entry['source_name'], category)

                    news_item = {
                        'title': title,
                        'summary': summary,
                        'source': entry['link'],
                        'date': entry['published'],
                        'source_name': entry['source_name'],
                        'translated': needs_translation,  # 标记是否翻译
                        'tags': tags  # 添加标签
                    }
                    category_news.append(news_item)

                time.sleep(0.5)  # 礼貌性延迟

            # 去重（按标题）
            seen_titles = set()
            unique_news = []
            for news in category_news:
                title_key = news['title'][:20]  # 前20字符作为去重键
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    unique_news.append(news)

            # 只保留前5条
            all_news[category] = unique_news[:5]
            print(f"   📊 共 {len(all_news[category])} 条（去重后）")

        return all_news

    def check_sources(self):
        """检查 RSS 源是否可用"""
        print("\n🔍 检查 RSS 源状态...\n")

        for category, sources in self.RSS_SOURCES.items():
            print(f"\n{category.upper()}:")
            for source in sources:
                try:
                    feed = feedparser.parse(source['url'])
                    if feed.entries:
                        print(f"  ✅ {source['name']}: 正常 ({len(feed.entries)} 篇文章)")
                    else:
                        print(f"  ⚠️  {source['name']}: 无文章")
                except Exception as e:
                    print(f"  ❌ {source['name']}: 无法访问 ({str(e)[:30]})")


def save_news_data(news_data, filepath='/Users/bytedance/daily_news_system/news_data.json'):
    """保存新闻数据"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 新闻数据已保存: {filepath}")


def main():
    fetcher = RSSFetcher()

    # 先检查 RSS 源状态（可选）
    # fetcher.check_sources()

    # 获取新闻
    news = fetcher.fetch_all_news()

    # 统计
    total = sum(len(news[cat]) for cat in ['ai', 'internet', 'tech', 'ev'])

    if total == 0:
        print("\n⚠️ 警告: 未获取到任何今日资讯")
        print("   可能原因:")
        print("   1. RSS 源暂时不可用")
        print("   2. 今日暂无新文章发布")
        print("   3. 网络连接问题")
        print("\n   将使用备用数据...")

        # 使用备用数据
        from backup_data import get_backup_news
        news = get_backup_news()

    save_news_data(news)

    print(f"\n📊 资讯统计:")
    print(f"   AI: {len(news['ai'])} 条")
    print(f"   互联网: {len(news['internet'])} 条")
    print(f"   科技: {len(news['tech'])} 条")
    print(f"   新能源汽车: {len(news['ev'])} 条")
    print(f"   总计: {total} 条")


if __name__ == '__main__':
    main()
