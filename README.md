# 📰 全球资讯日报 - 自动更新系统

> 自动抓取 AI、互联网、科技、新能源汽车四大领域 RSS 资讯，生成响应式网页并部署到 GitHub Pages

## 🔗 快速访问

- **网页地址**: https://KK9824.github.io/daily_news/daily_news.html
- **本地路径**: `/Users/bytedance/daily_news_system/`
- **GitHub 仓库**: https://github.com/KK9824/daily_news

## 🚀 快速开始

### 方式 1：手动更新（推荐日常使用）

```bash
# 进入项目目录
cd /Users/bytedance/daily_news_system

# 运行完整更新流程（抓取 + 生成 + 备份）
./run_daily_update.sh

# 或分别执行
python3 rss_fetcher.py      # 获取最新新闻
python3 generate_html.py    # 生成网页
```

### 方式 2：设置自动定时更新

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上 8:00 自动更新）
0 8 * * * /Users/bytedance/daily_news_system/run_daily_update.sh >> /Users/bytedance/daily_news_system/update.log 2>&1

# 保存退出
```

### 方式 3：手机临时访问（局域网）

```bash
# 启动本地服务器
cd /Users/bytedance && python3 -m http.server 8080

# 手机访问（需同一 WiFi）
# http://电脑IP:8080/daily_news.html
```

## 📁 文件说明

| 文件 | 用途 | 说明 |
|------|------|------|
| `rss_fetcher.py` | RSS 抓取器 | 从 14 个 RSS 源抓取新闻，自动翻译英文内容 |
| `generate_html.py` | 网页生成器 | 生成响应式 HTML，支持手机/电脑双端适配 |
| `run_daily_update.sh` | 一键更新脚本 | 自动执行抓取→生成→备份全流程 |
| `daily_news.html` | 本地网页 | 生成的本地网页文件 |
| `docs/daily_news.html` | 部署文件 | GitHub Pages 部署用的文件 |
| `news_data.json` | 数据文件 | 抓取的新闻数据存储 |
| `backups/` | 备份目录 | 每日数据备份 |

## 📡 RSS 数据源

| 模块 | 数据源 |
|------|--------|
| **AI** | 机器之心、量子位、PaperWeekly、OpenAI Blog |
| **互联网** | 36kr、虎嗅、晚点LatePost |
| **科技** | 爱范儿、少数派、Solidot、TechCrunch |
| **新能源汽车** | 42号车库、Electrek、InsideEVs |

## ✨ 功能特性

- ✅ **RSS 自动抓取** - 从 14 个优质 RSS 源获取资讯
- ✅ **自动翻译** - 英文新闻自动翻译成中文
- ✅ **标签系统** - 显示来源标签（如 #OpenAI）和内容标签
- ✅ **整卡点击** - 点击资讯卡片任意位置跳转源链接
- ✅ **响应式布局** - 电脑双列 / 手机单列自适应
- ✅ **日期筛选** - 查看历史日期的资讯
- ✅ **导出长图** - 一键生成分享长图
- ✅ **翻译标记** - 英文来源显示"译"标签

## 📋 每日工作流程

1. **数据获取** (`rss_fetcher.py`)
   - 从 14 个 RSS 源抓取新闻
   - 自动翻译英文内容
   - 提取关键词标签
   - 保存到 `news_data.json`

2. **网页生成** (`generate_html.py`)
   - 读取 `news_data.json`
   - 生成响应式 HTML
   - 支持电脑/手机双端适配
   - 生成 `daily_news.html`

3. **数据备份**
   - 自动备份到 `backups/YYYYMMDD/` 目录

## 🔧 故障排查

### 网页没有更新
```bash
# 检查新闻数据
python3 rss_fetcher.py

# 检查网页生成
python3 generate_html.py
```

### 定时任务不执行
```bash
# 检查 crontab
crontab -l

# 查看执行日志
tail -f /Users/bytedance/daily_news_system/update.log
```

### 推送到 GitHub Pages
```bash
cp /Users/bytedance/daily_news.html docs/daily_news.html
git add docs/ news_data.json
git commit -m "Update daily news: $(date '+%Y-%m-%d')"
git push origin main
```

---

**最后更新**: 2026-05-14
