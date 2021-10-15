users_table = """
    CREATE TABLE users (
        id int PRIMARY KEY,
        email VARCHAR(50),
        password VARCHAR(200),
        fullname VARCHAR(200)
    );
"""

suspicious_docs_table = """
    CREATE TABLE suspicious_docs (
        id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        filename VARCHAR(50),
        num_of_sentences int,
        is_plg boolean default false,
        num_of_plg_sentences int,
        plg_stats_name varchar(50),
        user_id int,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
"""

source_docs_table = """
    CREATE TABLE source_docs  (
        id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        filename VARCHAR(50),
        num_of_sentences int
    );
"""

source_embeddings_table = """
    CREATE TABLE source_embeddings (
        id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        source_id int,
        sentence_index int,
        embedding double precision[],
        FOREIGN KEY(source_id) REFERENCES source_docs(id) ON DELETE CASCADE
    );
"""

insert_a_source_doc = """
    INSERT INTO 
        source_docs (filename, num_of_sentences)
    VALUES
        (%s, %s)
    RETURNING 
        id;
"""

insert_embeddings_of_a_source_file = """
    INSERT INTO
        source_embeddings (source_id, sentence_index, embedding)
    VALUES
        %s;
"""

select_user = """
    SELECT
        id, email, password, fullname
    FROM
        users
    WHERE
        email = %s;
"""

# dùng để lấy tất cả src embeddings
select_all_source_docs_id = """
    SELECT
        id
    FROM
        source_docs;
"""

select_embeddings = """
    SELECT
        source_docs.filename as filename,
        sentence_index,
        embedding
    FROM
        source_embeddings se
    JOIN source_docs
    ON source_docs.id = source_embeddings.source_id
    WHERE 
        source_doc.id IN %s
    ;
"""