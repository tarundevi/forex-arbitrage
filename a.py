import requests
import math

class Graph:
    def __init__(self, vertices, index_to_currency):
        self.V = vertices  # Number of vertices (currencies)
        self.graph = []  # List to store graph edges
        self.index_to_currency = index_to_currency  # Map indices to currency names

    # Function to add an edge to the graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # Utility function to print the negative weight cycle and its weight, with exchange rates
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

        # Print the exchange rates for each step in the cycle
        self.printExchangeRates(cycle)

    def printExchangeRates(self, cycle):
        print("Exchange rates for the negative cycle:")
        for i in range(len(cycle) - 1):
            u = cycle[i]
            v = cycle[i + 1]
            currency_u = self.index_to_currency[u]
            currency_v = self.index_to_currency[v]

            # Find the weight for the edge u -> v
            for edge_u, edge_v, weight in self.graph:
                if edge_u == u and edge_v == v:
                    exchange_rate = math.exp(-weight)  # Convert negative log weight back to exchange rate
                    print(f"{currency_u} -> {currency_v}: 1 {currency_u} = {exchange_rate:.6f} {currency_v}")
                    break

    def BellmanFord(self, src):
        # Initialize distances from src to all other vertices as infinite
        dist = [float("Inf")] * self.V
        parent = [-1] * self.V  # Array to store the parent of each vertex
        dist[src] = 0

        # Relax all edges |V| - 1 times
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
                return  # Exit after finding one cycle

        # Print all distances if there is no negative weight cycle
        self.printArr(dist)

    # Utility function used to print the solution
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(self.index_to_currency[i], dist[i]))


# Function to retrieve exchange rates for selected currencies and build the complete graph
def buildGraphForSelectedCurrencies(api_key, selected_currencies):
    # Step 1: Map currency names to indices for the graph
    currency_to_index = {currency: idx for idx, currency in enumerate(selected_currencies)}
    index_to_currency = {idx: currency for currency, idx in currency_to_index.items()}
    num_currencies = len(selected_currencies)

    # Initialize the graph
    g = Graph(num_currencies, index_to_currency)

    # Step 2: Make API calls for each selected currency and add directed edges in both directions
    for base_currency in selected_currencies:
        # Fetch exchange rates with base as `base_currency`
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()

        if "conversion_rates" not in data:
            print(f"Error fetching data for base currency {base_currency}")
            continue

        rates = data["conversion_rates"]

        # Add edges for this base currency only for selected target currencies
        for target_currency, rate in rates.items():
            if target_currency != base_currency and target_currency in selected_currencies:
                # Calculate the weight as the negative log of the rate
                weight_direct = math.log(rate)
                weight_reverse = math.log(1 / rate)

                # Add both directed edges to the graph
                u = currency_to_index[base_currency]
                v = currency_to_index[target_currency]
                g.addEdge(u, v, weight_direct)
                g.addEdge(v, u, weight_reverse)

    return g, currency_to_index


# Main function
if __name__ == "__main__":
    api_key = "API-KEY"  # Replace with your actual API key

    # Ask user to specify which currencies to include
    selected_currencies = input("Enter the currencies to include (comma-separated, e.g., USD,EUR,JPY): ").split(",")
    selected_currencies = [currency.strip().upper() for currency in selected_currencies]  # Clean and format input

    # Build graph only for selected currencies
    g, currency_to_index = buildGraphForSelectedCurrencies(api_key, selected_currencies)

    # Run Bellman-Ford from the first currency in the list (you can change this)
    if selected_currencies[0] in currency_to_index:
        g.BellmanFord(currency_to_index[selected_currencies[0]])
    else:
        print(f"{selected_currencies[0]} not found in currency index")
