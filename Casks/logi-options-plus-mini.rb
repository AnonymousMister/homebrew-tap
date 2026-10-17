cask "logi-options-plus-mini" do
  version "2.1.0,21"
  sha256 "05f64b00f823e74d79bc9598c12de3c8441e727a09f74ad2d441bab344d73d7c"

  url "https://github.com/Qetesh/logi-options-plus-mini/releases/download/v#{version.csv.first}/Logi.Options+.mini-#{version.csv.first}-#{version.csv.second}.dmg"
  name "Logi Options+ mini"
  desc "Customized lightweight installer and manager for Logitech Options+"
  homepage "https://github.com/Qetesh/logi-options-plus-mini"

  auto_updates true
  depends_on macos: :sonoma

  app "Logi Options+ mini.app"

  zap trash: [
    "~/Library/Application Support/Logi Options+ mini",
    "~/Library/Caches/Logi Options+ mini",
    "~/Library/Preferences/com.qetesh.logi-options-plus-mini.plist",
  ]
end
