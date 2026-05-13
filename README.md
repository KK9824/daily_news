# 📰 全球资讯日报 - 自动更新系统

## 🚀 快速开始

### 方式 1：手动更新（推荐日常使用）

```bash
# 运行完整更新流程
cd /Users/bytedance/daily_news_system
./run_daily_update.sh

# 或分别执行
python3 news_fetcher.py    # 获取最新新闻
python3 update_html.py      # 更新网页
```

### 方式 2：设置自动定时更新

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上 8:00 自动更新）
0 8 * * * /Users/bytedance/daily_news_system/run_daily_update.sh >> /Users/bytedance/daily_news_system/update.log 2>&1

# 保存退出
```

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `news_fetcher.py` | 新闻抓取器，获取当天最新资讯 |
| `update_html.py` | HTML 更新器，将新闻写入网页 |
| `run_daily_update.sh` | 一键更新脚本 |
| `news_data.json` | 新闻数据存储 |
| `backups/` | 每日数据备份 |

## 📋 每日工作流程

1. **数据获取** (`news_fetcher.py`)
   - 搜索 AI、互联网、科技、新能源四大领域
   - 筛选当天发布的新闻
   - 保存到 `news_data.json`

2. **网页更新** (`update_html.py`)
   - 读取 `news_data.json`
   - 替换 HTML 中的新闻数据
   - 更新日期选择器范围
   - 生成新的 `daily_news.html`

3. **数据备份**
   - 自动备份到 `backups/YYYYMMDD/` 目录

## ⚠️ 重要提示

### 关于数据时效性

目前系统使用的是**内置模板数据**，需要每天手动更新模板中的新闻内容。

**真正自动化的方案：**
1. 接入新闻 API（如新浪财经、36kr、知乎等）
2. 使用 RSS 订阅源
3. 配置网络爬虫

### 如何添加新的新闻源

编辑 `news_fetcher.py`，在对应的方法中添加：

```python
def _get_ai_news(self):
    return [
        {
            "title": "新闻标题",
            "summary": "新闻摘要",
            "source": "https://source-link.com",
            "date": "2025-05-13"  # 确保是今天的日期
        },
        # ... 更多新闻
    ]
```

## 🔧 故障排查

### 网页没有更新
1. 检查 `news_data.json` 是否存在
2. 检查新闻日期是否为今天
3. 运行 `python3 update_html.py` 查看错误信息

### 新闻数据过时
1. 需要更新 `news_fetcher.py` 中的模板数据
2. 或接入真实的新闻 API

### 定时任务不执行
```bash
# 检查 crontab 是否正确设置
crontab -l

# 查看执行日志
tail -f /Users/bytedance/daily_news_system/update.log
```

## 📊 数据格式

`news_data.json` 格式：

```json
{
  "date": "2025-05-13",
  "ai": [
    {
      "title": "新闻标题",
      "summary": "新闻摘要",
      "source": "https://...",
      "date": "2025-05-13"
    }
  ],
  "internet": [...],
  "tech": [...],
  "ev": [...]
}
```

## 🎯 下一步优化

- [ ] 接入真实新闻 API（新浪财经、36kr等）
- [ ] 添加新闻去重功能
- [ ] 支持关键词过滤
- [ ] 添加邮件推送功能
- [ ] 生成每日摘要 PDF

---

**最后更新**: 2025-05-13
