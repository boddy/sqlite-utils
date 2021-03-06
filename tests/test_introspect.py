from sqlite_utils.db import Index


def test_table_names(existing_db):
    assert ["foo"] == existing_db.table_names()


def test_table_names_fts4(existing_db):
    existing_db["woo"].insert({"title": "Hello"}).enable_fts(
        ["title"], fts_version="FTS4"
    )
    existing_db["woo2"].insert({"title": "Hello"}).enable_fts(
        ["title"], fts_version="FTS5"
    )
    assert ["woo_fts"] == existing_db.table_names(fts4=True)
    assert ["woo2_fts"] == existing_db.table_names(fts5=True)


def test_detect_fts(existing_db):
    existing_db["woo"].insert({"title": "Hello"}).enable_fts(
        ["title"], fts_version="FTS4"
    )
    existing_db["woo2"].insert({"title": "Hello"}).enable_fts(
        ["title"], fts_version="FTS5"
    )
    assert "woo_fts" == existing_db["woo"].detect_fts()
    assert "woo_fts" == existing_db["woo_fts"].detect_fts()
    assert "woo2_fts" == existing_db["woo2"].detect_fts()
    assert "woo2_fts" == existing_db["woo2_fts"].detect_fts()
    assert None == existing_db["foo"].detect_fts()


def test_tables(existing_db):
    assert 1 == len(existing_db.tables)
    assert "foo" == existing_db.tables[0].name


def test_count(existing_db):
    assert 3 == existing_db["foo"].count


def test_columns(existing_db):
    table = existing_db["foo"]
    assert [{"name": "text", "type": "TEXT"}] == [
        {"name": col.name, "type": col.type} for col in table.columns
    ]


def test_rows(existing_db):
    assert [{"text": "one"}, {"text": "two"}, {"text": "three"}] == list(
        existing_db["foo"].rows
    )


def test_schema(existing_db):
    assert "CREATE TABLE foo (text TEXT)" == existing_db["foo"].schema


def test_table_repr(existing_db):
    assert "<Table foo>" == repr(existing_db["foo"])


def test_indexes(fresh_db):
    fresh_db.conn.executescript(
        """
        create table Gosh (c1 text, c2 text, c3 text);
        create index Gosh_c1 on Gosh(c1);
        create index Gosh_c2c3 on Gosh(c2, c3);
    """
    )
    assert [
        Index(
            seq=0,
            name="Gosh_c2c3",
            unique=0,
            origin="c",
            partial=0,
            columns=["c2", "c3"],
        ),
        Index(seq=1, name="Gosh_c1", unique=0, origin="c", partial=0, columns=["c1"]),
    ] == fresh_db["Gosh"].indexes
