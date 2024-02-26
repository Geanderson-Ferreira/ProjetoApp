from src.db_manager.populater import populate
from sys import argv
#from src.tests.tester import test_list_orders
import os
from src.db_manager.config import DEV_ENV_RUNNER_CONFIG
import socket

# Key é o parametro, o Value é a funcao.
ARGV_FUNCTIONS = {
    'Parametros aceitos no modulo manage.py \n': '',
    'help': lambda: [print('> ', key) for key in ARGV_FUNCTIONS.keys()],
    'populateDB': populate,
    'run': lambda: os.system(DEV_ENV_RUNNER_CONFIG[socket.gethostname()])
}

def run_arguments():
    if len(argv) > 1:
        arg2 = argv[2] if len(argv) > 2 else None

        for i in argv:
            if i in ARGV_FUNCTIONS.keys():
                ARGV_FUNCTIONS[argv[1]]()#(arg2)
                exit()

        print(f"\nFuncao '{argv[1]}' nao definida no escopo manager.\n")

run_arguments()
