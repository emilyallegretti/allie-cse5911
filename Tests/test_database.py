import pytest
import os
from SqliteUtils import Database

# Fixture is used for mounting and dismounting database connection
@pytest.fixture(scope="module")
def db():
    db_path = os.path.join("db", "FromEchoDev240208a_echo_main_db_current.sqlite3")
    test_db = Database(db_path)
    test_db.connect()
    yield test_db
    test_db.close()

# Test for successful database connection
def test_database_connection_success(db):
    assert db.conn is not None, "Database connection should be established."

# Test for database connection failure with an invalid path
def test_database_connection_failure():
    db_path = os.path.join("db", "test.sqlite3")
    db = Database(db_path)
    with pytest.raises(Exception) as excinfo:
        db.connect()
    assert "Database file does not exist" in str(excinfo.value), "Should raise an exception if the database does not exist."

# Test executing a valid query in the database
def test_valid_query_execution(db):
    valid_query = "SELECT * FROM EchoApp_videoactivity" 
    try:
        result = db.run_query(valid_query)
        rows = list(result)
        assert len(rows) >= 1, "Query result should be at least one row."
    except Exception as e:
        pytest.fail(f"Unexpected exception for a valid query: {e}")

# Test executing an invalid query for error handling
def test_invalid_query_error(db):
    invalid_query = "SELECT * FROM Invalid_table"
    result = db.run_query(invalid_query)
    assert result is None, "Expected query to fail and return None."