from flask_migrate import Migrate, MigrateCommand
from app import create_app,db
from flask_script import Manager,Server
from app.models import Writer

# Creating app instance
app = create_app('production')
# app = create_app('development')

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)
manager.add_command('run',Server(use_debugger=True))

@manager.command
def test():
    import unittest
    tests =unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def make_shell_context():
    return dict(app=app,db=db,Writer=Writer)

if __name__ == '__main__':
    manager.run()