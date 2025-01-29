from app import db
from app.models.models import VimCommand

def init_commands():
    """初期コマンドをデータベースに追加"""
    commands = [
        # レベル1：基本的な移動
        {'command': 'h', 'description': '左に移動', 'difficulty_level': 1, 'category': 'movement'},
        {'command': 'j', 'description': '下に移動', 'difficulty_level': 1, 'category': 'movement'},
        {'command': 'k', 'description': '上に移動', 'difficulty_level': 1, 'category': 'movement'},
        {'command': 'l', 'description': '右に移動', 'difficulty_level': 1, 'category': 'movement'},
        {'command': 'w', 'description': '次の単語の先頭に移動', 'difficulty_level': 1, 'category': 'movement'},
        {'command': 'b', 'description': '前の単語の先頭に移動', 'difficulty_level': 1, 'category': 'movement'},
        
        # レベル2：基本的な編集
        {'command': 'i', 'description': 'カーソル位置から入力モードを開始', 'difficulty_level': 2, 'category': 'insert'},
        {'command': 'a', 'description': 'カーソルの次の位置から入力モードを開始', 'difficulty_level': 2, 'category': 'insert'},
        {'command': 'o', 'description': '下に新しい行を追加して入力モードを開始', 'difficulty_level': 2, 'category': 'insert'},
        {'command': 'O', 'description': '上に新しい行を追加して入力モードを開始', 'difficulty_level': 2, 'category': 'insert'},
        {'command': 'x', 'description': 'カーソル位置の文字を削除', 'difficulty_level': 2, 'category': 'delete'},
        {'command': 'dd', 'description': '現在の行を削除', 'difficulty_level': 2, 'category': 'delete'},
        
        # レベル3：高度な移動
        {'command': '0', 'description': '行の先頭に移動', 'difficulty_level': 3, 'category': 'movement'},
        {'command': '$', 'description': '行の末尾に移動', 'difficulty_level': 3, 'category': 'movement'},
        {'command': 'gg', 'description': 'ファイルの先頭に移動', 'difficulty_level': 3, 'category': 'movement'},
        {'command': 'G', 'description': 'ファイルの末尾に移動', 'difficulty_level': 3, 'category': 'movement'},
        {'command': 'f{char}', 'description': '行内の次の{char}に移動', 'difficulty_level': 3, 'category': 'movement'},
        {'command': 'F{char}', 'description': '行内の前の{char}に移動', 'difficulty_level': 3, 'category': 'movement'},
        
        # レベル4：高度な編集
        {'command': 'yy', 'description': '現在の行をコピー', 'difficulty_level': 4, 'category': 'yank'},
        {'command': 'p', 'description': 'カーソルの後にペースト', 'difficulty_level': 4, 'category': 'paste'},
        {'command': 'P', 'description': 'カーソルの前にペースト', 'difficulty_level': 4, 'category': 'paste'},
        {'command': 'u', 'description': '直前の操作を取り消し', 'difficulty_level': 4, 'category': 'undo'},
        {'command': 'Ctrl+r', 'description': '取り消した操作をやり直し', 'difficulty_level': 4, 'category': 'redo'},
        {'command': '.', 'description': '直前の操作を繰り返し', 'difficulty_level': 4, 'category': 'repeat'},
    ]
    
    # 既存のコマンドを削除
    VimCommand.query.delete()
    
    # 新しいコマンドを追加
    for cmd in commands:
        command = VimCommand(
            command=cmd['command'],
            description=cmd['description'],
            difficulty_level=cmd['difficulty_level'],
            category=cmd['category']
        )
        db.session.add(command)
    
    db.session.commit()
