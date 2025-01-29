import json
from app.models.models import User, VimCommand
from app import db

def test_register_user(client):
    response = client.post('/api/user/register', 
                         json={'username': 'testuser'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert data['username'] == 'testuser'

def test_get_commands(client, app):
    with app.app_context():
        # テストデータを作成
        command = VimCommand(
            command='dd',
            description='行を削除',
            difficulty_level=1,
            category='削除'
        )
        db.session.add(command)
        db.session.commit()
        
        response = client.get('/api/game/commands/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['command'] == 'dd'
        assert data[0]['description'] == '行を削除'

def test_save_progress(client, app):
    with app.app_context():
        # ユーザーを作成
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        
        response = client.post('/api/game/progress',
                             json={
                                 'user_id': user.id,
                                 'level': 1,
                                 'score': 100
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == '進捗が保存されました'

def test_generate_question(client, app):
    with app.app_context():
        # ユーザーとコマンドを作成
        user = User(username='testuser')
        db.session.add(user)
        
        command = VimCommand(
            command='dd',
            description='行を削除',
            difficulty_level=1,
            category='削除'
        )
        db.session.add(command)
        db.session.commit()
        
        response = client.get(f'/api/game/generate-question/{user.id}/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'command' in data
        assert 'difficulty_level' in data
