cask "xiaoheiribao" do
  version "1.8.0"
  sha256 "f7815f115c1f9564435e76b9a8e35918598d807971cb1bd92ef7e967f94b0186"

  url "https://github.com/shjiyue/xiaoheiribao/releases/download/v#{version}/XiaoheiDailyAssistant-#{version}-mac-arm64.dmg.zip"
  name "XiaoHei Daily Assistant"
  name "小黑日报助手"
  desc "AI work memory and review assistant"
  homepage "https://www.xiaoheiribao.com/"

  depends_on arch: :arm64

  app "小黑日报助手.app"

  zap trash: [
    "~/Library/Application Support/xiaoheiribao",
    "~/Library/Preferences/com.shjiyue.xiaohei.plist",
    "~/Library/Saved Application State/com.shjiyue.xiaohei.savedState",
  ]
end
