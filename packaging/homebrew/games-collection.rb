class GamesCollection < Formula
  include Language::Python::Virtualenv

  desc "Command-line collection of classic board, card, and puzzle games"
  homepage "https://github.com/saint2706/Games"
  url "https://github.com/saint2706/Games/releases/download/v2.0.1/games_collection-2.0.1-py3-none-any.whl"
  sha256 "bb28340274d2b9a6eb7a895ac4883bcb7c8649fc6cdb401851e9550411918db9"
  license "MIT"
  version "2.0.1"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "games-collection", shell_output("#{bin}/games-collection --help")
  end
end
