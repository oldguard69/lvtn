users_table = """
    CREATE TABLE users (
        id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
        unique_filename varchar(50) unique,
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

###################################### USERS ######################################
insert_a_user = """
    INSERT INTO
        users (email, password, fullname)
    VALUES
        (%s, %s, %s);
"""

select_a_user = """
    SELECT
        id, email, password, fullname
    FROM
        users
    WHERE
        email = %s;
"""
####################################################################################


###################################### SOURCE DOCS ######################################
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
        source_embeddings
    JOIN source_docs
    ON source_docs.id = source_embeddings.source_id
    WHERE 
        source_docs.id IN %s
    ;
"""
####################################################################################


###################################### SUSPICIOUS DOCS ######################################
insert_a_susp_doc = """
    INSERT INTO
        suspicious_docs (filename, num_of_sentences, is_plg, num_of_plg_sentences, unique_filename, user_id)
    VALUES
        (%s, %s, %s, %s, %s, %s)
    RETURNING
        id;
"""

select_suspicious_docs = """
    SELECT
        id, filename, num_of_sentences, is_plg, num_of_plg_sentences, unique_filename, user_id
    FROM
        suspicious_docs
    WHERE
        user_id = %s;
"""

select_a_suspicious_doc = """
    SELECT
        id, filename, num_of_sentences, is_plg, num_of_plg_sentences, unique_filename, user_id
    FROM 
        suspicious_docs
    WHERE
        id = %s AND user_id = %s;
"""
####################################################################################
