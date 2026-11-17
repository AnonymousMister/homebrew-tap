cask "x1a0he-wechat-plugin" do
  version "2.15.1"
  sha256 "74cc4cfc88fe1d99a0c1613744d659451c0196ac25bc1a2db121a8a8d74fc0bf"

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
