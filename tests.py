try:
    from Project.News_Capsule.main import app
    import unittest

except Exception as e:
    print("Some Modules are Missing{}".format(e))


class FlaskTest(unittest.TestCase):
    # Check if Response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content returned is text/html
    def test_index_2(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"text/html; charset=utf-8")

    # check homepage data
    def test_index_3(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b"Welcome to Tech Capsule" in response.data)

    #checking sign in page
    def test_index_4(self):
        tester = app.test_client(self)
        response = tester.get("/sign-in")
        self.assertTrue(b"Login" in response.data)

     #checking create account page
    def test_index_5(self):
        tester = app.test_client(self)
        response = tester.get("/register?")
        self.assertTrue(b"CREATE AN ACCOUNT" in response.data)


    # Checking preference data page
    def test_index_6(self):
        tester = app.test_client(self)
        response = tester.get("/news-preferences")
        self.assertTrue(b"Crypto" in response.data)


if __name__ == "__main__":
    unittest.main()