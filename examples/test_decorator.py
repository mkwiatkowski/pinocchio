def test_me_one():
    pass


class TestMeTwo:
    def test_me_three(self):
        pass

    def test_me_four(self):
        pass


class TestMeWithValues:
    def test_me_runlevel_default(self):
        print "Running test_me_runlevel_default"

    def test_me_runlevel_quick(self):
        print "Running test_me_runlevel_quick"

    def test_me_runlevel_express(self):
        print "Running test_me_runlevel_express"

    def test_me_runlevel_extensive(self):
        print "Running test_me_runlevel_extensive"


class TestMultipleAttr:
    def test_one_and_two(self):
        print "Running test_one_and_two"


def fun_test_multiple_attr():
    print "Running fun_test_multiple_attr"
