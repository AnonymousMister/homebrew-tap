#!/usr/bin/env python3
"""
自动检查并更新 Homebrew Tap 中的 Cask 版本与校验和
支持：
- x1a0he-wechat-plugin (微信插件)
- wechat-universal (与插件严格锁定的官网 Universal 微信)
- xiaoheiribao (小黑日报助手)
- logi-options-plus-mini (精简版 Logi Options+)
"""

import os
import re
import sys
import json
import hashlib
import urllib.request
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASKS_DIR = os.path.join(ROOT_DIR, "Casks")

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")

def compute_sha256(url):
    print(f"  [下载并计算 SHA256] {url}")
    req = urllib.request.Request(url, headers=HEADERS)
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp:
        while chunk := resp.read(65536):
            h.update(chunk)
    return h.hexdigest()

def update_wechat_and_plugin(updated_list):
    print(">> 检查微信与 X1a0He 插件状态...")
    readme_url = "https://raw.githubusercontent.com/X1a0He/X1a0HeWeChatPlugin/main/README.md"
    try:
        content = fetch_url(readme_url)
    except Exception as e:
        print(f"  读取插件 README 失败: {e}")
        return

    # 1. 提取插件自身版本与 SHA256
    plugin_ver_match = re.search(r"release-v([\d\.]+)-brightgreen", content)
    plugin_sha_match = re.search(r"安装包 pkg SHA 256:\s*([a-f0-9]{64})", content)
    
    if plugin_ver_match and plugin_sha_match:
        plugin_ver = plugin_ver_match.group(1).strip()
        plugin_sha = plugin_sha_match.group(1).strip()
        plugin_cask = os.path.join(CASKS_DIR, "x1a0he-wechat-plugin.rb")
        
        with open(plugin_cask, "r") as f:
            cask_content = f.read()
        
        old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
        if old_ver != plugin_ver:
            print(f"  发现微信插件新版本: {old_ver} -> {plugin_ver}")
            cask_content = re.sub(r'version "[^"]+"', f'version "{plugin_ver}"', cask_content, count=1)
            cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{plugin_sha}"', cask_content, count=1)
            with open(plugin_cask, "w") as f:
                f.write(cask_content)
            updated_list.append(f"x1a0he-wechat-plugin {plugin_ver}")
        else:
            print(f"  微信插件已是最新版 ({plugin_ver})。")

    # 2. 提取配套的 Universal 微信版本与 SHA256
    # 格式: | 4.1.15.72 | 270152 |  ✅  | 2.12.0 / 2.12.1 | [立即下载](https://dldir1v6.qq.com/weixin/Universal/Mac/xWeChatMac_universal_4.1.15.72_270152.dmg) |
    wechat_match = re.search(r"\|\s*([\d\.]+)\s*\|\s*(\d+)\s*\|\s*✅.*?dldir1v6\.qq\.com", content)
    wechat_sha_match = re.search(r"SHA256:\s*([a-f0-9]{64})", content)
    
    if wechat_match and wechat_sha_match:
        wc_ver = wechat_match.group(1).strip()
        wc_build = wechat_match.group(2).strip()
        wc_full_ver = f"{wc_ver},{wc_build}"
        wc_sha = wechat_sha_match.group(1).strip()
        
        wechat_cask = os.path.join(CASKS_DIR, "wechat-universal.rb")
        with open(wechat_cask, "r") as f:
            cask_content = f.read()
            
        old_wc_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
        if old_wc_ver != wc_full_ver:
            print(f"  发现插件配套微信新版本: {old_wc_ver} -> {wc_full_ver}")
            cask_content = re.sub(r'version "[^"]+"', f'version "{wc_full_ver}"', cask_content, count=1)
            cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{wc_sha}"', cask_content, count=1)
            with open(wechat_cask, "w") as f:
                f.write(cask_content)
            updated_list.append(f"wechat-universal {wc_full_ver}")
        else:
            print(f"  配套微信已是最新版 ({wc_full_ver})。")

def update_xiaoheiribao(updated_list):
    print(">> 检查小黑日报助手状态...")
    api_url = "https://xiaoheiribao.com/api/check-update.php?version=0.0.0&platform=mac&arch=arm64"
    try:
        data = json.loads(fetch_url(api_url))
    except Exception as e:
        print(f"  请求小黑日报 API 失败: {e}")
        return

    if not data.get("ok") or not data.get("data"):
        return

    latest_ver = data["data"]["latestVersion"]
    cask_path = os.path.join(CASKS_DIR, "xiaoheiribao.rb")
    with open(cask_path, "r") as f:
        cask_content = f.read()

    old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
    if old_ver != latest_ver:
        print(f"  发现小黑日报助手新版本: {old_ver} -> {latest_ver}")
        dl_url = data["data"]["downloadUrl"]
        # 优先使用 GitHub Release 链接
        gh_url = f"https://github.com/shjiyue/xiaoheiribao/releases/download/v{latest_ver}/XiaoheiDailyAssistant-{latest_ver}-mac-arm64.dmg.zip"
        try:
            sha = compute_sha256(gh_url)
        except Exception:
            sha = compute_sha256(dl_url)
            
        cask_content = re.sub(r'version "[^"]+"', f'version "{latest_ver}"', cask_content, count=1)
        cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{sha}"', cask_content, count=1)
        with open(cask_path, "w") as f:
            f.write(cask_content)
        updated_list.append(f"xiaoheiribao {latest_ver}")
    else:
        print(f"  小黑日报助手已是最新版 ({latest_ver})。")

def update_logi_options_plus_mini(updated_list):
    print(">> 检查 Logi Options+ mini 状态...")
    appcast_url = "https://raw.githubusercontent.com/Qetesh/logi-options-plus-mini/main/appcast.xml"
    try:
        content = fetch_url(appcast_url)
        root = ET.fromstring(content)
        channel = root.find("channel")
        first_item = channel.find("item")
        short_ver = first_item.find("{http://www.andymatuschak.org/xml-namespaces/sparkle}shortVersionString").text.strip()
        build_ver = first_item.find("{http://www.andymatuschak.org/xml-namespaces/sparkle}version").text.strip()
        dmg_url = first_item.find("enclosure").attrib["url"].strip()
    except Exception as e:
        print(f"  解析 appcast.xml 失败: {e}")
        return

    full_ver = f"{short_ver},{build_ver}"
    cask_path = os.path.join(CASKS_DIR, "logi-options-plus-mini.rb")
    with open(cask_path, "r") as f:
        cask_content = f.read()

    old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
    if old_ver != full_ver:
        print(f"  发现 Logi Options+ mini 新版本: {old_ver} -> {full_ver}")
        sha = compute_sha256(dmg_url)
        cask_content = re.sub(r'version "[^"]+"', f'version "{full_ver}"', cask_content, count=1)
        cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{sha}"', cask_content, count=1)
        with open(cask_path, "w") as f:
            f.write(cask_content)
        updated_list.append(f"logi-options-plus-mini {full_ver}")
    else:
        print(f"  Logi Options+ mini 已是最新版 ({full_ver})。")

def main():
    updated = []
    update_wechat_and_plugin(updated)
    update_xiaoheiribao(updated)
    update_logi_options_plus_mini(updated)
    
    if updated:
        msg = "auto: 更新 " + ", ".join(updated)
        print(f"\n🎉 更新完成: {msg}")
        # 输出给 GitHub Actions 的环境变量
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("has_update=true\n")
                f.write(f"commit_msg={msg}\n")
    else:
        print("\n✨ 所有 Cask 均已是最新状态，无需更新。")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("has_update=false\n")

if __name__ == "__main__":
    main()
