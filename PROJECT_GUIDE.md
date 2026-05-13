# 每日资讯日报系统 - 项目指南

## 快速访问

- **本地路径**: `/Users/bytedance/daily_news_system/`
- **GitHub 仓库**: https://github.com/KK9824/daily_news
- **网页地址**: https://KK9824.github.io/daily_news/daily_news.html

---

## 核心文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `rss_fetcher.py` | 抓取 RSS 新闻 | 从 14 个 RSS 源抓取 AI、互联网、科技、新能源汽车资讯 |
| `generate_html.py` | 生成网页 | 生成响应式 HTML 网页，支持手机/电脑双端适配 |
| `run_daily_update.sh` | 每日更新脚本 | 自动执行抓取→生成→备份全流程 |
| `daily_news.html` | 本地网页 | 生成的本地网页文件 |
| `docs/daily_news.html` | 部署文件 | GitHub Pages 部署用的文件 |
| `news_data.json` | 数据文件 | 抓取的新闻数据存储 |

---

## 常用命令

### 进入项目目录
```bash
cd /Users/bytedance/daily_news_system
```

### 手动更新新闻
```bash
python3 rss_fetcher.py && python3 generate_html.py
```

### 一键更新（抓取+生成+备份）
```bash
./run_daily_update.sh
```

### 启动本地服务器（手机临时访问）
```bash
cd /Users/bytedance && python3 -m http.server 8080
# 手机访问: http://电脑IP:8080/daily_news.html
```

### 推送到 GitHub Pages
```bash
cp /Users/bytedance/daily_news.html docs/daily_news.html
git add docs/ news_data.json
git commit -m "Update daily news: $(date '+%Y-%m-%d')"
git push origin main
```

---

## 功能特性

- ✅ 每日自动抓取 RSS 新闻（AI、互联网、科技、新能源汽车）
- ✅ 自动翻译英文内容为中文
- ✅ 显示"译"标签和文章标签（如 #OpenAI #AI）
- ✅ 响应式布局（电脑双列 / 手机单列）
- ✅ 日期筛选功能
- ✅ 导出长图功能
- ✅ 整卡点击跳转源链接

---

## RSS 数据源

| 模块 | 数据源 |
|------|--------|
| AI | 机器之心、量子位、PaperWeekly、OpenAI Blog |
| 互联网 | 36kr、虎嗅、晚点LatePost |
| 科技 | 爱范儿、少数派、Solidot、TechCrunch |
| 新能源汽车 | 42号车库、Electrek、InsideEVs |

---

## 自动任务设置

添加到 crontab 每天早上 8 点自动运行：
```bash
0 8 * * * cd /Users/bytedance/daily_news_system && ./run_daily_update.sh >> /tmp/daily_news.log 2>&1
```

---

## 注意事项

1. GitHub 推送需要配置 Personal Access Token 或使用 SSH 密钥
2. 手机和电脑在同一 WiFi 下可用局域网方式访问
3. 部分 RSS 源（如虎嗅、晚点）可能有解析问题，属于正常现象

---

**最后更新**: 2026-05-13
