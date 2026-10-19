cask "x1a0he-wechat-plugin" do
  version "2.12.1"
  sha256 "82fbcc22f0bfffd6fde050e94cb9bcbed00b0602560c4713971014bf972c9e2e"

  url "https://raw.githubusercontent.com/X1a0He/X1a0HeWeChatPlugin/main/X1a0HeWeChatPlugin.pkg"
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
