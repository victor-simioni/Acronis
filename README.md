# Acronis

# 📊 Acronis Usage Reporting API

<div align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/license-MIT-green.svg">
  <img src="https://img.shields.io/badge/API-Acronis-orange.svg">
  <img src="https://img.shields.io/badge/status-stable-brightgreen.svg">
</div>

<p align="center">
  <strong>Script em Python para gerar relatórios detalhados de uso dos clientes na plataforma Acronis via API</strong>
</p>

<p align="center">
  <a href="#-sobre">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-estrutura">Estrutura</a> •
  <a href="#-começando">Começando</a> •
  <a href="#-configuração">Configuração</a> •
  <a href="#-exemplo">Exemplo</a> •
  <a href="#-agendamento">Agendamento</a> •
  <a href="#-contribuição">Contribuição</a>
</p>

---

## 📋 Sobre

Este projeto automatiza a extração de dados de uso da API da Acronis e gera relatórios completos em Excel, facilitando a análise de consumo por cliente e por serviço. Ideal para provedores de serviço (MSPs) que precisam monitorar o uso de seus clientes na plataforma Acronis.

## ✨ Funcionalidades

### ✅ **Coleta de Dados**
- Autenticação automática na API Acronis
- Listagem de todos os clientes por partner
- Dados de uso por serviço (Storage, Workloads, Microsoft 365, VMware, etc.)
- Suporte a múltiplos partners em uma única execução
- Fallback automático para busca individual se o batch falhar

### 📊 **Relatório Excel Completo**

| Aba | Descrição |
|-----|-----------|
| **GERAL** | Todos os clientes com serviços em colunas |
| **Partner_*** | Clientes separados por partner (uma aba por partner) |
| **Uso Detalhado** | Cada serviço em uma linha (formato longo) |
| **Resumo** | Totais consolidados por partner |

### 🎯 **Tipos de Serviços Suportados**

| Categoria | Serviços |
|-----------|----------|
| 💾 **Storage** | Backup, Immutable, Local, Archive |
| ☁️ **SaaS** | Microsoft 365, Google Workspace |
| 🖧 **Virtual** | VMware, Hyper-V |
| 🖥️ **Physical** | Servers, Workstations, Mobile |
| 🔄 **DR** | Disaster Recovery |
| 📦 **Outros** | Workloads e muito mais |

## 📋 Descrição dos Arquivos

| Ícone | Arquivo/Pasta | Tipo | Descrição |
|:-----:|---------------|------|-----------|
| 📄 | `.env` | `config` | Credenciais da API (ACRONIS_CLIENT_ID, ACRONIS_CLIENT_SECRET, ROOT_TENANT_IDS) |
| 📁 | `billing/` | `folder` | Diretório principal com todos os scripts |
| 🐍 | `acronis_usage_api.py` | `python` | Script principal com todas as funções de coleta e relatório |
| 📦 | `requirements.txt` | `deps` | Lista de bibliotecas necessárias |
| 📚 | `example_usage.py` | `example` | Script com exemplos de uso e execução agendada |
| 📁 | `acronis_reports/` | `output` | Pasta onde os relatórios Excel são salvos |
| 📊 | `relatorio_completo_*.xlsx` | `excel` | Relatórios gerados com timestamp |
| 📁 | `docs/` | `docs` | Documentação completa do projeto |
| 📄 | `README.md` | `doc` | Visão geral, instalação e configuração |
| 📄 | `API_REFERENCE.md` | `doc` | Referência técnica da API Acronis |


## ⚙️ Configurações da API Acronis

| Ícone | Variável | Tipo | Descrição | Exemplo |
|:-----:|----------|------|-----------|---------|
| 🌐 | `ACRONIS_BASE_URL` | `url` | URL base do data center Acronis | `https://br02-cloud.acronis.com` |
| 🔑 | `ACRONIS_CLIENT_ID` | `client_id` | ID do cliente para autenticação OAuth | `seu_client_id_aqui` |
| 🔒 | `ACRONIS_CLIENT_SECRET` | `secret` | Secret do cliente para autenticação OAuth | `seu_client_secret_aqui` |
| 👥 | `ROOT_TENANT_IDS` | `tenant_ids` | IDs dos tenants partners (separados por vírgula) | `id_partner1,id_partner2,id_partner3` |

## 📚 Documentação Adicional
API_REFERENCE.md - Documentação completa da API

