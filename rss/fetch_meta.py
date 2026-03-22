# rss/fetch_meta.py

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
TIMEOUT = 15


def find_external_links():
    """扫描 content/ 下所有含 externalUrl 的 md 文件。"""
    files = []
    for root, _, fnames in os.walk(CONTENT_DIR):
        for f in fnames:
            if not f.endswith(".md") or f == "_index.md":
                continue
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    content = fh.read()
                if "externalUrl:" in content:
                    files.append(path)
            except Exception:
                continue
    return files


def parse_front_matter(content):
    """解析 YAML front matter，返回 (front_matter_dict, body)。"""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not m:
        return {}, content
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().strip('"').strip("'")
            fm[key.strip()] = val
    return fm, body


def write_front_matter(path, fm, body):
    """将 front matter 写回文件。"""
    lines = ["---"]
    for k, v in fm.items():
        if v:
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f"{k}: ")
    lines.append("---")
    lines.append(body if body else "")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def fetch_site_meta(url):
    """抓取网站的标题、描述、图标。"""
    meta = {"title": "", "description": "", "icon": ""}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")

        # title: og:title > <title>
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            meta["title"] = og_title["content"].strip()
        elif soup.title and soup.title.string:
            meta["title"] = soup.title.string.strip()

        # description: og:description > meta description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            meta["description"] = og_desc["content"].strip()
        else:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                meta["description"] = meta_desc["content"].strip()

        # icon: apple-touch-icon > og:image > favicon
        apple_icon = soup.find("link", rel=lambda x: x and "apple-touch-icon" in x)
        if apple_icon and apple_icon.get("href"):
            meta["icon"] = urljoin(url, apple_icon["href"])
        else:
            og_img = soup.find("meta", property="og:image")
            if og_img and og_img.get("content"):
                meta["icon"] = urljoin(url, og_img["content"])
            else:
                icon_link = soup.find("link", rel=lambda x: x and "icon" in x)
                if icon_link and icon_link.get("href"):
                    meta["icon"] = urljoin(url, icon_link["href"])

        # 截断过长描述
        if len(meta["description"]) > 150:
            meta["description"] = meta["description"][:147] + "..."

    except Exception as e:
        print(f"  抓取失败 {url}: {e}")

    return meta


def main():
    files = find_external_links()
    print(f"找到 {len(files)} 个外链文件")

    for path in files:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        fm, body = parse_front_matter(content)
        url = fm.get("externalUrl", "")
        if not url:
            continue

        rel = os.path.relpath(path, CONTENT_DIR)
        print(f"\n处理: {rel} -> {url}")

        meta = fetch_site_meta(url)

        # 更新 front matter（保留手动设置的 title）
        if meta["description"]:
            fm["description"] = meta["description"]
            print(f"  描述: {meta['description'][:60]}...")
        if meta["icon"]:
            fm["icon"] = meta["icon"]
            print(f"  图标: {meta['icon'][:80]}")

        write_front_matter(path, fm, body)
        print(f"  已更新")

    print(f"\n完成，共处理 {len(files)} 个文件")


if __name__ == "__main__":
    main()
