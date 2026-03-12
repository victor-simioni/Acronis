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
- Backup Storage
- Immutable Storage
- Local Storage
- Microsoft 365
- Google Workspace
- VMware
- Hyper-V
- Physical Servers
- Workstations
- Mobile Devices
- Disaster Recovery
- E muito mais...

## 🏗️ Estrutura do Projeto

Acronis/
├── 📄 .env # Configurações e credenciais
├── 📁 billing/ # Scripts principais
│ ├── 📄 acronis_usage_api.py # Script principal
│ ├── 📄 requirements.txt # Dependências
│ ├── 📄 example_usage.py # Exemplos de uso
│ ├── 📁 acronis_reports/ # Relatórios gerados
│ │ ├── 📊 relatorio_completo_20240312_143022.xlsx
│ │ ├── 📊 relatorio_completo_20240313_093015.xlsx
│ │ └── 📊 relatorio_completo_20240314_172342.xlsx
│ │
│ └── 📁 docs/ # Documentação
├── 📄 README.md # Este arquivo
└── 📄 API_REFERENCE.md # Referência da API

## 📚 Documentação Adicional
API_REFERENCE.md - Documentação completa da API

Arquivo .env
# Configurações da API Acronis
ACRONIS_BASE_URL=https://br02-cloud.acronis.com
ACRONIS_CLIENT_ID=seu_client_id_aqui
ACRONIS_CLIENT_SECRET=seu_client_secret_aqui
ROOT_TENANT_IDS=id_partner1,id_partner2,id_partner3


## Saida 
=============================================================
RELATÓRIO DE USO ACRONIS - COM ABAS POR PARTNER
=============================================================
📁 Arquivo .env usado: /home/user/Acronis/.env
📁 Diretório dos scripts: /home/user/Acronis/billing
📁 Arquivos serão salvos em: /home/user/Acronis/billing/acronis_reports

📋 Coletando clientes do partner: partner_id_1
  📊 50 clientes encontrados
  ✅ 1. Empresa XYZ (uuid-123)
  ✅ 2. Empresa ABC (uuid-456)

📡 Buscando dados de uso...
  📡 Buscando uso em lote para 50 tenants...

✅ Aba 'GERAL' criada com todos os clientes
✅ Aba 'Partner_partner1' criada com 50 clientes
✅ Aba 'Uso Detalhado' criada
✅ Aba 'Resumo' criada

=============================================================
✅ RELATÓRIO GERADO COM SUCESSO!
📁 Arquivo salvo em: /home/user/Acronis/billing/acronis_reports/relatorio_completo_20240312_143022.xlsx
=============================================================

