cask "xiaoheiribao" do
  version "1.8.1"
  sha256 "e8bd19fd03a2b93724a5086765f3584a2cc9281671367c87d0c6423abc3b5db9"

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
