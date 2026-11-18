cask "x1a0he-wechat-plugin" do
  version "2.15.3"
  sha256 "469a6b3c63687b5c17d280c79617628b29e894661a681f8dc3f0228d0700a0b9"

  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/x1a0he-wechat-plugin-v#{version}/X1a0HeWeChatPlugin.pkg"
  name "X1a0He WeChat Plugin"
  name "微信防撤回多开插件 (小鹤版)"
  desc "WeChat plugin for macOS featuring message anti-revoke, multi-account and more"
  homepage "https://github.com/X1a0He/X1a0HeWeChatPlugin"

  depends_on arch: :arm64
  depends_on cask: "wechat-universal"

  pkg "X1a0HeWeChatPlugin.pkg"

  uninstall pkgutil: "com.x1a0he.pkg.wechatplugin"
end
