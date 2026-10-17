cask "feiniu-sync" do
  version "0.2.3"
  sha256 "e77ff71a1f11bf43086a0bf81c8f87cb11d278b8bae9b6b50af8553d04bfcc06"

  url "https://github.com/AnonymousMister/homebrew-tap/releases/download/v#{version}/fn-sync_#{version}_aarch64.dmg"
  name "FeiNiu Sync"
  name "飞牛同步"
  desc "Client for fnOS NAS file synchronization"
  homepage "https://www.fnnas.com/"

  depends_on arch: :arm64

  app "飞牛同步.app"

  zap trash: [
    "~/Library/Application Support/com.fn-sync-client.app",
    "~/Library/Preferences/com.fn-sync-client.app.plist",
    "~/Library/Saved Application State/com.fn-sync-client.app.savedState",
  ]
end
