# slack_export
(2022/08/08)
メッセージ出力用の関数が３つ入ってます。python3です。
private channelやdmなど、slackの管理画面からexportできないデータの保存ができます。
しばらくreadmeを作る余力がないので、もし解読できそうでしたらどうぞ。

- *channel_list()*: ユーザーから見れるチャンネル（DM含む）のリスト(名前とid)を./channel_list.txtに出力します。
- *get_message()*:./channel_list.txtに記載のあるチャンネルのメッセージをcsvとjsonで全部出力します。ただし、jsonは、マージの仕方がよくわかってないのでテキトーにprintさせています。"#json出力"のコメントアウトのある行を削除するとcsv onlyになります（そこそこ時間かかりそうです。オープンなチャンネルは、普通にexportしたほうがいいかも）
- *file_download()*: channel_list.txtに記載のあるチャンネルのファイルを全部ダウンロードします
