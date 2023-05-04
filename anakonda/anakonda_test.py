import pytest

from anakonda.model import Task


@pytest.mark.order(0)
def test_env(app):
    assert app.config.get("ENV") == "test"


@pytest.mark.order(0)
def test_debug(app):
    assert app.config.get("DEBUG") is True


@pytest.mark.order(0)
def test_database(db, app):
    with app.app_context():
        assert db.engine.url.database == "test"


@pytest.mark.order(100)
def test_seed_database(storage, db, app):
    test = Task(
        name="test",
        namespace="test",
        runtime="docker",
        image="alpine:latest",
        script="id",
        status="pending",
    )
    with app.app_context():
        db.session.add(test)
        db.session.commit()
        storage.set("test", test.id)
        print(test)


@pytest.mark.order(100000)
def test_down_database(storage, db, app):
    with app.app_context():
        db.session.query(Task).delete()
        db.session.commit()
