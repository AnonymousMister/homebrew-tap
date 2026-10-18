cask "feiniu-sync" do
  version "0.2.3"
  sha256 "4bca0c5f0d57a0aafd7c20545edf5c1f8b82151e7baf9bb7ff2113deb5605994"

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
