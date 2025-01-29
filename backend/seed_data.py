from app import app, db
from app.models.models import VimCommand

# 各レベルのVimコマンドデータ
vim_commands = [
    # レベル1: 基本的なカーソル移動
    {
        'commands': [
            {'command': 'h', 'description': '左に移動', 'category': 'カーソル移動'},
            {'command': 'j', 'description': '下に移動', 'category': 'カーソル移動'},
            {'command': 'k', 'description': '上に移動', 'category': 'カーソル移動'},
            {'command': 'l', 'description': '右に移動', 'category': 'カーソル移動'},
        ],
        'level': 1
    },
    # レベル2: 単語単位の移動
    {
        'commands': [
            {'command': 'w', 'description': '次の単語の先頭に移動', 'category': '単語移動'},
            {'command': 'b', 'description': '前の単語の先頭に移動', 'category': '単語移動'},
            {'command': 'e', 'description': '単語の末尾に移動', 'category': '単語移動'},
        ],
        'level': 2
    },
    # レベル3: 行内移動
    {
        'commands': [
            {'command': '0', 'description': '行の先頭に移動', 'category': '行内移動'},
            {'command': '$', 'description': '行の末尾に移動', 'category': '行内移動'},
            {'command': '^', 'description': '行の最初の非空白文字に移動', 'category': '行内移動'},
        ],
        'level': 3
    },
    # レベル4: 画面内移動
    {
        'commands': [
            {'command': 'H', 'description': '画面の一番上に移動', 'category': '画面移動'},
            {'command': 'M', 'description': '画面の中央に移動', 'category': '画面移動'},
            {'command': 'L', 'description': '画面の一番下に移動', 'category': '画面移動'},
        ],
        'level': 4
    },
    # レベル5: 検索と置換
    {
        'commands': [
            {'command': '/', 'description': '前方検索', 'category': '検索'},
            {'command': '?', 'description': '後方検索', 'category': '検索'},
            {'command': 'n', 'description': '次の検索結果へ', 'category': '検索'},
            {'command': 'N', 'description': '前の検索結果へ', 'category': '検索'},
        ],
        'level': 5
    },
    # レベル6: 編集コマンド
    {
        'commands': [
            {'command': 'i', 'description': 'カーソル位置から挿入モード', 'category': '編集'},
            {'command': 'a', 'description': 'カーソルの後ろから挿入モード', 'category': '編集'},
            {'command': 'o', 'description': '下に新しい行を作成して挿入モード', 'category': '編集'},
            {'command': 'O', 'description': '上に新しい行を作成して挿入モード', 'category': '編集'},
        ],
        'level': 6
    },
    # レベル7: 削除コマンド
    {
        'commands': [
            {'command': 'x', 'description': 'カーソル位置の文字を削除', 'category': '削除'},
            {'command': 'dd', 'description': '行を削除', 'category': '削除'},
            {'command': 'dw', 'description': '単語を削除', 'category': '削除'},
        ],
        'level': 7
    },
    # レベル8: コピーと貼り付け
    {
        'commands': [
            {'command': 'yy', 'description': '行をコピー', 'category': 'コピー'},
            {'command': 'yw', 'description': '単語をコピー', 'category': 'コピー'},
            {'command': 'p', 'description': 'カーソルの後にペースト', 'category': 'ペースト'},
            {'command': 'P', 'description': 'カーソルの前にペースト', 'category': 'ペースト'},
        ],
        'level': 8
    },
    # レベル9: 高度な移動
    {
        'commands': [
            {'command': 'gg', 'description': 'ファイルの先頭に移動', 'category': 'ファイル移動'},
            {'command': 'G', 'description': 'ファイルの末尾に移動', 'category': 'ファイル移動'},
            {'command': '%', 'description': '対応する括弧に移動', 'category': '特殊移動'},
        ],
        'level': 9
    },
    # レベル10: マクロと高度な編集
    {
        'commands': [
            {'command': 'qa', 'description': 'マクロの記録開始', 'category': 'マクロ'},
            {'command': 'q', 'description': 'マクロの記録終了', 'category': 'マクロ'},
            {'command': '@a', 'description': 'マクロの実行', 'category': 'マクロ'},
            {'command': '.', 'description': '直前の編集を繰り返す', 'category': '編集'},
        ],
        'level': 10
    },
]

def seed_database():
    with app.app_context():
        # 既存のデータをクリア
        VimCommand.query.delete()
        
        # 新しいデータを追加
        for level_data in vim_commands:
            for cmd in level_data['commands']:
                command = VimCommand(
                    command=cmd['command'],
                    description=cmd['description'],
                    category=cmd['category'],
                    difficulty_level=level_data['level']
                )
                db.session.add(command)
        
        db.session.commit()
        print('データベースの初期化が完了しました')

if __name__ == '__main__':
    seed_database()
