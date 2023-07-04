# URL from which pdfs to be downloaded
import os
import time

import pandas as pd
from download_pdf import download_pdf_file
import pdfquery
from dotenv import load_dotenv

from pdf_scrapper import pdfscrape_infojogo_pattern1, pdfscrape_infopublico_pattern1

load_dotenv()

PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH")

partidas = [129, 9, 109, 107, 110]

colunas = ['Competição', 'Rodada', 'Partida', 'Mandante', 'Visitante', 'Pagantes', 'Renda']
tabela_publico = pd.DataFrame(columns=colunas)

for partida in partidas:
    URL = f'https://conteudo.cbf.com.br/sumulas/2023/142{partida}b.pdf'
    download_pdf_file(URL)

    path = PDF_FOLDER_PATH
    with open(os.path.join(path, f'jogo_{partida}.pdf'), 'rb') as pdf_path:
        pdf = pdfquery.PDFQuery(pdf_path)
        pdf.load()
        pdf.tree.write(f'boletim_{partida}.txt', pretty_print = True)

        pagecount = pdf.doc.catalog['Pages'].resolve()['Count']
        for p in range(pagecount - 1):
            pdf.load(p)
            page_jogo = pdfscrape_infojogo_pattern1(pdf) 
            
        page_publico = pdfscrape_infopublico_pattern1(pdf_path)

        page_merged = pd.concat([page_jogo, page_publico], axis=1)
        tabela_publico = tabela_publico.append(page_merged, ignore_index=True).sort_values('Partida')
    
    remove_pdf_path = os.path.join(PDF_FOLDER_PATH, f'jogo_{partida}.pdf')
    remove_boletim_path = os.path.join(os.getcwd(), f'boletim_{partida}.txt')
    os.remove(remove_pdf_path)
    os.remove(remove_boletim_path)
    
# tabela_publico = tabela_publico.reset_index(drop=True, inplace=True)

if(os.path.exists('C:/src/python/CBF-Scraping/tabela_publico/tabela_publico.csv')):
    tabela_publico.to_csv('C:/src/python/CBF-Scraping/tabela_publico/tabela_publico.csv', mode='a',header=False, index=False)
else: 
    tabela_publico.to_csv('C:/src/python/CBF-Scraping/tabela_publico/tabela_publico.csv', mode='a',header=True, index=False)

