cask "xiaoheiribao" do
  version "1.8.6"
  sha256 "6e3f3c321e74376db0c792405e3a4bd37a325e788f3963f513a50d2378feb20a"

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
