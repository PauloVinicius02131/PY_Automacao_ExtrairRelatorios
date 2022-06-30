# PY_Automacao_ExtrairRelatorios
Projeto utilizando python para extrair relatórios de um sistema web. 

  Confecionei esse script para alimentar uma base de dados para a empresa em que trabalho e realizar integração entre os dados de dois sistemas. Após a extração desses
relatórios existe uma rotina de Pentaho PDI para o tratamento e cruzamento dos sistemas.

Algumas observações importantes:
    
    O sistema gera estouro ao fazer a chamada do relatório com vários veículos selecionados, por isso o loop de gerar um relatório para cada registro na linha.
    
    O sistema apresenta erro como um span dentro de uma div, então por isso o while para testar o erro.
