cask "zync-sh" do
  version "2.39.0"
  sha256 "054fd94d02548a5f6d442fd4a8cb719eaad5371aee889bd23dd3eca06616519c"

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
