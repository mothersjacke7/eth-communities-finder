import requests
import networkx as nx
import community
import matplotlib.pyplot as plt
import os
from rich.console import Console

os.system('cls' if os.name == 'nt' else 'clear')
console = Console()

etherscan_api_key = "CWG3A9W84UTGQNKUXP63DA614HD8P177XK"

def read_addresses_from_file(file_path):
    with open(file_path, 'r') as file:
        addresses = [line.strip() for line in file.readlines()]
    return addresses

def get_transactions_for_address(address):
    etherscan_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={etherscan_api_key}'
    response = requests.get(etherscan_url)
    if response.status_code == 200:
        data = response.json()
        transactions = data.get('result', [])
        return transactions
    else:
        console.print(f"Ошибка HTTP для адреса {address}: {response.status_code}")
        return []

def add_transactions_to_graph(graph, transactions):
    for tx in transactions:
        sender = tx['from']
        receiver = tx['to']
        graph.add_edge(sender, receiver)

def draw_graph(G, partition):
    pos = nx.spring_layout(G)
    cmap = plt.cm.get_cmap("viridis", max(partition.values()) + 1)
    nx.draw(G, pos, node_color=list(partition.values()), cmap=cmap, with_labels=True)
    plt.show()

def detect_communities(graph, addresses_from_file):
    partition = community.best_partition(graph)
    console.print("Результаты анализа:")
    console.print(f"Общее количество узлов (адресов): {graph.number_of_nodes()}")
    console.print(f"Общее количество связей (транзакций): {graph.number_of_edges()}")
    console.print(f"Количество обнаруженных сообществ: {len(set(partition.values()))}")

    communities = group_by_community(partition)
    for community_id, wallets in communities.items():
        console.print(f"Сообщество #{community_id}: содержит {len(wallets)} вхождений.")

    detect_cross_community_connections(graph, partition, addresses_from_file)

    draw_graph(graph, partition)

def group_by_community(partition):
    communities = {}
    for wallet, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append((wallet, community_id))
    return communities

def detect_cross_community_connections(graph, partition, addresses_from_file):
    for wallet, community_id in partition.items():
        if wallet in addresses_from_file and len(set(partition.values())) > 1:
            other_communities = set(partition.values()) - {community_id}
            connected_wallets = set()

            for neighbor in graph.neighbors(wallet):
                if partition[neighbor] in other_communities:
                    connected_wallets.add(neighbor)

            if connected_wallets:
                console.print(f"Кошелек {wallet} соединен с кошельками из других сообществ:")
                for connected_wallet in connected_wallets:
                    console.print(f"  общий кошелек - {connected_wallet}")
            else:
                for other_community_id in other_communities:
                    if has_indirect_connection(graph, partition, wallet, other_community_id):
                        console.print(f"Кошелек {wallet} связан с кошельками из других сообществ (непрямая связь).")
                        break
                else:
                    console.print(f"[red]Кошелек {wallet} не соединен с кошельками из других сообществ.[/]")

def has_indirect_connection(graph, partition, start_wallet, target_community_id, visited=None):
    if visited is None:
        visited = set()

    visited.add(start_wallet)

    for neighbor in graph.neighbors(start_wallet):
        if neighbor not in visited and partition[neighbor] == target_community_id:
            return True
        elif neighbor not in visited:
            if has_indirect_connection(graph, partition, neighbor, target_community_id, visited):
                return True

    return False

if __name__ == "__main__":
    file_path = 'addresses.txt'
    addresses_from_file = [address.lower() for address in read_addresses_from_file(file_path)]
    global_graph = nx.Graph()
    for address in addresses_from_file:
        console.print(f"Анализ адреса: {address}")
        transactions = get_transactions_for_address(address)
        add_transactions_to_graph(global_graph, transactions)
    detect_communities(global_graph, addresses_from_file)
