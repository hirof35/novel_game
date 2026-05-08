Python Novel Game Engine (Gemini Edition)このプロジェクトは、PythonとPygameを使用したシンプルかつ拡張性の高いノベルゲームエンジンです。シナリオを外部のJSONファイルで管理するため、プログラミングの知識が少なくても自分だけのノベルゲームを作成できます。📁 ファイル構成main.py: ゲーム本体（プログラム実行ファイル）scenario.json: シナリオデータ（会話内容や分岐の設定）config.json: システム設定（音量など、初回起動時に自動生成）save.json: セーブデータ（必要に応じて実装可能）🚀 使い方Pythonのインストール: Python 3.xがインストールされていることを確認してください。ライブラリのインストール:Bashpip install pygame
ゲームの起動:Bashpython main.py
📝 シナリオの書き方 (scenario.json)シナリオはリスト形式で記述します。各要素（シーン）には以下のプロパティを設定できます。キー説明text画面に表示されるメッセージ本文。showキャラクターを表示するかどうか (true / false)。bg背景色を [R, G, B] 形式で指定（任意）。options選択肢。text（表示文字）, love（好感度変化）, next（次へ進むインデックス）を含む。resultそのシーンを終えた後の遷移先 ("CLEAR" または "GAMEOVER")。記述例：JSON{
    "text": "どちらの道に進みますか？",
    "options": [
        {"text": "右の道（安全）", "love": 0, "next": 5},
        {"text": "左の道（危険）", "love": 5, "next": 8}
    ]
}
🎮 操作方法マウス左クリック: メッセージの進行 / 選択肢の決定。スペースキー: タイトル画面でのスタート / クリア・オーバー画面からのリスタート。ESCキー: プレイ中のコンフィグ画面（設定）の開閉。🛠 カスタマイズのヒント画像の使用: 現在はキャラクターを楕円（ellipse）で描画しています。Characterクラスのdrawメソッドを、pygame.image.loadを使用した画像描画（blit）に書き換えることで、イラストを表示できます。フォント: 日本語が表示されない場合は、pygame.font.SysFontにインストール済みの日本語フォント名（"MS Gothic"など）を指定するか、.ttfファイルを直接読み込んでください。📜 ライセンスこのコードは自由に改変・配布可能です。学習や創作活動にぜひお役立てください！
<img width="995" height="780" alt="スクリーンショット 2026-05-08 092025" src="https://github.com/user-attachments/assets/36018dd4-f23e-4e18-9eb9-58c7368ed56e" />
