#!/usr/bin/env python3
"""
网页图片批量下载工具
用法：python3 download-images.py <输出目录> <图片URL1> [图片URL2] ...
或   python3 download-images.py <输出目录> --from-file <url列表文件>

输出：每行一个 JSON，格式：{"url": "...", "path": "...", "status": "ok"|"fail", "reason": "..."}
"""

import sys
import os
import json
import hashlib
import urllib.request
import urllib.error
from urllib.parse import urlparse, urljoin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_SIZE_MB = 10


def url_to_filename(url: str, idx: int) -> str:
    """根据 URL 生成本地文件名，保留扩展名"""
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    name, ext = os.path.splitext(basename)
    # 只保留支持的扩展名
    if ext.lower() not in SUPPORTED_EXTS:
        ext = ".jpg"
    # 用 URL 哈希作为前缀防止重名
    short_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    safe_name = f"{idx:02d}_{short_hash}{ext}"
    return safe_name


def download_one(url: str, out_dir: str, idx: int) -> dict:
    filename = url_to_filename(url, idx)
    out_path = os.path.join(out_dir, filename)

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            # 跳过非图片响应
            if content_type and not content_type.startswith("image/"):
                return {"url": url, "path": None, "status": "skip",
                        "reason": f"content-type: {content_type}"}

            data = resp.read(MAX_SIZE_MB * 1024 * 1024 + 1)
            if len(data) > MAX_SIZE_MB * 1024 * 1024:
                return {"url": url, "path": None, "status": "skip",
                        "reason": f"超过 {MAX_SIZE_MB}MB 大小限制"}

            with open(out_path, "wb") as f:
                f.write(data)

        return {"url": url, "path": out_path, "status": "ok", "reason": ""}

    except urllib.error.HTTPError as e:
        return {"url": url, "path": None, "status": "fail",
                "reason": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"url": url, "path": None, "status": "fail",
                "reason": str(e.reason)}
    except Exception as e:
        return {"url": url, "path": None, "status": "fail",
                "reason": str(e)}


def main():
    if len(sys.argv) < 2:
        print("用法: python3 download-images.py <输出目录> <URL1> [URL2] ...", file=sys.stderr)
        sys.exit(1)

    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)

    # 收集 URL
    urls = []
    if "--from-file" in sys.argv:
        file_idx = sys.argv.index("--from-file") + 1
        if file_idx < len(sys.argv):
            with open(sys.argv[file_idx]) as f:
                urls = [line.strip() for line in f if line.strip()]
    else:
        urls = sys.argv[2:]

    if not urls:
        print(json.dumps({"error": "没有提供任何图片 URL"}))
        sys.exit(0)

    results = []
    for idx, url in enumerate(urls):
        result = download_one(url, out_dir, idx)
        results.append(result)
        # 逐行输出，方便调用方实时读取
        print(json.dumps(result, ensure_ascii=False), flush=True)

    # 输出摘要到 stderr
    ok = sum(1 for r in results if r["status"] == "ok")
    fail = sum(1 for r in results if r["status"] == "fail")
    skip = sum(1 for r in results if r["status"] == "skip")
    print(f"\n✅ 成功: {ok}  ❌ 失败: {fail}  ⏭️ 跳过: {skip}", file=sys.stderr)


if __name__ == "__main__":
    main()
