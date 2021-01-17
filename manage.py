from flask_script import Manager

from api.app import create_app

manager = Manager(create_app)
manager.add_option('--config', '-c', required=True)

if __name__ == '__main__':
    manager.run()
