cask "wechat-input" do
  version "3.0.0,670"
  sha256 "51a240e8b3459463034c74cfc94df2412edbf7814b167e1f5fc88439b32f651b"

  url "https://download.weread.qq.com/app/wxkb/mac/#{version.csv.first}/WeType_#{version.csv.first}_#{version.csv.second}.zip"
  name "WeChat Input"
  name "微信输入法"
  desc "Smart text input method developed by WeChat team"
  homepage "https://z.weixin.qq.com/"

  auto_updates true

  input_method "WeType.app"

  postflight do
    # 为微信输入法设置面板在 /Applications 建立快捷访问，方便随时调起配置，无需 sudo
    source_settings = "#{Dir.home}/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app"
    source_settings = "/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app" unless File.exist?(source_settings)
    target_link = "/Applications/微信输入法设置.app"
    if File.exist?(source_settings)
      system_command "/bin/ln", args: ["-sfn", source_settings, target_link]
    end
  end

  uninstall_postflight do
    system_command "/bin/rm", args: ["-f", "/Applications/微信输入法设置.app"]
  end

  zap trash: [
    "~/Library/Application Support/WeType",
    "~/Library/Caches/com.tencent.inputmethod.wetype",
    "~/Library/Caches/WeType",
    "~/Library/HTTPStorages/com.tencent.inputmethod.wetype",
    "~/Library/Preferences/com.tencent.inputmethod.wetype.plist",
  ]
end
