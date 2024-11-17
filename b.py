import requests
import math

class Graph:
    def __init__(self, vertices, index_to_currency):
        self.V = vertices  
        self.graph = []  
        self.index_to_currency = index_to_currency  

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def printNegativeCycle(self, parent, start):
        cycle = []
        cycle_weight = 0
        current = start
        visited = set()

        # Traverse the parent chain to get the cycle
        while current not in visited:
            visited.add(current)
            cycle.append(current)  # Append currency index
            prev = parent[current]
            # Find the edge weight from prev to current
            for u, v, w in self.graph:
                if u == prev and v == current:
                    cycle_weight += w
                    break
            current = prev

        # Backtrack to find the actual start of the cycle
        cycle_start = current
        cycle = cycle[cycle.index(cycle_start):] + [cycle_start]  # Complete the cycle

        # Print the cycle and its total weight
        print("Negative weight cycle found:", " -> ".join(self.index_to_currency[idx] for idx in cycle))
        print("Weight of the cycle:", cycle_weight)

        # Print the exchange rates and simulate the currency conversion
        self.printExchangeRates(cycle)

    def printExchangeRates(self, cycle):
        print("Exchange rates and value progression for the negative cycle:")
        initial_value = 1.0  
        value = initial_value

        for i in range(len(cycle) - 1):
            u = cycle[i]
            v = cycle[i + 1]
            currency_u = self.index_to_currency[u]
            currency_v = self.index_to_currency[v]

            # Find the weight for the edge u -> v
            for edge_u, edge_v, weight in self.graph:
                if edge_u == u and edge_v == v:
                    exchange_rate = math.exp(-weight)  
                    value *= exchange_rate  
                    print(f"{currency_u} -> {currency_v}: 1 {currency_u} = {exchange_rate:.6f} {currency_v} | Value now: {value:.6f} {currency_v}")
                    break


        final_currency = self.index_to_currency[cycle[0]]
        print(f"\nStarting with 1 {final_currency}, after completing the cycle, we end up with: {value:.6f} {final_currency}")

    def BellmanFord(self, src):
        dist = [float("Inf")] * self.V
        parent = [-1] * self.V  
        dist[src] = 0

        
        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u

        # Check for negative-weight cycles
        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graph contains a negative weight cycle.")
                self.printNegativeCycle(parent, v)
                return 

        
        self.printArr(dist)

    
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(self.index_to_currency[i], dist[i]))



def buildGraphForSelectedCurrencies(api_key, selected_currencies):
    currency_to_index = {currency: idx for idx, currency in enumerate(selected_currencies)}
    index_to_currency = {idx: currency for currency, idx in currency_to_index.items()}
    num_currencies = len(selected_currencies)

    
    g = Graph(num_currencies, index_to_currency)

    
    for base_currency in selected_currencies:
    
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()

        if "conversion_rates" not in data:
            print(f"Error fetching data for base currency {base_currency}")
            continue

        rates = data["conversion_rates"]


        for target_currency, rate in rates.items():
            if target_currency != base_currency and target_currency in selected_currencies:

                weight_direct = -math.log(rate)
                weight_reverse = math.log(rate)
                u = currency_to_index[base_currency]
                v = currency_to_index[target_currency]
                g.addEdge(u, v, weight_direct)
                g.addEdge(v, u, weight_reverse)

    return g, currency_to_index



if __name__ == "__main__":
    api_key = "API_KEY"  


    selected_currencies = input("Enter the currencies to include (comma-separated, e.g., USD,EUR,JPY): ").split(",")
    selected_currencies = [currency.strip().upper() for currency in selected_currencies] 

    
    g, currency_to_index = buildGraphForSelectedCurrencies(api_key, selected_currencies)

    
    if selected_currencies[0] in currency_to_index:
        g.BellmanFord(currency_to_index[selected_currencies[0]])
    else:
        print(f"{selected_currencies[0]} not found in currency index")
