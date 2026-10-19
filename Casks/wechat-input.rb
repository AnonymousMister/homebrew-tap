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

  postflight_steps do
    # 为微信输入法设置面板在 /Applications 建立快捷访问，方便随时调起配置，无需 sudo
    if_path_exists "~/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app" do
      symlink "~/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app",
              "/Applications/微信输入法设置.app",
              overwrite:           true,
              remove_on_uninstall: true
    end
    if_path_exists "/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app" do
      symlink "/Library/Input Methods/WeType.app/Contents/MacOS/WeTypeSettings.app",
              "/Applications/微信输入法设置.app",
              overwrite:           true,
              remove_on_uninstall: true
    end
  end

  zap trash: [
    "~/Library/Application Support/WeType",
    "~/Library/Caches/com.tencent.inputmethod.wetype",
    "~/Library/Caches/WeType",
    "~/Library/HTTPStorages/com.tencent.inputmethod.wetype",
    "~/Library/Preferences/com.tencent.inputmethod.wetype.plist",
  ]
end
