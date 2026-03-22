# rss/notify.py

import os
import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta

import requests

REPO = "chainlinn/chainlinn.github.io"


def send_showdoc(title: str, content: str):
    """发送通知到 ShowDoc 推送服务。"""
    url = os.environ.get("SHOWDOC_PUSH_URL")
    if not url:
        print("未配置 SHOWDOC_PUSH_URL 环境变量，跳过推送。")
        return False
    try:
        resp = requests.post(url, data={"title": title, "content": content}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("error_code") == 0:
            print("✅ ShowDoc 推送成功！")
            return True
        else:
            print(f"❌ ShowDoc 推送失败: {data.get('error_message', '未知错误')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ ShowDoc 推送请求失败: {e}")
    except json.JSONDecodeError:
        print("❌ ShowDoc 推送失败: 无法解析服务器响应。")
    return False


def notify_articles():
    """检测本次提交中 content/ 目录的变更，推送文章更新通知。"""
    print("--- 检测文章变更... ---")
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", "HEAD~1", "--", "content/"],
            capture_output=True, text=True, timeout=30
        )
        changes = result.stdout.strip()
    except Exception as e:
        print(f"无法获取 git diff: {e}")
        return

    if not changes:
        print("本次提交没有文章变更，跳过通知。")
        return

    added, modified, deleted = [], [], []
    for line in changes.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        status, filepath = parts
        # 跳过 _index.md
        if filepath.endswith("_index.md"):
            continue
        name = filepath.replace("content/", "", 1)
        if status.startswith("A"):
            added.append(name)
        elif status.startswith("M"):
            modified.append(name)
        elif status.startswith("D"):
            deleted.append(name)

    if not added and not modified and not deleted:
        print("仅有 _index.md 变更，跳过通知。")
        return

    lines = []
    for f in added:
        lines.append(f"- ✅ 新增: {f}")
    for f in modified:
        lines.append(f"- 📝 修改: {f}")
    for f in deleted:
        lines.append(f"- 🗑️ 删除: {f}")

    total = len(added) + len(modified) + len(deleted)
    title = f"📝 博客文章更新（{total} 个文件变更）"
    content = "#### 本次部署变更：\n" + "\n".join(lines) + f"\n\n共 {total} 个文件变更"

    print(f"检测到 {total} 个文件变更，正在推送...")
    send_showdoc(title, content)


def notify_visitors():
    """通过 GitHub API 获取流量数据，推送访客活跃度报告。"""
    print("--- 获取访客统计... ---")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("未配置 GITHUB_TOKEN 环境变量，跳过访客统计。")
        return

    try:
        resp = requests.get(
            f"https://api.github.com/repos/{REPO}/traffic/views",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取 GitHub Traffic 数据失败: {e}")
        return

    views = data.get("views", [])
    if not views:
        print("暂无流量数据。")
        return

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%dT00:00:00Z")
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")

    # 按日期索引
    daily = {v["timestamp"]: v for v in views}

    # 今日数据（可能还没有，用昨日兜底）
    today_data = daily.get(today_str, daily.get(yesterday_str, {}))
    dau = today_data.get("uniques", 0)
    today_views = today_data.get("count", 0)

    # 近 7 天
    week_ago = now - timedelta(days=7)
    wau, week_views = 0, 0
    for v in views:
        ts = datetime.fromisoformat(v["timestamp"].replace("Z", "+00:00"))
        if ts >= week_ago:
            wau += v.get("uniques", 0)
            week_views += v.get("count", 0)

    # 14 天总计（GitHub API 最多 14 天）
    total_uniques = data.get("uniques", 0)
    total_views = data.get("count", 0)

    # 趋势图（简易 bar chart）
    trend_lines = []
    max_uniques = max((v.get("uniques", 0) for v in views), default=1) or 1
    for v in views[-7:]:
        ts = datetime.fromisoformat(v["timestamp"].replace("Z", "+00:00"))
        date_label = ts.strftime("%m/%d")
        uniques = v.get("uniques", 0)
        bar_len = int(uniques / max_uniques * 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        trend_lines.append(f"{date_label} {bar} {uniques}")

    title = f"📊 博客访客报告（DAU: {dau}）"
    content_parts = [
        "#### 访客活跃度",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 今日访客 (DAU) | {dau} |",
        f"| 今日浏览量 | {today_views} |",
        f"| 近7天访客 (WAU) | {wau} |",
        f"| 近7天浏览量 | {week_views} |",
        f"| 近14天独立访客 | {total_uniques} |",
        f"| 近14天总浏览量 | {total_views} |",
        "",
        "#### 近7天趋势",
        "```",
    ]
    content_parts.extend(trend_lines)
    content_parts.append("```")

    content = "\n".join(content_parts)
    print(f"DAU={dau}, WAU={wau}, 14天={total_uniques}，正在推送...")
    send_showdoc(title, content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python notify.py <articles|visitors>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "articles":
        notify_articles()
    elif command == "visitors":
        notify_visitors()
    else:
        print(f"未知命令: {command}")
        print("用法: python notify.py <articles|visitors>")
        sys.exit(1)
