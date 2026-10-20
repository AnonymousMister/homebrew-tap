cask "zync-sh" do
  version "2.35.1"
  sha256 "301d660581c82b69c5c9090f75dc3cfb8a8a7b2e841a76beeb615f0300dc3f02"

  url "https://github.com/zync-sh/zync/releases/download/v#{version}/zync_#{version}_aarch64.dmg"
  name "Zync"
  desc "Modern SSH workspace for developers & DevOps with SFTP, tunneling, and terminal"
  homepage "https://github.com/zync-sh/zync"

  auto_updates true
  depends_on arch: :arm64

  app "zync.app"

  postflight_steps do
    run "/usr/bin/xattr",
        args:         ["-cr", "{{appdir}}/zync.app"],
        must_succeed: false
  end

  zap trash: [
    "~/Library/Application Support/in.thesudoer.zync",
    "~/Library/Caches/in.thesudoer.zync",
    "~/Library/Preferences/in.thesudoer.zync.plist",
    "~/Library/Saved Application State/in.thesudoer.zync.savedState",
    "~/Library/WebKit/in.thesudoer.zync",
  ]
end
