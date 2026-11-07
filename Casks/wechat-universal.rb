cask "wechat-universal" do
  version "4.2.0.51,270387"
  sha256 "ede51054941e241ffa0873003d28681b92bc927de371968113eb4f648fd637a2"

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
