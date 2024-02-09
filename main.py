from unzip import extractAll
import logging
import os
import xml.etree.ElementTree as ET
import csv
import numpy as np



def main():  
    
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',filename="log.log", level=logging.INFO, datefmt='%Y/%m/%d %I:%M:%S %p')
    logging.info('starting program')
    
    print('Bienvenido al extractor de archivos')
    print('Archivo a procesar: ')
    filePath = str(input())
    report = filePath.replace('zip', 'csv')
    
    with open(report, 'w', newline='') as csvfile:
        fieldnames = ['Emisor', 'RFC','Archivo','Fecha','TipoDeComprobante', 'MetodoPago', 'SubTotal', 'Num Conceptos', 'Clave Unidad','Descripcion', 'Cantidad','Valor Unitario', 'Importe Concepto','SumImporte','Diferencia','Nota','Base','Impuesto','TipoFactor','TasaOCuota','Importe Impuesto', 'Total Impuestos', 'Total Impuestos Trasladados']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
    
        directory = extractAll(filePath)        
        files = os.listdir(directory)
        print('se encontraron ' + str(len(files)) + ' archivos') 
        info1 = []
    
        
        for index_file, file in enumerate(files):
            if index_file != 0:
                writer.writerow([''])
                            
            row = []
            filePath = directory + '/' + file
            tree = ET.parse(filePath)
            root = tree.getroot()
            fecha = root.attrib.get('Fecha')        
            tipoComprobante = root.attrib.get('TipoDeComprobante')
            metodoPago = root.attrib.get('MetodoPago')
            subTotal = round(float(root.attrib.get('SubTotal')),3)    
            
            emisor = root.findall('.//{http://www.sat.gob.mx/cfd/4}Emisor')
            nombre = ''
            rfc = ''
            for emi in emisor:
                nombre = str(emi.get('Nombre'))
                rfc = str(emi.get('Rfc'))                
            
            totalImpuestosTrasladados = 0
            impuestos = root.findall('.//{http://www.sat.gob.mx/cfd/4}Impuestos')            
            for impuesto in impuestos:
                if impuesto.get('TotalImpuestosTrasladados') != None:
                    totalImpuestosTrasladados = impuesto.get('TotalImpuestosTrasladados')                    
                    break
            
            conceptos = root.find('.//{http://www.sat.gob.mx/cfd/4}Conceptos')
            info1 = [nombre, rfc,file, fecha, tipoComprobante, metodoPago, subTotal, len(conceptos)]            
            sumImporte = 0
            sumImporteImpuesto = 0            
            for index, concepto in enumerate(conceptos.findall('.//{http://www.sat.gob.mx/cfd/4}Concepto')):                            
                clave_prod_serv = concepto.get('ClaveProdServ')
                cantidad = concepto.get('Cantidad')
                clave_unidad = concepto.get('ClaveUnidad')
                descripcion = concepto.get('Descripcion')
                valor_unitario = round(float(concepto.get('ValorUnitario')),3)
                importe = round(float(concepto.get('Importe')),3)
                
                row.append(clave_unidad)
                row.append(descripcion)
                row.append(cantidad)
                row.append(valor_unitario)
                row.append(importe)                
                sumImporte = round(sumImporte + float(importe),3)                
                
                
                if index + 1 == len(conceptos):
                    row.append(sumImporte)
                    
                    r = round(sumImporte - subTotal, 3)
                    row.append(r)
                    
                    if sumImporte != subTotal:
                        row.append('desigual')
                    else:
                        row.append('igual')                
                    
                else:
                    row.append('')
                    row.append('')
                    row.append('')                    
                    
                
                impuestos = concepto.findall('.//{http://www.sat.gob.mx/cfd/4}Impuestos')                                
                for impuesto in impuestos:                    
                    traslados = impuesto.find('.//{http://www.sat.gob.mx/cfd/4}Traslados')
                    
                    for index, traslado in enumerate(traslados):                            
                        base = round(float(traslado.get('Base')),3)
                        impuesto_traslado = round(float(traslado.get('Impuesto')),3)
                        tipo_factor = traslado.get('TipoFactor')
                        if tipo_factor == 'Exento':
                            continue                            
                        tasa_cuota = traslado.get('TasaOCuota')
                        if traslado.get('Importe') != None:
                            importeTraslado = round(float(traslado.get('Importe')),3)
                        else:
                            importeTraslado = 0
                        sumImporteImpuesto = sumImporteImpuesto + importeTraslado                                    
                        row.append(base)
                        row.append(impuesto_traslado)
                        row.append(tipo_factor)
                        row.append(tasa_cuota)
                        row.append(importeTraslado)                          
                        row.append(sumImporteImpuesto)                                                         
                        row.append(totalImpuestosTrasladados)
                
                writer.writerow(np.concatenate((info1, row)))                  
                
                if index == len(conceptos):
                    writer.writerow([''])                
                
                row = [] 
        # os.remove(directory)
                
if __name__ == '__main__':
    main()