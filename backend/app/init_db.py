from app import create_app, db
from app.models.models import User, VimCommand
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from seed_data import seed_database

def init_database():
    app = create_app()
    with app.app_context():
        # データベースを削除して再作成
        db.drop_all()
        db.create_all()
        
        # デフォルトユーザーを作成
        default_user = User(username='player1')
        db.session.add(default_user)
        db.session.commit()
        
        # シードデータを追加
        seed_database()
        print("データベースの初期化が完了しました")

if __name__ == '__main__':
    init_database()
