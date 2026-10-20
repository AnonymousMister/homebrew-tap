# AnonymousMister's Homebrew Tap

个人专属维护的 Homebrew 软件源，收录常用个性化、内测或独立 macOS 应用程序，并通过 **GitHub Actions 全自动巡检与更新**。

---

## 📦 如何使用

在 macOS 终端中添加此 Tap：

```bash
brew tap AnonymousMister/tap
```

---

## 🚀 收录软件列表

| 软件名称 | Cask 标识符 | 安装命令 | 自动更新说明 |
| :--- | :--- | :--- | :--- |
| **微信输入法** | `wechat-input` | `brew install --cask wechat-input` | 自动监听官网 API 元数据，并在 `/Applications` 建立设置面板快捷入口 |
| **微信防撤回插件 (小鹤版)** | `x1a0he-wechat-plugin` | `brew install --cask x1a0he-wechat-plugin` | 自动转存官方 PKG 至 GitHub Release 缓存，防止上游静默覆写，内置去隔离与防损坏签名 |
| **微信 Mac 官网原版 (插件锁版)** | `wechat-universal` | `brew install --cask wechat-universal` | **与插件严格版本绑定**，转存官网原版 DMG 至 Release 托管，防止官方原包失效 |
| **飞牛同步** | `feiniu-sync` | `brew install --cask feiniu-sync` | 自动请求官网防盗链鉴权签名并托管至 Release 直链，全自动巡检发布 |
| **小黑日报助手** | `xiaoheiribao` | `brew install --cask xiaoheiribao` | 每日自动请求官网 API 提取最新版本与计算哈希 |
| **Logi Options+ mini** | `logi-options-plus-mini` | `brew install --cask logi-options-plus-mini` | 追踪 Sparkle 官方 Appcast 自动更新精简版 |
| **123云盘** | `123pan` | `brew install --cask 123pan` | 官方原生 ARM64 桌面端直链 |
| **Zync** | `zync` | `brew install --cask zync` | 现代 SSH 工作区与终端工具（SFTP、隧道管理），每日监听 GitHub Release 自动巡检 |

---

## 🤖 自动化运维机制

- 仓库内包含 [`.github/workflows/autoupdate.yml`](.github/workflows/autoupdate.yml)；
- 每日凌晨 04:00 (UTC 20:00) 自动触发 Python 脚本巡检上游官方源；
- 检测到新版本时，自动下载计算 SHA256 校验和并提交更新；
- 本机日常只需执行 `brew upgrade`，即可享受到这些软件的无感全自动升级。
