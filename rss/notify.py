# rss/notify.py

import os
import sys
import json
import subprocess

import requests


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python notify.py articles")
        sys.exit(1)

    command = sys.argv[1]
    if command == "articles":
        notify_articles()
    else:
        print(f"未知命令: {command}")
        print("用法: python notify.py articles")
        sys.exit(1)
