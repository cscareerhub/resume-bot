import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.Database = Database("testing_db")
        self.db = self.Database.db
        self.Database.start_connection()

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertEqual(sorted(tables), ['resume', 'users'])
        cols_res = self.db.get_columns('resume')
        cols_res2 = self.db.get_columns('users')

        self.assertTrue(len(cols_res) == 3)
        self.assertTrue(len(cols_res2) == 3)

    def test_push_resume(self):
        resume = "imgur.com/iamaresume"

        self.assertTrue(self.Database.push_resume("Nik", resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 1)
        self.assertEqual(self.Database.Resume.get(self.Database.Resume.id == 1).resume, resume)
        self.assertEqual(self.Database.Resume.get(self.Database.Resume.id == 1).user_id, "Nik")

        self.assertTrue(self.Database.push_resume("Gopher", resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 2)

        self.assertFalse(self.Database.push_resume("Gopher", resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 2)

        # Testing this post integrity error
        self.assertTrue(self.Database.push_resume("iNirvana", resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 3)

    def test_pop_resume(self):
        first_resume = "imgur.com/iamaresume"
        second_resume = "imgur.com/iamalsoaresume"

        self.assertTrue(self.Database.push_resume("Nik", first_resume).is_success)
        self.assertTrue(self.Database.push_resume("Gopher", second_resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 2)

        result1 = self.Database.pop_resume()
        self.assertEqual(self.Database.Resume.select().count(), 1)
        result2 = self.Database.pop_resume()
        self.assertEqual(self.Database.Resume.select().count(), 0)

        self.assertTrue(result1.is_success)
        self.assertTrue(result2.is_success)

        self.assertEqual(result1.data, ("Nik", first_resume))
        self.assertEqual(result2.data, ("Gopher", second_resume))

    def test_delete_resume(self):
        resume = "imgur.com/iamaresume"

        self.assertTrue(self.Database.push_resume("Nik", resume).is_success)
        self.assertTrue(self.Database.push_resume("Gopher", resume).is_success)
        self.assertTrue(self.Database.push_resume("iNirvana", resume).is_success)
        self.assertEqual(self.Database.Resume.select().count(), 3)

        self.assertTrue(self.Database.delete_resume("Gopher").is_success)
        self.assertEqual(self.Database.Resume.select().count(), 2)

        self.assertFalse(self.Database.delete_resume("Gopher").is_success)
        self.assertEqual(self.Database.Resume.select().count(), 2)

    def test_user_insert(self):
        # given
        user1 = "001"
        user2 = "002"

        # when
        n1 = self.Database.insert_user(user1)
        n2 = self.Database.insert_user(user2)
        n3 = self.Database.insert_user(user1)

        # then
        self.assertTrue(n1.is_success)
        self.assertTrue(n2.is_success)
        self.assertFalse(n3.is_success)

    def test_user_update(self):
        # given
        user1 = "001"
        user2 = "002"
        self.Database.insert_user(user1)
        self.Database.insert_user(user2)

        # when
        r1 = self.Database.update_user(user1)
        r2 = self.Database.update_user(user1)
        r3 = self.Database.update_user(user2)

        # then
        self.assertEqual(r1.data, 1)
        self.assertEqual(r2.data, 2)
        self.assertEqual(r3.data, 1)
        
    def test_user_contains(self):
        # given
        user1 = "001"
        self.Database.insert_user(user1)

        # when
        b = self.Database.check_user_present(user1)

        # then
        self.assertTrue(b)

    def test_user_removal(self):
        # given
        user1 = "001"
        user2 = "002"
        user3 = "003"
        self.Database.insert_user(user1)
        self.Database.insert_user(user2)

        # when
        b1 = self.Database.remove_user(user1)
        b3 = self.Database.remove_user(user3)

        # then
        self.assertTrue(b1)
        self.assertFalse(b3)
        self.assertTrue(self.Database.check_user_present(user2))

    def tearDown(self):
        self.db.drop_tables([self.Database.Resume, self.Database.Users], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
