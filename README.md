# slack_export

- slackワークスペースの過去ログとアップロードされたファイルを出力します。
- フリープランのslackでは、コードの実行者が見ることのできる範囲のデータを出力できます（DMやプライベートチャンネルも出力可）。
- python3です。外部モジュールは"requests", "dictknife"を使っています。
- Tokenの発行にappを作成する必要があります。フリープランの場合はappを10個までしかワークスペースに導入できないため、実行後は削除しましょう。

## 使い方
### Tokenの発行
1. <https://api.slack.com/apps?new_app=1> で"Create New App"をクリック。
2. From Scratchを選択。
3. app名を入力（適当でok）, データをエクスポートしたいワークスペースを選択し、"Create App"をクリック。
4. メニューから、"OAuth & Permissions" を選択。
5. ページ下方の"Scopes"内、"User Token Scopes"に以下のスコープを追加。

(必須)
- users:read
- channels:read
- groups:read
- im:read
- mpim:read

(ログ出力時は必要)
- channels:history
- groups:history
- im:history
- mpim:history

(ファイル出力時は必要)
- files:read

6. ページ上方の"OAuth Tokens for Your Workspace" 内、"Install to Workspace" をクリック
7. "Accept"をクリック
7. 自動遷移先のページに"User OAuth Token"が表示されるので、手元に保存する。

### pythonファイルの実行
1. slack_export.py を実行。
2. Workspace名を入力(保存フォルダの名前になります)。
3. Tokenの入力が求められるので、先ほど保存したTokenを入力。
4. "l","m","f"の入力が求められるので、最初は"l"を入力。Tokenを発行した人から見ることができる範囲の全channel(private channelやDM含む)の名前とIDがchannel_list.txtに出力される。
5. channel_list.txtを開きログやファイルをエクスポートしたいものだけ残し、他は削除する。（最下行のEOFは残してください。）
6. 次にターミナルで"m"を入力するとchannel_list.txtに記載のあるchannelのメッセージがjsonとcsvの形式で出力される。slack_export.py内の"#json出力"のコメントアウトがある行を削除するとcsvだけが出力される。
7. "f"を入力するとchannel_list.txtに記載のあるchannelにアップロードされたファイルがすべてエクスポートされる。

### appの削除
1. <https://api.slack.com/apps>から、作成したappを選択
2. ページ下部の"Delete App"から削除

### 更新履歴
2022/08/20: csvにファイル名も出力

2022/08/15: workspaceの入力を追加

2022/08/08:作成
