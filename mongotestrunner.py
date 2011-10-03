from django.test.simple import DjangoTestSuiteRunner
from django.test import TransactionTestCase

from settings import MONGO_DB
from settings import DUMP_DIR

_running_test = False
from subprocess import call

class TestRunner(DjangoTestSuiteRunner):
    def setup_databases(self, **kwangs):
        global _running_test
        _running_test = True
        
        print 'Creating test-database: ' + MONGO_DB
        print 'restoring default data'
        call(["mongo/mongorestore", "--db", MONGO_DB, DUMP_DIR])
        return MONGO_DB
    
    def teardown_databases(self, db_name, **kwargs):
        from pymongo import Connection
        conn = Connection()
        conn.drop_database(db_name)
        print 'Dropping test-database: ' + db_name


class TestCase(TransactionTestCase):
    def _fixture_setup(self):
        pass