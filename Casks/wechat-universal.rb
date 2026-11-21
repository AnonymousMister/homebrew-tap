cask "wechat-universal" do
  version "4.2.1.4,270596"
  sha256 "0b00aa99fb098344815b9e2e22b67ddae88b8e61219c79e50904b6d7fa61e69d"

  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/wechat-universal-v#{version.csv.first}_#{version.csv.second}/xWeChatMac_universal_#{version.csv.first}_#{version.csv.second}.dmg"
  name "WeChat Universal (Plugin Supported)"
  name "微信 Mac 官网原版 (插件适配版)"
  desc "Official WeChat for Mac, version-locked for X1a0HeWeChatPlugin compatibility"
  homepage "https://mac.weixin.qq.com/"

  auto_updates false
  conflicts_with cask: "wechat"
  depends_on arch: :arm64

  app "WeChat.app"

  zap trash: [
    "~/Library/Application Scripts/com.tencent.xinWeChat",
    "~/Library/Caches/com.tencent.xinWeChat",
    "~/Library/Containers/com.tencent.xinWeChat",
    "~/Library/Preferences/com.tencent.xinWeChat.plist",
    "~/Library/Saved Application State/com.tencent.xinWeChat.savedState",
  ]
end
