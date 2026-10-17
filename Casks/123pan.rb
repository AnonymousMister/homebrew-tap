cask "123pan" do
  version "3.2.6"
  sha256 "c9aa6169e071395e6dd85690673aea76cd44b892121fafa3284b20ef2803811e"

  url "https://app.123pan.com/pc-pro/darwin/arm64/#{version.no_dots}/123pan-#{version}-arm64.dmg"
  name "123 Cloud Disk"
  name "123云盘"
  desc "Cloud storage and file sharing client"
  homepage "https://www.123pan.com/"

  depends_on arch: :arm64

  app "123云盘.app"

  zap trash: [
    "~/Library/Application Support/123云盘",
    "~/Library/Preferences/com.mac123.mfy.plist",
    "~/Library/Saved Application State/com.mac123.mfy.savedState",
  ]
end
