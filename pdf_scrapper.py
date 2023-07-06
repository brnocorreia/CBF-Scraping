import pandas as pd
import pdfplumber
import pdfquery


def pdfscrape_infojogo_pattern1(pdf):
  #Extracting each relevant information individually
  # for count in range(pagecount - 1):
  #   if pdf.pq('LTTextLineHorizontal:contains("{}")'.format("ALUGUEIS E SEGUROS")):
  #     index = 3
  #   else: 
  #     index = 0

  # total =  pdf.pq('LTTextLineHorizontal:contains("{}")'.format("TOTAL"))[index] 
  # x0 = float(total.get('x0',0)) + 156.4
  # y0 = float(total.get('y0',0))
  # x1 = float(total.get('x1',0)) + 155.41
  # y1 = float(total.get('y1',0))
  # total_disponivel = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text().replace(".","")

  # x0 = float(total.get('x0',0)) + 269.79
  # y0 = float(total.get('y0',0))
  # x1 = float(total.get('x1',0)) + 268.8
  # y1 = float(total.get('y1',0))
  # total_vendidos = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text().replace(".","")

  # x0 = float(total.get('x0',0)) + 387.83
  # y0 = float(total.get('y0',0))
  # x1 = float(total.get('x1',0)) + 398.516
  # y1 = float(total.get('y1',0))
  # renda = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text().replace(".","").replace(",",".")

  numero_jogo =  pdf.pq('LTTextLineHorizontal:contains("{}")'.format("RODADA"))[0] 
  x0 = float(numero_jogo.get('x0',0)) + 104.98
  y0 = float(numero_jogo.get('y0',0))
  x1 = float(numero_jogo.get('x1',0)) + 65.101
  y1 = float(numero_jogo.get('y1',0))
  info_jogo = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()

  rodada = info_jogo.split("/")[0]
  partida = info_jogo.split("/")[1]


  competicao = pdf.pq('LTTextLineHorizontal:overlaps_bbox("108.42, 740.541, 231.732, 747.541")').text()

  jogo = pdf.pq('LTTextLineHorizontal:overlaps_bbox("75.17, 726.371, 264.982, 733.371")').text()

  time_casa = jogo.split("X")[0]
  time_fora = jogo.split("X")[1]

  #Combined all relevant info into a single observation

  page = pd.DataFrame({
      'Competição': competicao,
      'Rodada': int(rodada),
      'Partida': int(partida),
      "Mandante": time_casa,
      "Visitante": time_fora,
      # "Ingressos Disponíveis": int(total_disponivel),
      # "Ingressos Vendidos": int(total_vendidos),
      # "Renda": float(renda),
      }, index=[0])
  return(page)


def pdfscrape_infopublico_pattern1(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
    first_page = pdf.pages[0]
    table = first_page.extract_table()

  df = pd.DataFrame(table[1:], columns=table[0])
  df.drop(df.columns[[0]], axis=1, inplace=True)
  df.columns = ['INGRESSOS', 'DISPONÍVEL', 'DEVOLVIDOS', 'VENDIDOS', 'PREÇO', 'ARRECADAÇÃO']
  df = df.drop(0)

  inteiros = ['DISPONÍVEL', 'DEVOLVIDOS', 'VENDIDOS']
  floats = ['PREÇO', 'ARRECADAÇÃO']

  for inteiro in inteiros:
    df[inteiro] = pd.to_numeric(df[inteiro].str.replace('.', ''), errors='coerce').astype('Int64')
    
  for floater in floats:
    df[floater] = pd.to_numeric(df[floater].str.replace('[.,]', '', regex=True), errors='coerce')/100

  df = df[df['INGRESSOS'] == 'TOTAL']

  ingressos_disponiveis = df['DISPONÍVEL'].iloc[-1]
  publico_pagante = df['VENDIDOS'].iloc[-1]
  total_renda = df['ARRECADAÇÃO'].iloc[-1]

  page = pd.DataFrame({
    'Ingressos Disponíveis': [ingressos_disponiveis],
    'Pagantes': [publico_pagante],
    'Renda': [total_renda],
  }, index=[0])

  return(page)
  