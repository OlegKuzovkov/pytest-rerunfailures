import py, pytest


class TestFunctionality(object):

    pass_the_third_time = """
                import os
                filename = "test.res"
                state = None
                try:
                    fileh = open(filename, 'r')
                    state = fileh.read()
                    fileh.close()
                except IOError:
                    state = ''

                if state == '':
                    fileh = open(filename, 'w')
                    fileh.write('fail')
                    fileh.flush()
                    raise Exception("Failing the first time")
                elif state == 'fail':
                    fileh = open(filename, 'w')
                    fileh.write('pass')
                    fileh.flush()
                    raise Exception("Failing the second time")
                elif state == 'pass':
                    os.popen('rm -f %s' % filename)  # delete the file
                    return  # pass the method
                else:
                    raise Exception("unexpected data in file %s: %s" % (filename, state))
    """

    passing_test = """
            import pytest
            @pytest.mark.nondestructive
            def test_fake_pass():
                assert True
        """

    failing_test = """
            import pytest
            @pytest.mark.nondestructive
            def test_fake_fail():
                raise Exception("OMG! failing test!")
        """

    flakey_test = """
            import pytest
            @pytest.mark.nondestructive
            def test_flaky_test():
    """ + pass_the_third_time

    flakey_setup_conftest = """
        import py, pytest
        def pytest_runtest_setup(item):
        """ + pass_the_third_time

    failing_setup_conftest = """
            import py, pytest
            def pytest_runtest_setup(item):
                raise Exception("OMG! setup failure!")
        """

    flakey_teardown_conftest = """
        import py, pytest
        def pytest_runtest_teardown(item):
        """ + pass_the_third_time

    failing_teardown_conftest = """
        import py, pytest
        def pytest_runtest_teardown(item):
            raise Exception("OMG! teardown failure!")
        """

    # passing tests
    def test_can_pass_with_reruns_enabled(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)

        reprec = testdir.inline_run('--reruns=2', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1

    def test_can_pass_with_reruns_disabled(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)

        reprec = testdir.inline_run(test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1

    # setup
    def test_fails_with_flakey_setup_if_rerun_not_used(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_setup_conftest)

        reprec = testdir.inline_run(test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the first time'

    def test_fails_with_flakey_setup_if_rerun_only_once(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_setup_conftest)

        reprec = testdir.inline_run('--reruns=1', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the second time'

    def test_passes_with_flakey_setup_if_run_two_times(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_setup_conftest)

        reprec = testdir.inline_run('--reruns=2', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1

    def test_fails_with_failing_setup_even_if_rerun_three_times(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.failing_setup_conftest)

        reprec = testdir.inline_run('--reruns=3', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: OMG! setup failure!'

    # the test itself
    def test_flaky_test_fails_if_rerun_not_used(self, testdir):
        test_file = testdir.makepyfile(self.flakey_test)

        reprec = testdir.inline_run(test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the first time'

    def test_flaky_test_fails_if_run_only_once(self, testdir):
        test_file = testdir.makepyfile(self.flakey_test)

        reprec = testdir.inline_run('--reruns=1', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the second time'

    def test_flakey_test_passes_if_run_two_times(self, testdir):
        test_file = testdir.makepyfile(self.flakey_test)

        reprec = testdir.inline_run('--reruns=2', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1

    def test_failing_test_fails_if_rerun_three_times(self, testdir):
        test_file = testdir.makepyfile(self.failing_test)

        reprec = testdir.inline_run('--reruns=3', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: OMG! failing test!'

    # teardown
    def test_fails_with_flakey_teardown_if_rerun_not_used(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_teardown_conftest)

        reprec = testdir.inline_run(test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the first time'

    def test_fails_with_flakey_teardown_if_rerun_only_once(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_teardown_conftest)

        reprec = testdir.inline_run('--reruns=1', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(failed) == 1
        out = failed[0].longrepr.reprcrash.message
        assert out == 'Exception: Failing the first time'

    def test_passes_with_flakey_teardown_if_rerun_two_times(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.flakey_teardown_conftest)

        reprec = testdir.inline_run('--reruns=2', test_file)
        passed, skipped, failed = reprec.listoutcomes()
        assert len(passed) == 1

    def test_fails_with_failing_teardown_if_rerun_three_times(self, testdir):
        test_file = testdir.makepyfile(self.passing_test)
        conftest_file = testdir.makeconftest(self.failing_teardown_conftest)

        reprec = testdir.inline_run('--reruns=3', test_file)
        passed, skipped, failed = reprec.listoutcomes()

        # strange outocmes for failures in teardown
        assert len(failed) == 1
        assert len(passed) == 1