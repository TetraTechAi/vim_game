from app.models.models import User, Progress, WeakPoint, VimCommand
from app import db

def test_user_creation(app):
    with app.app_context():
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert len(user.progress) == 0
        assert len(user.weak_points) == 0

def test_progress_creation(app):
    with app.app_context():
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        
        progress = Progress(user_id=user.id, level=1, score=100)
        db.session.add(progress)
        db.session.commit()
        
        assert progress.id is not None
        assert progress.user_id == user.id
        assert progress.level == 1
        assert progress.score == 100

def test_weak_point_creation(app):
    with app.app_context():
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        
        weak_point = WeakPoint(
            user_id=user.id,
            command='dd',
            difficulty_level=3,
            mistake_count=5
        )
        db.session.add(weak_point)
        db.session.commit()
        
        assert weak_point.id is not None
        assert weak_point.user_id == user.id
        assert weak_point.command == 'dd'
        assert weak_point.difficulty_level == 3
        assert weak_point.mistake_count == 5

def test_vim_command_creation(app):
    with app.app_context():
        command = VimCommand(
            command='dd',
            description='行を削除',
            difficulty_level=3,
            category='削除'
        )
        db.session.add(command)
        db.session.commit()
        
        assert command.id is not None
        assert command.command == 'dd'
        assert command.description == '行を削除'
        assert command.difficulty_level == 3
        assert command.category == '削除'
