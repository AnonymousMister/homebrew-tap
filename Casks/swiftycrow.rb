cask "swiftycrow" do
  version "2.10.1"
  sha256 "d0193cc0c08923ed065eba92d2397c374bf2d918668d38a8ea89729c3a2a329e"

  url "https://github.com/PangMo5/SwiftyCrow/releases/download/v#{version}/SwiftyCrow-#{version}.dmg"
  name "SwiftyCrow"
  desc "Fully on-device screen translator powered by Apple Vision and Translation"
  homepage "https://github.com/PangMo5/SwiftyCrow"

  depends_on macos: :sonoma

  app "SwiftyCrow.app"

  zap trash: [
    "~/.config/SwiftyCrow",
    "~/Library/Application Support/SwiftyCrow",
    "~/Library/Caches/dev.PangMo5.SwiftyCrow",
    "~/Library/HTTPStorages/dev.PangMo5.SwiftyCrow",
    "~/Library/Preferences/dev.PangMo5.SwiftyCrow.plist",
  ]
end
