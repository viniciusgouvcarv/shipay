Para utilizar a API, você precisará instalar o Python 3 em sua máquina (que você pode adquirir aqui https://www.python.org/downloads/release/python-382/). Então, precisará dos módulos Flask e SQLite, que podem ser instalados no seu terminal normalmente através dos comandos ``pip install sqlite3`` e ``pip install flask``.

Para rodar o programa, abra o prompt de comando e digite ``cd /caminho/até/o/arquivo/da/api`` e pressione enter. Então digite ``python server.py`` ou ``python3 server.py``. A API funcionará até você apertar "Ctrl+C" ou "Ctrl+Break" e poderá ser acessada pela URL base "http://127.0.0.1:5000/" e os paths "api/v1/estabelecimento" e "api/v1/transacao".

**api/v1/transacao**

Salva a transação no banco de dados. Só recebe o método POST com JSONs no seguinte formato:

``{
    "estabelecimento": "00.000.000/0000-00",
    "cliente": "000.000.000-00"
    "valor": 1.01
    "descricao": "Descrição da venda!"
}
``

É esperada a resposta ``{"aceito":true}`` e o código 201, caso o JSON esteja correto. Se algum dos dados estiver inválido, (ex: valor como string, CPF ou CNPJ em outro formato, etc) espera-se a resposta ``{"aceito":false}`` e o código 400.

**api/v1/estabelecimento**

Consulta todas as transações de um estabelecimento. Só recebe o método GET e deve ser passado o CNPJ na URL da seguinte forma: "http://127.0.0.1:5000/api/v1/estabelecimento?cnpj=00.000.000/0000-00".

É esperada a resposta no seguinte formato: ``{
    "estabelecimento": {
        "nome": "ESTABELECIMENTO PADRÃO",
        "cnpj": "00.000.000/0000-00",
        "dono": "Nome do Proprietário.",
        "telefone": "11999999999",
    },
    "recebimentos": [
        {
            "cliente": "000.000.000-00",
            "valor": 1.01,
            "descricao": "Descrição da venda!"
        },
        {
            "cliente": "000.000.000-001",
            "valor": 1,
            "descricao": "Descrição da venda!"
        },
    ],
    "total_recebido": 2.01
}``
