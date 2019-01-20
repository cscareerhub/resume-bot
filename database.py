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
            user_id = peewee.IntegerField(primary_key=True)
            resume = peewee.TextField()
            id = peewee.AutoField()

        self.Resume = Resume

    def start_connection(self):
        self.db.connect()
        self.db.create_tables([self.Resume])
        self.db.commit()

    def end_connection(self):
        self.db.close()

    def push_resume(self, user_id, resume):
        try:
            q = self.Resume(user_id=user_id, resume=resume)
            n_rows_modified = q.save()
            return Result(is_success=n_rows_modified == 1)
        except peewee.IntegrityError:
            self.db.rollback()
            return Result(is_success=False)
    
    def pop_resume(self):
        try:
            r = self.Resume.select(self.Resume.user_id, self.Resume.resume).order_by(self.Resume.id).get()
            user_id = r.user_id
            resume = r.resume
            r.delete_instance()
            return Result(is_success=True, data=(user_id, resume))
        except peewee.DoesNotExist:
            return Result(is_success=False)

    def delete_resume(self, user_id):
        r = self.Resume.get_or_none(self.Resume.user_id == user_id)
        if r is None:
            return Result(is_success=False)
        resume = r.resume
        r.delete_instance()
        return Result(is_success=True, data=(user_id, resume))

    def replace_resume(self, user_id, new_resume):
        q = self.Resume.update({self.Resume.resume: new_resume}).where(self.Resume.user_id == user_id)
        n_rows_modified = q.execute()
        return Result(is_success=n_rows_modified == 1)

    def show_resumes(self, n):
        count = 0
        resumes = []
        rows = self.Resume.select(self.Resume.user_id, self.Resume.resume).order_by(self.Resume.id).tuples()
        for row in rows:
            if count >= n:
                break
            resumes.append(row)
            count += 1
        return Result(is_success=True, data=resumes)

