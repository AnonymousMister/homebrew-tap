cask "x1a0he-wechat-plugin" do
  version "2.13.1"
  sha256 "172db4b6e2edee2a04c148fcdebc21533fc5e18b23669c4ad1dfd60c6b935e7a"

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
