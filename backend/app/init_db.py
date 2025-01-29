from app import app, db
from app.models.models import User, VimCommand
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from seed_data import seed_database

def init_database():
    with app.app_context():
        # データベースを作成
        db.create_all()
        
        # デフォルトユーザーを作成
        default_user = User(username='player1')
        db.session.add(default_user)
        db.session.commit()
        
        # シードデータを追加
        seed_database()

if __name__ == '__main__':
    init_database()
