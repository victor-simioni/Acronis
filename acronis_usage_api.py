import os
import base64
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
from collections import defaultdict
import sys

# ==============================
# CONFIGURAÇÃO DO CAMINHO DO .ENV
# ==============================
# Obtém o diretório atual do script (Acronis/billing/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível para encontrar a raiz do projeto (Acronis/)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Caminho completo para o arquivo .env na raiz
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

# Carrega as variáveis de ambiente do arquivo .env na raiz
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    print(f"✅ Arquivo .env carregado de: {ENV_PATH}")
else:
    print(f"❌ Arquivo .env não encontrado em: {ENV_PATH}")
    print("Por favor, crie o arquivo .env na raiz do projeto Acronis/")
    sys.exit(1)

# ==============================
# CONFIGURAÇÕES DA API
# ==============================
ACRONIS_BASE_URL = os.getenv("ACRONIS_BASE_URL", "https://br02-cloud.acronis.com")
ACRONIS_CLIENT_ID = os.getenv("ACRONIS_CLIENT_ID")
ACRONIS_CLIENT_SECRET = os.getenv("ACRONIS_CLIENT_SECRET")
PARTNER_IDS = os.getenv("ROOT_TENANT_IDS", "").split(",")

# ==============================
# CONFIGURAÇÃO DO DIRETÓRIO DE EXPORT
# ==============================
# Os relatórios serão salvos em Acronis/billing/acronis_reports/
EXPORT_PATH = os.path.join(SCRIPT_DIR, "acronis_reports")
os.makedirs(EXPORT_PATH, exist_ok=True)

print(f"📁 Raiz do projeto: {PROJECT_ROOT}")
print(f"📁 Diretório dos scripts: {SCRIPT_DIR}")
print(f"📁 Diretório de exportação: {EXPORT_PATH}")
print("=" * 70)

def get_access_token():
    """Autentica no Acronis e retorna o token de acesso."""
    url = f"{ACRONIS_BASE_URL}/api/2/idp/token"
    credentials = f"{ACRONIS_CLIENT_ID}:{ACRONIS_CLIENT_SECRET}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {credentials_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"grant_type": "client_credentials"}
    
    # Verifica se as credenciais foram carregadas
    if not ACRONIS_CLIENT_ID or not ACRONIS_CLIENT_SECRET:
        print("❌ Erro: ACRONIS_CLIENT_ID ou ACRONIS_CLIENT_SECRET não configurados no .env")
        print(f"   Verifique o arquivo: {ENV_PATH}")
        sys.exit(1)
    
    print("🔑 Autenticando...")
    resp = requests.post(url, data=payload, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Erro: {resp.status_code}")
        print(resp.text)
        raise Exception(f"Falha na autenticação: {resp.status_code}")
    
    print("✅ Autenticação OK")
    return resp.json().get("access_token")

def get_customers(partner_id, token):
    """Lista todos os clientes de um partner."""
    url = f"{ACRONIS_BASE_URL}/api/2/tenants?subtree_root_id={partner_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return []
    
    data = resp.json()
    return data.get("items", data.get("tenants", []))

def get_batch_tenant_usage(tenant_ids, token):
    """
    Busca uso de múltiplos tenants em lote usando o endpoint /tenants/usages
    """
    if not tenant_ids:
        return {}
    
    tenants_param = ','.join(tenant_ids)
    url = f"{ACRONIS_BASE_URL}/api/2/tenants/usages"
    headers = {"Authorization": f"Bearer {token}"}
    params = {'tenants': tenants_param}
    
    print(f"  📡 Buscando uso em lote para {len(tenant_ids)} tenants...")
    
    try:
        resp = requests.get(url, headers=headers, params=params)
        
        if resp.status_code == 200:
            data = resp.json()
            return process_usage_batch_response(data)
        else:
            print(f"  ⚠️ Erro no batch usage: {resp.status_code}")
            return {}
    except Exception as e:
        print(f"  ⚠️ Exceção no batch usage: {e}")
        return {}

def get_single_tenant_usage_fallback(tenant_id, token):
    """Fallback para busca individual"""
    try:
        url = f"{ACRONIS_BASE_URL}/api/2/tenants/{tenant_id}/usages"
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            result = {}
            items = data.get("items", [])
            for item in items:
                usage_name = item.get("usage_name", item.get("name", "unknown"))
                result[usage_name] = {
                    'value': item.get("value", 0),
                    'absolute_value': item.get("absolute_value", 0),
                    'measurement_unit': item.get("measurement_unit", ""),
                    'edition': item.get("edition", ""),
                    'application_id': item.get("application_id", ""),
                    'usage_name': usage_name,
                    'friendly_name': get_friendly_name(usage_name)
                }
            return {tenant_id: result}
    except:
        pass
    return {}

def get_friendly_name(usage_name):
    """Retorna nome amigável para o tipo de uso"""
    friendly_names = {
        'storage': 'Backup Storage',
        'immutable_storage': 'Immutable Storage',
        'local_storage': 'Local Storage',
        'archive_storage': 'Archive Storage',
        'workloads': 'Workloads',
        'microsoft365': 'Microsoft 365',
        'google_workspace': 'Google Workspace',
        'vmware': 'VMware',
        'hyperv': 'Hyper-V',
        'physical_servers': 'Physical Servers',
        'workstations': 'Workstations',
        'mobile_devices': 'Mobile Devices',
        'disaster_recovery': 'Disaster Recovery',
        'backup': 'Backup',
        'files_cloud': 'Files Cloud',
        'notary': 'Notary',
        'siem': 'SIEM',
        'edr': 'EDR',
        'mdr': 'MDR'
    }
    return friendly_names.get(usage_name, usage_name.replace('_', ' ').title())

def process_usage_batch_response(data):
    """Processa a resposta do endpoint /tenants/usages"""
    result = defaultdict(lambda: defaultdict(lambda: {
        'value': 0,
        'absolute_value': 0,
        'measurement_unit': '',
        'edition': '',
        'application_id': '',
        'usage_name': '',
        'friendly_name': ''
    }))
    
    items = data.get('items', [])
    
    for item in items:
        tenant_uuid = item.get('tenant')
        usages = item.get('usages', [])
        
        for usage in usages:
            usage_name = usage.get('usage_name', usage.get('name', 'unknown'))
            
            result[tenant_uuid][usage_name] = {
                'value': usage.get('value', 0),
                'absolute_value': usage.get('absolute_value', 0),
                'measurement_unit': usage.get('measurement_unit', ''),
                'edition': usage.get('edition', ''),
                'application_id': usage.get('application_id', ''),
                'usage_name': usage_name,
                'friendly_name': get_friendly_name(usage_name)
            }
    
    return result

def get_tenant_offers(tenant_id, token):
    """Obtém offers/serviços contratados."""
    offers = []
    try:
        url = f"{ACRONIS_BASE_URL}/api/2/tenants/{tenant_id}/resources"
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("items", []):
                if item.get("type") in ["offer", "edition"]:
                    offers.append({
                        "name": item.get("name", ""),
                        "edition": item.get("edition", ""),
                        "status": item.get("status", "")
                    })
    except:
        pass
    return offers

def convert_bytes(bytes_value):
    """Converte bytes para formato legível."""
    if bytes_value == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def clean_sheet_name(name):
    """Limpa o nome da aba para ser válido no Excel"""
    invalid_chars = ['[', ']', ':', '*', '?', '/', '\\']
    for char in invalid_chars:
        name = name.replace(char, '_')
    if len(name) > 31:
        name = name[:31]
    return name

def main():
    print("=" * 70)
    print("RELATÓRIO DE USO ACRONIS - COM ABAS POR PARTNER")
    print("=" * 70)
    print(f"📁 Arquivo .env usado: {ENV_PATH}")
    print(f"📁 Diretório dos scripts: {SCRIPT_DIR}")
    print(f"📁 Arquivos serão salvos em: {EXPORT_PATH}")
    print("=" * 70)
    
    valid_partners = [p.strip() for p in PARTNER_IDS if p and p.strip()]
    if not valid_partners:
        print("❌ Nenhum partner configurado no .env")
        print(f"   Verifique a variável ROOT_TENANT_IDS em: {ENV_PATH}")
        return
    
    try:
        token = get_access_token()
    except Exception as e:
        print(f"❌ Erro autenticação: {e}")
        return
    
    # Dicionários para armazenar dados organizados
    partners_clients = {}  # {partner_id: [clientes]}
    all_clients = []
    all_usage_detail = []
    all_tenant_ids = []
    tenant_info_map = {}
    
    # Coleta todos os tenants organizados por partner
    for partner_id in valid_partners:
        print(f"\n📋 Coletando clientes do partner: {partner_id}")
        tenants = get_customers(partner_id, token)
        
        if not tenants:
            print("  ⚠️ Nenhum cliente encontrado")
            partners_clients[partner_id] = []
            continue
        
        print(f"  📊 {len(tenants)} clientes encontrados")
        partners_clients[partner_id] = []
        
        for tenant in tenants:
            tenant_id = tenant.get("id") or tenant.get("uuid")
            if tenant_id:
                all_tenant_ids.append(tenant_id)
                tenant_info_map[tenant_id] = {
                    "partner_id": partner_id,
                    "name": tenant.get("name", "N/A"),
                    "email": tenant.get("email", ""),
                    "status": tenant.get("status", ""),
                    "kind": tenant.get("kind", "customer"),
                    "created_at": tenant.get("created_at", ""),
                    "offers": get_tenant_offers(tenant_id, token)
                }
                partners_clients[partner_id].append(tenant_id)
    
    if not all_tenant_ids:
        print("\n❌ Nenhum cliente encontrado")
        return
    
    print(f"\n📊 Total de clientes para análise: {len(all_tenant_ids)}")
    
    # Busca dados de uso
    print("\n📡 Buscando dados de uso...")
    batch_usage = get_batch_tenant_usage(all_tenant_ids, token)
    
    # Fallback para busca individual se necessário
    if not batch_usage:
        print("⚠️ Batch falhou, tentando busca individual...")
        batch_usage = {}
        for i, tenant_id in enumerate(all_tenant_ids, 1):
            print(f"  {i}/{len(all_tenant_ids)}: {tenant_id[:8]}...")
            individual_usage = get_single_tenant_usage_fallback(tenant_id, token)
            batch_usage.update(individual_usage)
    
    # Processa os dados e identifica todas as colunas de serviço
    service_columns = set()
    clients_data = {}  # {tenant_id: client_data}
    
    for tenant_id in all_tenant_ids:
        info = tenant_info_map.get(tenant_id, {})
        offers = info.get("offers", [])
        offers_str = ", ".join([f"{o['name']} ({o['edition']})" for o in offers if o.get('name')])
        
        client_data = {
            "Tenant ID": tenant_id,
            "Cliente": info.get("name", "N/A"),
            "Email": info.get("email", ""),
            "Status": info.get("status", ""),
            "Tipo": info.get("kind", "customer"),
            "Criado em": info.get("created_at", ""),
            "Serviços Contratados": offers_str or "Nenhum",
            "Total Storage": "0 B",
            "Total Workloads": 0
        }
        
        tenant_usage = batch_usage.get(tenant_id, {})
        
        total_storage = 0
        total_workloads = 0
        
        for usage_name, usage_data in tenant_usage.items():
            friendly_name = usage_data['friendly_name']
            value = usage_data['value']
            absolute_value = usage_data['absolute_value']
            measurement_unit = usage_data['measurement_unit']
            
            display_value = absolute_value if absolute_value > 0 else value
            
            if measurement_unit == 'bytes' or 'storage' in usage_name.lower():
                col_name = f"{friendly_name}"
                client_data[col_name] = convert_bytes(display_value)
                client_data[f"{friendly_name} (Bytes)"] = display_value
                service_columns.add(col_name)
                
                if 'immutable' not in usage_name.lower():
                    total_storage += display_value
                
                all_usage_detail.append({
                    "Partner ID": info.get("partner_id", ""),
                    "Cliente": info.get("name", "N/A"),
                    "Serviço": friendly_name,
                    "Tipo": "Storage",
                    "Valor": convert_bytes(display_value),
                    "Valor (Bytes)": display_value,
                    "Unidade": measurement_unit,
                    "Edição": usage_data['edition']
                })
            else:
                col_name = f"{friendly_name}"
                client_data[col_name] = display_value
                service_columns.add(col_name)
                
                total_workloads += display_value
                
                all_usage_detail.append({
                    "Partner ID": info.get("partner_id", ""),
                    "Cliente": info.get("name", "N/A"),
                    "Serviço": friendly_name,
                    "Tipo": "Workloads/Contagem",
                    "Valor": display_value,
                    "Valor (Bytes)": 0,
                    "Unidade": measurement_unit,
                    "Edição": usage_data['edition']
                })
        
        client_data["Total Storage"] = convert_bytes(total_storage)
        client_data["Total Workloads"] = total_workloads
        client_data["Storage Bytes Total"] = total_storage
        
        clients_data[tenant_id] = client_data
        
        # Adiciona à lista geral com Partner ID
        client_data_with_partner = client_data.copy()
        client_data_with_partner["Partner ID"] = info.get("partner_id", "")
        all_clients.append(client_data_with_partner)
    
    # Gera nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"relatorio_completo_{timestamp}.xlsx"
    excel_filepath = os.path.join(EXPORT_PATH, excel_filename)
    
    with pd.ExcelWriter(excel_filepath, engine='openpyxl') as writer:
        # 1. Aba GERAL - Todos os clientes
        df_main = pd.DataFrame(all_clients)
        
        # Organiza colunas da aba GERAL
        base_cols = ['Partner ID', 'Tenant ID', 'Cliente', 'Email', 'Status', 
                     'Tipo', 'Criado em', 'Serviços Contratados']
        service_cols = sorted(list(service_columns))
        total_cols = ['Total Storage', 'Total Workloads']
        
        all_cols = base_cols + service_cols + total_cols
        all_cols = [c for c in all_cols if c in df_main.columns]
        
        df_main = df_main[all_cols]
        df_main = df_main.sort_values(['Partner ID', 'Cliente'])
        df_main.to_excel(writer, sheet_name='GERAL', index=False)
        print("\n✅ Aba 'GERAL' criada com todos os clientes")
        
        # 2. Abas por PARTNER
        for partner_id, tenant_ids in partners_clients.items():
            if not tenant_ids:
                continue
            
            # Cria nome da aba
            partner_short = partner_id[:8] if len(partner_id) > 8 else partner_id
            sheet_name = clean_sheet_name(f"Partner_{partner_short}")
            
            # Coleta dados dos clientes deste partner
            partner_data = []
            for tenant_id in tenant_ids:
                if tenant_id in clients_data:
                    client_copy = clients_data[tenant_id].copy()
                    # Remove Partner ID se existir (não necessário na aba do partner)
                    if 'Partner ID' in client_copy:
                        del client_copy['Partner ID']
                    partner_data.append(client_copy)
            
            if partner_data:
                df_partner = pd.DataFrame(partner_data)
                
                # Organiza colunas (sem Partner ID)
                partner_cols = [c for c in all_cols if c != 'Partner ID' and c in df_partner.columns]
                df_partner = df_partner[partner_cols]
                df_partner = df_partner.sort_values('Cliente')
                
                df_partner.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"✅ Aba '{sheet_name}' criada com {len(partner_data)} clientes")
        
        # 3. Aba de USO DETALHADO
        if all_usage_detail:
            df_detail = pd.DataFrame(all_usage_detail)
            df_detail = df_detail.sort_values(['Partner ID', 'Cliente', 'Serviço'])
            df_detail.to_excel(writer, sheet_name='Uso Detalhado', index=False)
            print("✅ Aba 'Uso Detalhado' criada")
        
        # 4. Aba de RESUMO
        if 'Storage Bytes Total' in df_main.columns:
            summary = df_main.groupby('Partner ID').agg({
                'Cliente': 'count',
                'Storage Bytes Total': 'sum',
                'Total Workloads': 'sum'
            }).reset_index()
            
            summary['Storage Total'] = summary['Storage Bytes Total'].apply(convert_bytes)
            summary = summary.rename(columns={'Cliente': 'Total Clientes'})
            summary = summary[['Partner ID', 'Total Clientes', 'Storage Total', 'Total Workloads']]
            
            total_row = pd.DataFrame([{
                'Partner ID': 'TOTAL GERAL',
                'Total Clientes': summary['Total Clientes'].sum(),
                'Storage Total': convert_bytes(summary['Storage Bytes Total'].sum()),
                'Total Workloads': summary['Total Workloads'].sum()
            }])
            
            summary = pd.concat([summary, total_row], ignore_index=True)
            summary.to_excel(writer, sheet_name='Resumo', index=False)
            print("✅ Aba 'Resumo' criada")
        
        # Ajusta largura das colunas em todas as abas
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("\n" + "=" * 70)
    print(f"✅ RELATÓRIO GERADO COM SUCESSO!")
    print(f"📁 Arquivo salvo em: {excel_filepath}")
    print("=" * 70)
    print("\n📊 ESTRUTURA DO RELATÓRIO:")
    print("   • Aba GERAL: Todos os clientes (com Partner ID)")
    print(f"   • {len([p for p in partners_clients.values() if p])} abas de partners (clientes separados)")
    print("   • Aba Uso Detalhado: Cada serviço em uma linha")
    print("   • Aba Resumo: Totais consolidados")
    print("=" * 70)

if __name__ == "__main__":
    main()