# Ethereum Address Network Analysis

This Python script utilizes the Ethereum blockchain data to perform network analysis on a set of Ethereum addresses. It retrieves transaction information from the Etherscan API, builds a network graph based on transactions, detects communities within the graph using the Louvain method, and identifies cross-community connections.

## Dependencies

Make sure to install the following Python packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## Usage

1. **Obtain Etherscan API Key:**
   - Obtain an API key from [Etherscan API](https://etherscan.io/apis).
   - Save your API key in the `etherscan_api_key` variable within the script.

2. **Prepare Addresses File:**
   - Create a file named `addresses.txt`.
   - Add Ethereum addresses (one per line) for analysis.

3. **Run the Script:**

   ```
   python ethereum_network_analysis.py
   ```

Feel free to explore and modify the script based on your specific needs.