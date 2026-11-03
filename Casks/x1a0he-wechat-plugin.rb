cask "x1a0he-wechat-plugin" do
  version "2.13.0"
  sha256 "0a4188bdc006a4b8f307209b518abbba95fa12dbcf1f7c882227617da3ec1df8"

  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/x1a0he-wechat-plugin-v#{version}/X1a0HeWeChatPlugin.pkg"
  name "X1a0He WeChat Plugin"
  name "微信防撤回多开插件 (小鹤版)"
  desc "WeChat plugin for macOS featuring message anti-revoke, multi-account and more"
  homepage "https://github.com/X1a0He/X1a0HeWeChatPlugin"

  depends_on arch: :arm64
  depends_on cask: "wechat-universal"

  pkg "X1a0HeWeChatPlugin.pkg"

  postflight_steps do
    run "/usr/bin/xattr",
        args: ["-rd", "com.apple.quarantine", "/Applications/WeChat.app"],
        sudo: true
    run "/usr/bin/codesign",
        args: ["--force", "--deep", "--sign", "-", "/Applications/WeChat.app"],
        sudo: true
  end

  uninstall pkgutil: "com.x1a0he.pkg.wechatplugin"
end
