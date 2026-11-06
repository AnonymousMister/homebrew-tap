cask "xiaoheiribao" do
  version "1.8.2"
  sha256 "af5ff9afd2538587ac60ba1e2b529259aeee1b0630e5a420cd79d59abbb097a2"

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
