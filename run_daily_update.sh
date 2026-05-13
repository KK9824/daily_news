#!/bin/bash
# 每日资讯自动更新脚本
# 建议添加到 crontab 每天早上 8:00 运行

echo "=========================================="
echo "🌅 开始执行每日资讯更新 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 切换到工作目录
cd /Users/bytedance/daily_news_system

# 1. 获取最新资讯
echo ""
echo "📰 步骤 1/3: 获取最新资讯..."
python3 rss_fetcher.py
if [ $? -ne 0 ]; then
    echo "❌ 获取资讯失败"
    exit 1
fi

# 2. 生成 HTML 网页
echo ""
echo "🌐 步骤 2/3: 生成网页..."
python3 generate_html.py
if [ $? -ne 0 ]; then
    echo "❌ 更新网页失败"
    exit 1
fi

# 3. 备份数据
echo ""
echo "💾 步骤 3/3: 备份数据..."
BACKUP_DIR="backups/$(date '+%Y%m%d')"
mkdir -p "$BACKUP_DIR"
cp news_data.json "$BACKUP_DIR/"
cp /Users/bytedance/daily_news.html "$BACKUP_DIR/"
echo "✅ 已备份到: $BACKUP_DIR"

echo ""
echo "=========================================="
echo "✅ 每日更新完成! - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""
echo "📱 网页位置: /Users/bytedance/daily_news.html"
echo "📊 数据位置: /Users/bytedance/daily_news_system/news_data.json"
