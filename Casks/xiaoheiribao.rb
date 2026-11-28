cask "xiaoheiribao" do
  version "1.8.7"
  sha256 "c7fcef6271fe86b2dd871c961f2e24302fb8ba1d6e2b9b676d5336b6b40c9c5a"

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
