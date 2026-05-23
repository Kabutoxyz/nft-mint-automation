#!/usr/bin/env python3
"""
NFT Mint Automation - Collection Scanner
Checks NFT collection stats from OpenSea API
"""
import requests
import sys
from datetime import datetime

def get_collection_stats(slug):
    """Get collection stats from OpenSea"""
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data.get('collection', {}).get('stats', {})
            
            print(f"\n📊 Collection: {slug}")
            print(f"Floor Price: {stats.get('floor_price', 0):.4f} ETH")
            print(f"Total Supply: {stats.get('total_supply', 0):,}")
            print(f"Owners: {stats.get('num_owners', 0):,}")
            print(f"Volume (24h): {stats.get('one_day_volume', 0):.2f} ETH")
            print(f"Volume (7d): {stats.get('seven_day_volume', 0):.2f} ETH")
            print(f"Average Price: {stats.get('average_price', 0):.4f} ETH")
            
            # Calculate unique owner ratio
            supply = stats.get('total_supply', 1)
            owners = stats.get('num_owners', 0)
            if supply > 0:
                ratio = (owners / supply) * 100
                print(f"\n📈 Unique Owner Ratio: {ratio:.1f}%")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def search_collections(query):
    """Search for collections"""
    url = "https://api.opensea.io/api/v1/collections"
    params = {'offset': 0, 'limit': 5}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"\n🔍 Search Results for: {query}")
            print("-" * 40)
            for collection in data[:5]:
                name = collection.get('name', 'Unknown')
                slug = collection.get('slug', '')
                stats = collection.get('stats', {})
                floor = stats.get('floor_price', 0)
                print(f"  {name} ({slug}) - Floor: {floor:.4f} ETH")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print(f"🎨 NFT Mint Automation")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if len(sys.argv) > 1:
        collection = sys.argv[1]
        get_collection_stats(collection)
    else:
        # Default example
        get_collection_stats("boredapeyachtclub")
