CREATE TABLE Documents(
    cod SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    titleqn TEXT NULL,
    cleanTitleQn TEXT NULL,
    pagesRange VARCHAR(15) NULL,
    citations INT NULL CHECK(citations >= 0),
    volume INT NULL CHECK(volume > 0),
    issue CHAR(8) NULL,
    doi TEXT NULL,
    abstract TEXT NULL,
    cleanAbstract TEXT NULL,   
    yearPublished INT NOT NULL CHECK(yearPublished >= 1978),
    language CHAR(2) NULL CHECK(language IN('pt', 'es', 'en')),
    type TEXT NULL CHECK(type IN('review', 'article')),
    UNIQUE(title, volume, issue, yearPublished)
)

CREATE TABLE Authors(
    cod INT,
    author TEXT NOT NULL,
    FOREIGN KEY(cod) REFERENCES Documents(cod),
    PRIMARY KEY(cod, author)
)

CREATE TABLE Keywords(
    keyword TEXT NOT NULL,
    cleanKeyword TEXT,
    PRIMARY KEY(keyword)
)

CREATE TABLE Have(
    cod INT,
    keyword TEXT NOT NULL,
    FOREIGN KEY(cod) REFERENCES Documents(cod),
    FOREIGN KEY(keyword) REFERENCES Keywords(keyword),
    PRIMARY KEY(cod, keyword)
)

CREATE TABLE ChemicalElements (
    z INT PRIMARY KEY,
    symbol VARCHAR(2) NOT NULL UNIQUE,
    name VARCHAR(25) NOT NULL UNIQUE,
    englishname VARCHAR(25) NOT NULL UNIQUE,
    spanishname VARCHAR(25) NOT NULL UNIQUE,
    latim VARCHAR(25) NOT NULL UNIQUE
)

CREATE TABLE Prefixes(
    prefix VARCHAR(20) PRIMARY KEY
)