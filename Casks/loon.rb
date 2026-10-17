cask "loon" do
  version "0.4.0,81"
  sha256 :no_check

  url "https://raw.githubusercontent.com/Loon0x00/Loon4Mac/main/Loon.dmg"
  name "Loon for Mac"
  desc "Network tool and proxy client for macOS"
  homepage "https://github.com/Loon0x00/Loon4Mac"

  depends_on macos: :monterey

  app "Loon.app"

  zap trash: [
    "~/Library/Application Support/Loon",
    "~/Library/Preferences/com.loon.Loon.plist",
    "~/Library/Saved Application State/com.loon.Loon.savedState",
  ]
end
