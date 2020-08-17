# -*- coding: utf-8 -*-
# João, dá uma olhada no PEP-8 https://wiki.python.org.br/GuiaDeEstilo.
# Tenta sempre comentar as funções, que é mais fácil na hora da revisão.
# Sempre fique com, no máximo, 1 linha em branco para não dar volume ao código.

# Eu dividi os imports entre os da biblioteca padrão e os da aplicação.
# Biblioteca Padrão
import os
import sys
import traceback
import logging
import configparser
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta, timezone

# Específicos da Aplicação
import xlsxwriter
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def main(argv):
    """Iniciate the program."""
    greetings()

    print('Press Crtl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Config and add a handler to the app
    app = Flask(__name__)
    handler = RotatingFileHandler('bot.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    

    # Assign the database and set the config
    # Tente nunca chegar a 80 colunas.
    app.config['SQLALCHEMY_DATABASE_URI'] = """postgresql+psycopg2://
        postgres:123mudar@127.0.0.1:5432/bot_db"""
    db = SQLAlchemy(app)
    config = configparser.ConfigParser()
    config.read('/tmp/bot/settings/config.ini')

    # Assign the scheduler and make a warning
    var1 = int(config.get('scheduler','IntervalInMinutes'))
    app.logger.warning("Intervalo entre as execucoes do processo: "
        "{}".format(var1))
    scheduler = BlockingScheduler()

    # Add jobs
    task1_instance = scheduler.add_job(task1(db), 'interval', id='task1_job',
        minutes=var1)

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        pass

def greetings():
    print('             ##########################')
    print('             # - ACME - Tasks Robot - #')
    print('             # - v 1.0 - 2020-07-28 - #')
    print('             ##########################')

def task1(db):
    """Read the database and put the data on the worksheet."""
    now = datetime.now()
    file_name = 'data_export_{0}.xlsx'.format(now.strftime("%Y%m%d%H%M%S"))
    file_path = os.path.join(os.path.curdir, file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    orders = db.session.execute('SELECT * FROM users;')
    index = 1
    columns = ['Id', 'Name', 'Email', 'Password', 'Role Id',
        'Created At', 'Updated At']
    worksheet_columns = 'ABCDEFG'
    other_index = 0

    # Lembra do DRY? Don't Repeat Yourself. Use mais iterações
    for column in columns:
        worksheet.write(worksheet_columns[other_index] +'{0}'.format(index),
            column)
        other_index += 1

    other_index = 0

    # Write the data from the database into the worksheet
    for order in orders:
        index += 1 # DRY outra vez

        print(column[other_index], '{0}'.format(order[other_index]))
        worksheet.write(worksheet_columns[other_index] + '{0}'.format(index),
            order[other_index])

        other_index += 1

    workbook.close()
    print('job executed!')

if __name__ == '__main__':
    main(sys.argv)

# Não esquece de apagar todos os comentários em português depois ;p