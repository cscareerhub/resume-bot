import unittest
from database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.Database = Database("testing_db")
        self.db = self.Database.db
        self.Database.start_connection()

    def test_valid_table(self):
        tables = self.db.get_tables()
        self.assertEqual(sorted(tables), ['resume'])
        cols_res = self.db.get_columns('resume')

        self.assertTrue(len(cols_res) == 3)

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

    def tearDown(self):
        self.db.drop_tables([self.Database.Resume], safe=True)
        self.db.close()


if __name__ == '__main__':
    unittest.main()
