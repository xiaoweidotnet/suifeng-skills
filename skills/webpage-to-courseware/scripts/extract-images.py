#!/usr/bin/env python3
"""
从 HTML 字符串中提取所有图片 URL
用法：echo "<html>..." | python3 extract-images.py [基础URL]
或   python3 extract-images.py [基础URL] < page.html

输出：每行一个图片 URL（已转为绝对路径）
过滤掉：图标/logo小图（通常 < 20px）、base64 内联图、追踪像素
"""

import sys
import re
from urllib.parse import urljoin, urlparse

# 需要过滤掉的无意义图片关键词
SKIP_KEYWORDS = [
    "tracking", "pixel", "beacon", "analytics", "spacer",
    "blank", "transparent", "1x1", "favicon", ".ico",
    "avatar-placeholder", "spinner", "loading",
]

# 最小有意义图片尺寸（URL 中若明确包含极小尺寸则跳过）
TINY_SIZE_RE = re.compile(r"[/_-](\d+)x(\d+)[._]")


def is_meaningful(url: str) -> bool:
    """判断图片 URL 是否值得下载"""
    url_lower = url.lower()
    # 跳过 base64 内联
    if url_lower.startswith("data:"):
        return False
    # 跳过追踪/装饰用图
    for kw in SKIP_KEYWORDS:
        if kw in url_lower:
            return False
    # 跳过明显的 1px 追踪图（URL 中含 1x1 尺寸）
    m = TINY_SIZE_RE.search(url)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        if w <= 4 and h <= 4:
            return False
    return True


def extract_image_urls(html: str, base_url: str = "") -> list:
    urls = []
    seen = set()

    # 匹配 <img src="..."> 和 srcset
    img_src_re = re.compile(
        r'<img[^>]+src=["\']([^"\'>\s]+)["\']', re.IGNORECASE
    )
    srcset_re = re.compile(
        r'<img[^>]+srcset=["\']([^"\']+)["\']', re.IGNORECASE
    )
    # 匹配 CSS background-image: url(...)
    bg_re = re.compile(
        r'background(?:-image)?\s*:\s*url\(["\']?([^"\')\s]+)["\']?\)',
        re.IGNORECASE
    )
    # Open Graph / Twitter card 图片
    og_re = re.compile(
        r'<meta[^>]+(?:og:image|twitter:image)[^>]+content=["\']([^"\']+)["\']',
        re.IGNORECASE
    )

    def add(raw_url):
        url = raw_url.strip()
        if not url:
            return
        if base_url:
            url = urljoin(base_url, url)
        if url not in seen and is_meaningful(url):
            seen.add(url)
            urls.append(url)

    for m in img_src_re.finditer(html):
        add(m.group(1))

    for m in srcset_re.finditer(html):
        # srcset 格式: "url1 1x, url2 2x" 或 "url1 100w, url2 200w"
        for part in m.group(1).split(","):
            candidate = part.strip().split()[0]
            add(candidate)

    for m in bg_re.finditer(html):
        add(m.group(1))

    for m in og_re.finditer(html):
        add(m.group(1))

    return urls


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else ""
    html = sys.stdin.read()
    urls = extract_image_urls(html, base_url)
    for url in urls:
        print(url)
    print(f"# 共提取到 {len(urls)} 张图片 URL", file=sys.stderr)


if __name__ == "__main__":
    main()
