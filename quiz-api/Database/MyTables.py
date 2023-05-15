
# Database tables
# Key : table name
# Value : SQL script
TABLES = {
    'questions': '''
        CREATE TABLE questions
        (
            id INTEGER NOT NULL,
            title TEXT NOT NULL,
            image TEXT,
            position INTEGER,
            text TEXT,

            CONSTRAINT pk_qu_id PRIMARY KEY(id)
        )
    ''',
    'possible_answers': '''
        CREATE TABLE possible_answers
        (
            id INTEGER NOT NULL,
            text TEXT NOT NULL,
            isCorrect INTEGER,
            nbSips INTEGER,
            questionId INTEGER NOT NULL,

            CONSTRAINT pk_an_id PRIMARY KEY (id),
            CONSTRAINT isCorrect_ck CHECK (isCorrect BETWEEN 0 AND 1),
            CONSTRAINT fk_qu_id FOREIGN KEY (questionId) REFERENCES questions(id)
        );
    ''',
    'participations': '''
        CREATE TABLE participations
        (
            id INTEGER NOT NULL,
            score REAL,
            playerName TEXT,
            date TEXT,

            CONSTRAINT pk_sc_id PRIMARY KEY (id)
        );
    '''
}
