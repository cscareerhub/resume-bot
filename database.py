class Result:
    def __init__(self, is_success=True, data=None):
        self.is_success = is_success
        self.data = data

class Database:
    def __init__(self, db_name, uname="test", pwd="test", host="localhost"):
        self.db_name = db_name

    def start_connection(self):
        return Result(True)

    def end_connection(self):
        return Result(True)

    def add_admin(self, user_id):
        return Result(True)

    def remove_admin(self, user_id):
        return Result(True)

    def is_admin(self, user_id):
        return Result(True)

    def push_resume(self, user_id, resume):
        return Result(True)
    
    def pop_resume(self):
        return Result(True)

    def delete_resume(self, user_id):
        return Result(True)

    def replace_resume(self, user_id, new_resume):
        return Result(True)

    def show_resumes(self, n):
        return Result(True)

