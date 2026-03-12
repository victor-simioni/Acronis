#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de uso do script acronis_usage_api.py
"""

import os
from acronis_usage_api import main as gerar_relatorio

def exemplo_basico():
    """Executa o relatório padrão"""
    print("=" * 50)
    print("EXEMPLO 1: Relatório Padrão")
    print("=" * 50)
    gerar_relatorio()

def exemplo_com_parametros():
    """
    Exemplo de como poderia ser expandido para aceitar parâmetros
    (função main modificada para aceitar argumentos)
    """
    print("=" * 50)
    print("EXEMPLO 2: Relatório com Parâmetros")
    print("=" * 50)
    
    # Aqui você poderia passar parâmetros específicos
    # como data inicial, filtros, etc.
    
    # Por enquanto, apenas chama a função principal
    gerar_relatorio()

def exemplo_agendado():
    """
    Exemplo para execução agendada (cron job / task scheduler)
    """
    print("=" * 50)
    print("EXEMPLO 3: Execução Agendada")
    print("=" * 50)
    
    import schedule
    import time
    
    def job():
        print(f"\n📅 Executando em: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        gerar_relatorio()
    
    # Agenda para executar toda segunda-feira às 08:00
    schedule.every().monday.at("08:00").do(job)
    
    print("⏰ Agendador iniciado. Pressione Ctrl+C para parar.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    except KeyboardInterrupt:
        print("\n⏹️  Agendador parado.")

if __name__ == "__main__":
    print("🔧 ESCOLHA O EXEMPLO:")
    print("1 - Relatório básico")
    print("2 - Relatório com parâmetros")
    print("3 - Execução agendada")
    
    escolha = input("Digite o número (1-3): ").strip()
    
    if escolha == "1":
        exemplo_basico()
    elif escolha == "2":
        exemplo_com_parametros()
    elif escolha == "3":
        exemplo_agendado()
    else:
        print("❌ Opção inválida")