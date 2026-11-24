cask "zync-sh" do
  version "2.41.2"
  sha256 "075fc22a785ae15efeab1d6fb2ee22fd9c1191bcb7bb44ea990dffb643cb461d"

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
