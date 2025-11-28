import subprocess
import sys
import time
import requests
import os
import signal

def testar_caminho_feliz():
    print("\n=== INICIANDO TESTE AUTOMATIZADO 'CAMINHO FELIZ' ===\n")

    # 1. Iniciar o sistema (iniciar_todos.py) em background
    print("1. Subindo microserviços...")
    # Ajuste para o caminho correto
    processo_sistema = subprocess.Popen(
        [sys.executable, "sistema_delivery/iniciar_todos.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguarda inicialização
    time.sleep(10) 
    print("   -> Microserviços devem estar online agora.\n")

    base_url = "http://localhost:5000"
    
    try:
        # 2. Criar Cliente
        print("2. Cadastrando Cliente...")
        cliente_data = {
            "nome": "João Silva",
            "email": "joao@email.com"
        }
        resp_cliente = requests.post(f"{base_url}/api/clientes", json=cliente_data)
        print(f"   Status: {resp_cliente.status_code}")
        print(f"   Resp: {resp_cliente.json()}")
        cliente_id = resp_cliente.json()['cliente']['id']

        # 3. Criar Produto
        print("\n3. Cadastrando Produto...")
        produto_data = {
            "nome": "Pizza de Calabresa",
            "preco": 45.90,
            "estoque": 10
        }
        resp_produto = requests.post(f"{base_url}/api/produtos", json=produto_data)
        print(f"   Status: {resp_produto.status_code}")
        print(f"   Resp: {resp_produto.json()}")
        produto_id = resp_produto.json()['produto']['id']

        # 4. Realizar Pedido
        print("\n4. Realizando Pedido...")
        pedido_data = {
            "cliente_id": cliente_id,
            "itens": [
                {"produto_id": produto_id, "quantidade": 2}
            ],
            "endereco_entrega": "Rua das Flores, 123"
        }
        resp_pedido = requests.post(f"{base_url}/api/pedidos", json=pedido_data)
        print(f"   Status: {resp_pedido.status_code}")
        print(f"   Resp: {resp_pedido.json()}")
        pedido_id = resp_pedido.json().get('pedido_id')

        # 5. Aguardar processamento (Filas)
        print("\n5. Aguardando processamento assíncrono (5 segundos)...")
        for i in range(5):
            print(f"   Processando... {5-i}")
            time.sleep(1)

        # 6. Verificar Status do Pedido
        print("\n6. Consultando Pedidos Processados (Microserviço Processar Pedido)...")
        resp_lista = requests.get(f"{base_url}/api/pedidos")
        pedidos = resp_lista.json().get('pedidos', [])
        
        pedido_encontrado = None
        for p in pedidos:
            if p.get('pedido_id') == pedido_id:
                pedido_encontrado = p
                break
        
        if pedido_encontrado:
            print(f"   ✅ Pedido Encontrado!")
            print(f"   Status: {pedido_encontrado.get('status')}")
            print(f"   Total: R$ {pedido_encontrado.get('total')}")
        else:
            print(f"   ❌ Pedido ainda não aparece na lista de processados.")

        # 7. Verificar Recomendações
        print(f"\n7. Consultando Recomendações para o Cliente {cliente_id}...")
        resp_rec = requests.get(f"{base_url}/api/recomendacoes/{cliente_id}")
        print(f"   Status: {resp_rec.status_code}")
        print(f"   Resp: {resp_rec.json()}")

        # 8. Verificar Analytics
        print("\n8. Consultando Relatório de Analytics...")
        resp_analytics = requests.get("http://localhost:5006/relatorio")
        print(f"   Status: {resp_analytics.status_code}")
        print(f"   Resp: {resp_analytics.json()}")

    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")

    finally:
        print("\n=== FIM DO TESTE ===")
        print("Encerrando microserviços...")
        # Mata o processo pai e tenta matar os filhos (no Windows é meio chato, mas vamos tentar)
        processo_sistema.terminate()
        # Comando forçado para matar pythons soltos (cuidado em produção!)
        if os.name == 'nt':
            os.system("taskkill /f /im python.exe /t")
        else:
            os.system("pkill -f lambda_function.py")
        print("Sistema encerrado.")

if __name__ == "__main__":
    testar_caminho_feliz()
