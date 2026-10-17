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
| **微信防撤回插件 (小鹤版)** | `x1a0he-wechat-plugin` | `brew install --cask x1a0he-wechat-plugin` | 自动监听 X1a0He 官方 Release 与 PKG 哈希 |
| **微信 Mac 官网原版 (插件锁版)** | `wechat-universal` | `brew install --cask wechat-universal` | **与插件严格版本绑定**，避免因微信误升级导致插件失效 |
| **小黑日报助手** | `xiaoheiribao` | `brew install --cask xiaoheiribao` | 每日自动请求官网 API 提取最新版本与计算哈希 |
| **Loon for Mac** | `loon` | `brew install --cask loon` | 官方 releases 跟踪 |

> **💡 微信输入法说明**：
> 微信输入法（微信键盘，官网 [z.weixin.qq.com](https://z.weixin.qq.com/)）已被 Homebrew 官方收录，可直接运行：
> ```bash
> brew install --cask wetype
> ```

---

## 🤖 自动化运维机制

- 仓库内包含 [`.github/workflows/autoupdate.yml`](.github/workflows/autoupdate.yml)；
- 每日凌晨 04:00 (UTC 20:00) 自动触发 Python 脚本巡检上游官方源；
- 检测到新版本时，自动下载计算 SHA256 校验和并提交更新；
- 本机日常只需执行 `brew upgrade`，即可享受到这些软件的无感全自动升级。
