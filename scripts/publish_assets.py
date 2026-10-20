#!/usr/bin/env python3
"""
发布 Release 资产到 GitHub Releases，并按 tag_prefix 清理该软件的历史旧版本 Releases 与 Tags
"""

import os
import sys
import json
import re
import subprocess

def publish_assets(manifest_path):
    if not os.path.exists(manifest_path):
        print(f"Manifest {manifest_path} 不存在，跳过。")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        assets = json.load(f)

    for item in assets:
        tag = item["tag"]
        file_path = item["file"]
        tag_prefix = item.get("tag_prefix")
        title = item.get("title", tag)
        notes = item.get("notes", "自动托管下载资产")

        print(f"\n📦 正在发布最新资产 {file_path} 到 Tag {tag}...")

        # 1. 创建或更新当前最新 Release
        res = subprocess.run(["gh", "release", "view", tag], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  Release {tag} 已存在，更新资产 (--clobber)...")
            subprocess.run(["gh", "release", "upload", tag, file_path, "--clobber"], check=True)
        else:
            print(f"  创建新 Release {tag}...")
            subprocess.run(["gh", "release", "create", tag, file_path, "--title", title, "--notes", notes], check=True)

        # 2. 清理属于该分类 (tag_prefix) 的历史旧 Release 与 Tag，确保每类软件仅保留最新版本
        if tag_prefix:
            list_res = subprocess.run(["gh", "release", "list", "--limit", "100", "--json", "tagName"], capture_output=True, text=True)
            if list_res.returncode == 0:
                try:
                    releases = json.loads(list_res.stdout)
                    for rel in releases:
                        old_tag = rel.get("tagName")
                        if not old_tag or old_tag == tag:
                            continue

                        # 判断是否属于当前软件类别，避免误删其它软件的 Release
                        should_delete = False
                        if tag_prefix == "v":
                            # 飞牛同步旧 tag 格式为 v0.x.x
                            if re.match(r"^v\d+\.", old_tag):
                                should_delete = True
                        elif old_tag.startswith(tag_prefix):
                            should_delete = True

                        if should_delete:
                            print(f"  🗑️ 清理旧版本 Release 与 Tag: {old_tag}")
                            subprocess.run(["gh", "release", "delete", old_tag, "--yes", "--cleanup-tag"], check=False)
                except Exception as e:
                    print(f"  清理旧 Release 出错 (跳过): {e}")

if __name__ == "__main__":
    manifest = sys.argv[1] if len(sys.argv) > 1 else "/tmp/release_assets.json"
    publish_assets(manifest)
