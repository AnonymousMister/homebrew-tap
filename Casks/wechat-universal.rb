cask "wechat-universal" do
  version "4.1.15.72,270152"
  sha256 "8fc1b6d136754368588ae841330a435f31bda1d84baf2dbf999b0933cdee22fc"

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
