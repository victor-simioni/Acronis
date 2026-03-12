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

## 🏗️ 📋 Descrição dos Arquivos
    <div class="container">
        <h2>📋 Descrição dos Arquivos</h2>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>📁 Arquivo/Pasta</th>
                        <th>🔧 Tipo</th>
                        <th>📝 Descrição</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <span class="emoji">📄</span>
                            <span class="file-name">.env</span>
                            <span class="badge">config</span>
                        </td>
                        <td><span class="file-type type-config">⚙️ Configuração</span></td>
                        <td class="description">Credenciais da API (ACRONIS_CLIENT_ID, ACRONIS_CLIENT_SECRET, ROOT_TENANT_IDS)</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📁</span>
                            <span class="file-name">billing/</span>
                        </td>
                        <td><span class="file-type type-folder">📁 Pasta</span></td>
                        <td class="description">Diretório principal com todos os scripts</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">🐍</span>
                            <span class="file-name">acronis_usage_api.py</span>
                        </td>
                        <td><span class="file-type type-script">🐍 Script</span></td>
                        <td class="description">Script principal com todas as funções de coleta e relatório</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📦</span>
                            <span class="file-name">requirements.txt</span>
                        </td>
                        <td><span class="file-type type-deps">📦 Dependências</span></td>
                        <td class="description">Lista de bibliotecas necessárias (requests, pandas, python-dotenv, openpyxl)</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📚</span>
                            <span class="file-name">example_usage.py</span>
                        </td>
                        <td><span class="file-type type-example">📚 Exemplo</span></td>
                        <td class="description">Script com exemplos de uso e execução agendada</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📁</span>
                            <span class="file-name">acronis_reports/</span>
                        </td>
                        <td><span class="file-type type-folder">📁 Relatórios</span></td>
                        <td class="description">Pasta onde os relatórios Excel são salvos automaticamente</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📊</span>
                            <span class="file-name">relatorio_completo_*.xlsx</span>
                        </td>
                        <td><span class="file-type type-excel">📊 Excel</span></td>
                        <td class="description">Relatórios gerados com timestamp (formato: YYYYMMDD_HHMMSS)</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📁</span>
                            <span class="file-name">docs/</span>
                        </td>
                        <td><span class="file-type type-folder">📁 Documentação</span></td>
                        <td class="description">Documentação completa do projeto</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📄</span>
                            <span class="file-name">README.md</span>
                        </td>
                        <td><span class="file-type type-doc">📄 Documento</span></td>
                        <td class="description">Visão geral, instalação e configuração do projeto</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📄</span>
                            <span class="file-name">API_REFERENCE.md</span>
                        </td>
                        <td><span class="file-type type-doc">📄 Documento</span></td>
                        <td class="description">Referência técnica da API Acronis com endpoints e exemplos</td>
                    </tr>
                    <tr>
                        <td>
                            <span class="emoji">📄</span>
                            <span class="file-name">TROUBLESHOOTING.md</span>
                        </td>
                        <td><span class="file-type type-doc">📄 Documento</span></td>
                        <td class="description">Guia de solução de problemas com erros comuns e soluções</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="footer-note">
            <span class="emoji">📌</span> Total de itens: 11 | 
            <span class="emoji">📁</span> Pastas: 3 | 
            <span class="emoji">📄</span> Arquivos: 8
        </div>
    </div>

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

