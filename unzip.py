from zipfile import ZipFile
from datetime import date
import os
from datetime import datetime
import logging


unzipFiles = './unzipFiles'
def extractAll(filePath):
    if not filePath or not os.path.exists(filePath):
            print('** No se encontro el archivo: '+ filePath + ' **')
            logging.error('file not found, filePath: ' + filePath)
            exit()

    with ZipFile(filePath, 'r') as zObject:                
        now = str(datetime.now()).replace(":", "-")
        path = os.path.join(unzipFiles, now)
        print("extrayendo archivos")
        logging.info('extracting files')
        zObject.extractall(path)
        logging.info("done extracting files")
        print("se termino de extraer los archivos")
    
    return path
