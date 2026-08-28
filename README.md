# 福祉業務 要件ヒアリング Skill

福祉事業の業務担当者へ、専門用語を使わず1問ずつ質問し、回答に応じて要件を深掘りする Hermes / Codex 互換Skillです。

## できること

- 「ヒアリングスタート」を合図に開始
- 1メッセージ1問、原則選択肢形式
- 回答済み事項を飛ばし、不足や矛盾に応じて追加質問
- 5問ごとの継続確認と、中断・再開
- 要件定義草案、未解決事項、開発に必要な共有物一覧の作成
- 個人情報、AIによる外部送信、制度・請求判断の確認漏れを防止

## Hermesで使う

```bash
hermes skills install kousoeie-beep/fukushi-requirements-interviewer/skills/fukushi-requirements-interviewer --yes
hermes
```

Hermesを起動したら、次のどちらかを入力します。

```text
/fukushi-requirements-interviewer
```

```text
ヒアリングスタート
```

## Codexで使う

```bash
git clone https://github.com/kousoeie-beep/fukushi-requirements-interviewer.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R fukushi-requirements-interviewer/skills/fukushi-requirements-interviewer "${CODEX_HOME:-$HOME/.codex}/skills/"
```

新しいCodexの会話で、次のどちらかを入力します。

```text
$fukushi-requirements-interviewer
```

```text
ヒアリングスタート
```

## GitHubを使わずに渡す

配布用の `fukushi-requirements-interviewer-skill-v1.0.0.zip` を、メール、Google Drive、Dropbox、AirDrop、USBメモリなどで共有できます。受け取った人はZIPを展開し、そのフォルダで次のいずれかを実行します。

macOS / Linux：

```bash
./install.sh hermes
./install.sh codex
./install.sh both
```

Windows PowerShell：

```powershell
.\install.ps1 -Target hermes
.\install.ps1 -Target codex
.\install.ps1 -Target both
```

既に同名のSkillがある場合、インストーラーは勝手に上書きせず停止します。内容を確認して更新する場合だけ `--force` または `-Force` を付けます。

## 会話の操作

- `ヒアリングスタート`：新しく開始
- `一旦停止` / `今日はここまで`：現在位置を短く整理して停止
- `ヒアリング再開`：回答済みを飛ばして再開
- `ヒアリング終了`：現在の回答で要件定義草案を作成

## 安全な資料共有

実在する利用者・児童・保護者・職員の個人情報は貼らず、匿名化した見本や架空データを使ってください。パスワード、本人確認コード、秘密鍵は共有しないでください。

## 検証

```bash
python3 skills/fukushi-requirements-interviewer/scripts/audit_skill.py
python3 skills/fukushi-requirements-interviewer/scripts/simulate_interview.py
```

## License

MIT
