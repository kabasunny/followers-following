# followers-following


# .envファイルに以下を設定
GITHUB_API_TOKEN=あなたのトークン（https://github.com/settings/tokens から取得）
BASE_URL=https://api.github.com
GITHUB_USER=自身のユーザー名


準備に以下を行います (☝´◑д◐｀)☝

## uvのインストール

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## uvを使った実行方法

```bash
# Pythonのインストール（uvが自動で管理）
uv python install 3.12

# 依存関係のインストール
uv sync

# 実行
uv run python followers_following.py
```


## 従来の方法（pip）

あらかじめ、pythonをインストールしておきます。

```bash
pip install requests python-dotenv
python followers_following.py
```

# May all people, including myself, see each other as friends. May the world be liberated from vested interests, money, and laws.

# このアイディアは、日本の年賀状を見ていて思いました。そうだ郵便局がすべての年賀状を仮想的にやり取りしたことにすれば、だれも年賀状を見なくても済むと