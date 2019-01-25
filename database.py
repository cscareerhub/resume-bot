import peewee


class Result:
    def __init__(self, is_success=True, data=None):
        self.is_success = is_success
        self.data = data


class Database:
    def __init__(self, db_name, uname="test", pwd="test", host="localhost"):
        self.db = peewee.PostgresqlDatabase(
            db_name,
            user=uname,
            password=pwd,
            host=host
        )

        # This is taken mostly from the Peewee sample app
        class BaseModel(peewee.Model):
            class Meta:
                database = self.db

        class Resume(BaseModel):
            user_id = peewee.TextField(unique=True)
            resume = peewee.TextField()
            id = peewee.AutoField()

        class Users(BaseModel):
            user_id = peewee.TextField(unique=True)
            post_count = peewee.IntegerField(null=False)

        self.Resume = Resume
        self.Users = Users

    def start_connection(self):
        self.db.connect()
        self.db.create_tables([self.Resume, self.Users])
        self.db.commit()

    def end_connection(self):
        self.db.close()

    # Resume stuff
    def push_resume(self, user_id, resume):
        try:
            resume_model = self.Resume(user_id=user_id, resume=resume)
            nb_rows_modified = resume_model.save()
            return Result(is_success=nb_rows_modified == 1)
        except peewee.IntegrityError:
            self.db.rollback()
            return Result(is_success=False)

    def pop_resume(self):
        resume_model = self.Resume.select().order_by(self.Resume.id.asc()).first()
        if resume_model is None:
            return Result(is_success=False)
        return self.delete_resume(resume_model.user_id)

    def delete_resume(self, user_id):
        resume_model = self.Resume.get_or_none(self.Resume.user_id == user_id)
        if resume_model is None:
            return Result(is_success=False)
        resume = resume_model.resume
        resume_model.delete_instance()
        return Result(is_success=True, data=(user_id, resume))

    def replace_resume(self, user_id, new_resume):
        update_query = self.Resume.update({self.Resume.resume: new_resume}).where(self.Resume.user_id == user_id)
        nb_rows_modified = update_query.execute()
        return Result(is_success=nb_rows_modified == 1)

    def show_resumes(self, nb_resumes=None):
        resumes = self.Resume.select(self.Resume.user_id, self.Resume.resume).order_by(self.Resume.id).limit(
            nb_resumes).tuples()
        return Result(is_success=True, data=resumes)

    # Users Stuff
    def update_user(self, user_id):
        query = self.Users.insert(user_id=user_id, post_count=0).on_conflict(
            conflict_target=[self.Users.user_id],
            update={self.Users.post_count: self.Users.post_count + 1})

        print(query.sql())
        query.execute()

        return self.Users.get(self.Users.user_id == user_id).post_count

    def remove_user(self, user_id):
        user = self.Users.get_or_none(self.Users.user_id == user_id)

        if user is None:
            return False

        user.delete_instance()
        return True

    def check_user_present(self, user_id):
        return self.Users.get_or_none(self.Users.user_id == user_id) is not None
