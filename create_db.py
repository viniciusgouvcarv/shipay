import sqlite3

conn = sqlite3.connect('transations.db')
cursor = conn.cursor()

# Create table of emporia "estabelecimentos"
cursor.execute("""
CREATE TABLE estabelecimentos (
        nome TEXT NOT NULL,
        cnpj VARCHAR(18) PRIMARY KEY,
        dono TEXT NOT NULL,
        telefone TEXT
);
""")

# Create table of receivements "recebimentos"
cursor.execute("""
CREATE TABLE recebimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente VARCHAR(14) NOT NULL,
        cnpj_estabelecimento VARCHAR(18) NOT NULL,
        valor REAL NOT NULL,
        descricao TEXT,
        FOREIGN KEY (cnpj_estabelecimento) REFERENCES estabelecimentos(cnpj)
);
""")

# Insert the first emporium into "estabelecimentos" table
cursor.execute("""
INSERT INTO estabelecimentos (nome, cnpj, dono, telefone)
VALUES ("Nosso Restaurante de Todo Dia LTDA", "45.283.163/0001-67", "Fabio I.", "11909000300");
""")

conn.commit()
conn.close()