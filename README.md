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
