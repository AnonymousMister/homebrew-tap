#!/usr/bin/env python3
"""
自动检查并更新 Homebrew Tap 中的 Cask 版本与校验和
支持：
- x1a0he-wechat-plugin (微信插件)
- wechat-universal (与插件严格锁定的官网 Universal 微信)
- xiaoheiribao (小黑日报助手)
- logi-options-plus-mini (精简版 Logi Options+)
- wechat-input (微信输入法)
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

def download_file_and_hash(url, dest_path, timeout=300):
    print(f"  [正在下载并计算 SHA256] {url}")
    h = hashlib.sha256()
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest_path, "wb") as out_f:
        while chunk := resp.read(65536):
            h.update(chunk)
            out_f.write(chunk)
    sha = h.hexdigest()
    print(f"  下载完成: {dest_path} (SHA256: {sha})")
    return sha

def compute_sha256(url):
    print(f"  [下载并计算 SHA256] {url}")
    req = urllib.request.Request(url, headers=HEADERS)
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp:
        while chunk := resp.read(65536):
            h.update(chunk)
    return h.hexdigest()

def update_wechat_and_plugin(updated_list, release_assets):
    print(">> 检查微信与 X1a0He 插件状态...")
    readme_url = "https://raw.githubusercontent.com/X1a0He/X1a0HeWeChatPlugin/main/README.md"
    try:
        content = fetch_url(readme_url)
    except Exception as e:
        print(f"  读取插件 README 失败: {e}")
        return

    # 1. 检查并缓存微信插件 (x1a0he-wechat-plugin)
    plugin_ver_match = re.search(r"release-v([\d\.]+)-brightgreen", content)
    plugin_sha_match = re.search(r"安装包 pkg SHA 256:\s*([a-f0-9]{64})", content)
    
    if plugin_ver_match and plugin_sha_match:
        plugin_ver = plugin_ver_match.group(1).strip()
        plugin_cask = os.path.join(CASKS_DIR, "x1a0he-wechat-plugin.rb")
        
        with open(plugin_cask, "r") as f:
            cask_content = f.read()
        
        old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
        gh_plugin_tag = f"x1a0he-wechat-plugin-v{plugin_ver}"
        gh_plugin_url = f"https://github.com/AnonymousMister/homebrew-tap/releases/download/{gh_plugin_tag}/X1a0HeWeChatPlugin.pkg"
        has_plugin_asset = check_asset_exists(gh_plugin_url)
        needs_plugin_update = (old_ver != plugin_ver) or (not has_plugin_asset) or ("releases/download" not in cask_content)

        if needs_plugin_update:
            if old_ver != plugin_ver:
                print(f"  发现微信插件新版本: {old_ver} -> {plugin_ver}")
            else:
                print(f"  微信插件 Release 资产缺失或未切换直链，准备下载转存: v{plugin_ver}")

            raw_pkg_url = "https://raw.githubusercontent.com/X1a0He/X1a0HeWeChatPlugin/main/X1a0HeWeChatPlugin.pkg"
            tmp_pkg = "/tmp/X1a0HeWeChatPlugin.pkg"
            sha = download_file_and_hash(raw_pkg_url, tmp_pkg)

            new_cask = re.sub(r'version "[^"]+"', f'version "{plugin_ver}"', cask_content, count=1)
            new_cask = re.sub(r'sha256 "[^"]+"', f'sha256 "{sha}"', new_cask, count=1)
            new_url_line = '  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/x1a0he-wechat-plugin-v#{version}/X1a0HeWeChatPlugin.pkg"'
            new_cask = re.sub(r'  url "[^"]+"', new_url_line, new_cask, count=1)

            if new_cask != cask_content:
                with open(plugin_cask, "w") as f:
                    f.write(new_cask)
                updated_list.append(f"x1a0he-wechat-plugin {plugin_ver}")

            release_assets.append({
                "tag": gh_plugin_tag,
                "tag_prefix": "x1a0he-wechat-plugin-",
                "file": tmp_pkg,
                "title": f"x1a0he-wechat-plugin-v{plugin_ver}",
                "notes": f"X1a0He 微信防撤回多开插件官方安装包 v{plugin_ver}"
            })
        else:
            print(f"  微信插件已是最新版 ({plugin_ver}) 且 Release 资产已就绪。")

    # 2. 检查并缓存 Universal 微信原版 (wechat-universal)
    # 格式: | 4.1.15.72 | 270152 |  ✅  | 2.12.0 / 2.12.1 | [立即下载](https://dldir1v6.qq.com/weixin/Universal/Mac/xWeChatMac_universal_4.1.15.72_270152.dmg) |
    wechat_match = re.search(r"\|\s*([\d\.]+)\s*\|\s*(\d+)\s*\|\s*✅.*?dldir1v6\.qq\.com", content)
    if wechat_match:
        wc_ver = wechat_match.group(1).strip()
        wc_build = wechat_match.group(2).strip()
        wc_full_ver = f"{wc_ver},{wc_build}"
        
        wechat_cask = os.path.join(CASKS_DIR, "wechat-universal.rb")
        with open(wechat_cask, "r") as f:
            cask_content = f.read()
            
        old_wc_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
        gh_wc_tag = f"wechat-universal-v{wc_ver}_{wc_build}"
        gh_wc_file = f"xWeChatMac_universal_{wc_ver}_{wc_build}.dmg"
        gh_wc_url = f"https://github.com/AnonymousMister/homebrew-tap/releases/download/{gh_wc_tag}/{gh_wc_file}"
        has_wc_asset = check_asset_exists(gh_wc_url)
        needs_wc_update = (old_wc_ver != wc_full_ver) or (not has_wc_asset) or ("releases/download" not in cask_content)

        if needs_wc_update:
            if old_wc_ver != wc_full_ver:
                print(f"  发现插件配套微信新版本: {old_wc_ver} -> {wc_full_ver}")
            else:
                print(f"  配套微信 Release 资产缺失或未切换直链，准备下载转存: {wc_full_ver}")

            raw_wc_url = f"https://dldir1v6.qq.com/weixin/Universal/Mac/xWeChatMac_universal_{wc_ver}_{wc_build}.dmg"
            tmp_dmg = f"/tmp/{gh_wc_file}"
            wc_sha = download_file_and_hash(raw_wc_url, tmp_dmg, timeout=600)

            new_cask = re.sub(r'version "[^"]+"', f'version "{wc_full_ver}"', cask_content, count=1)
            new_cask = re.sub(r'sha256 "[^"]+"', f'sha256 "{wc_sha}"', new_cask, count=1)
            new_url_line = '  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/wechat-universal-v#{version.csv.first}_#{version.csv.second}/xWeChatMac_universal_#{version.csv.first}_#{version.csv.second}.dmg"'
            new_cask = re.sub(r'  url "[^"]+"', new_url_line, new_cask, count=1)

            if new_cask != cask_content:
                with open(wechat_cask, "w") as f:
                    f.write(new_cask)
                updated_list.append(f"wechat-universal {wc_full_ver}")

            release_assets.append({
                "tag": gh_wc_tag,
                "tag_prefix": "wechat-universal-",
                "file": tmp_dmg,
                "title": f"wechat-universal-v{wc_ver}_{wc_build}",
                "notes": f"官方微信 Universal 原版安装包（适配插件锁版）v{wc_ver}_{wc_build}"
            })
        else:
            print(f"  配套微信已是最新版 ({wc_full_ver}) 且 Release 资产已就绪。")

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

def update_wechat_input(updated_list):
    print(">> 检查微信输入法状态...")
    portal_url = "https://z.weixin.qq.com/"
    try:
        html = fetch_url(portal_url)
    except Exception as e:
        print(f"  获取微信输入法官网失败: {e}")
        return

    matches = re.findall(r'https?://download\.weread\.qq\.com/app/wxkb/mac/([\d\.]+)/install_info_([\d\.]+)_(\d+)\.json', html)
    if not matches:
        print("  未能在页面中匹配到微信输入法正式版元数据链接")
        return

    ver_dir, ver, build = matches[0]
    full_ver = f"{ver},{build}"
    json_url = f"https://download.weread.qq.com/app/wxkb/mac/{ver_dir}/install_info_{ver}_{build}.json"

    cask_path = os.path.join(CASKS_DIR, "wechat-input.rb")
    with open(cask_path, "r") as f:
        cask_content = f.read()

    old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)
    if old_ver != full_ver:
        print(f"  发现微信输入法新版本: {old_ver} -> {full_ver}")
        try:
            j_content = fetch_url(json_url)
            j_data = json.loads(j_content)
            zip_url = j_data.get("zip_download_url")
        except Exception as e:
            print(f"  获取 install_info.json 失败: {e}")
            return

        if not zip_url:
            zip_url = f"https://download.weread.qq.com/app/wxkb/mac/{ver}/WeType_{ver}_{build}.zip"

        sha = compute_sha256(zip_url)
        cask_content = re.sub(r'version "[^"]+"', f'version "{full_ver}"', cask_content, count=1)
        cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{sha}"', cask_content, count=1)
        with open(cask_path, "w") as f:
            f.write(cask_content)
        updated_list.append(f"wechat-input {full_ver}")
    else:
        print(f"  微信输入法已是最新版 ({full_ver})。")

def check_asset_exists(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        req.get_method = lambda: "HEAD"
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False

def update_feiniu_sync(updated_list, release_assets):
    print(">> 检查飞牛同步状态...")
    download_page = "https://www.fnnas.com/download"
    try:
        html = fetch_url(download_page)
    except Exception as e:
        print(f"  获取飞牛下载页面失败: {e}")
        return

    m = re.search(r"https?://[^\"\\]*?fn-sync_([\d\.]+)_aarch64\.dmg", html)
    if not m:
        print("  未能在页面中匹配到飞牛同步 ARM64 下载链接")
        return

    latest_ver = m.group(1).strip()
    raw_mac_url = m.group(0).strip()

    cask_path = os.path.join(CASKS_DIR, "feiniu-sync.rb")
    with open(cask_path, "r") as f:
        cask_content = f.read()

    old_ver = re.search(r'version "([^"]+)"', cask_content).group(1)

    gh_release_url = f"https://github.com/AnonymousMister/homebrew-tap/releases/download/v{latest_ver}/fn-sync_{latest_ver}_aarch64.dmg"
    has_asset = check_asset_exists(gh_release_url)

    needs_update = (old_ver != latest_ver) or (not has_asset)

    if not needs_update:
        print(f"  飞牛同步已是最新版 ({latest_ver}) 且 Release 资产已就绪，跳过。")
        return

    if old_ver != latest_ver:
        print(f"  发现飞牛同步新版本: {old_ver} -> {latest_ver}")
    else:
        print(f"  飞牛同步 Release 资产缺失，准备自动下载并托管: v{latest_ver}")

    sign_api = "https://www.fnnas.com/asset/download-sign"
    try:
        sign_req = urllib.request.Request(
            sign_api,
            data=json.dumps({"url": raw_mac_url}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": HEADERS["User-Agent"]}
        )
        with urllib.request.urlopen(sign_req, timeout=30) as resp:
            sign_data = json.loads(resp.read().decode("utf-8"))
            signed_url = sign_data.get("url")
    except Exception as e:
        print(f"  获取防盗链签名失败: {e}")
        return

    if not signed_url:
        print("  未能获取有效的签名下载链接")
        return

    tmp_dmg = f"/tmp/fn-sync_{latest_ver}_aarch64.dmg"
    print(f"  [正在从官网签名直链下载] {signed_url}")
    h = hashlib.sha256()
    dl_req = urllib.request.Request(signed_url, headers=HEADERS)
    with urllib.request.urlopen(dl_req, timeout=180) as resp, open(tmp_dmg, "wb") as out_f:
        while chunk := resp.read(65536):
            h.update(chunk)
            out_f.write(chunk)

    sha = h.hexdigest()
    print(f"  下载完成，SHA256: {sha}")

    new_cask_content = re.sub(r'version "[^"]+"', f'version "{latest_ver}"', cask_content, count=1)
    new_cask_content = re.sub(r'sha256 "[^"]+"', f'sha256 "{sha}"', new_cask_content, count=1)
    
    if new_cask_content != cask_content:
        with open(cask_path, "w") as f:
            f.write(new_cask_content)
        updated_list.append(f"feiniu-sync {latest_ver}")

    release_assets.append({
        "tag": f"v{latest_ver}",
        "tag_prefix": "v",
        "file": tmp_dmg,
        "title": f"v{latest_ver}",
        "notes": f"FeiNiu Sync 飞牛同步客户端官方包 v{latest_ver}"
    })

def main():
    updated = []
    release_assets = []
    update_wechat_and_plugin(updated, release_assets)
    update_xiaoheiribao(updated)
    update_logi_options_plus_mini(updated)
    update_wechat_input(updated)
    update_feiniu_sync(updated, release_assets)

    if release_assets:
        manifest_path = "/tmp/release_assets.json"
        with open(manifest_path, "w") as f:
            json.dump(release_assets, f, indent=2)
        print(f"\n📦 已准备 {len(release_assets)} 个 Release 待发布资产。")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("has_release_asset=true\n")
                f.write(f"release_manifest={manifest_path}\n")
    else:
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("has_release_asset=false\n")

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
