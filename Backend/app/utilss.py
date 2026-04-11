import math
from scipy.spatial import KDTree
import numpy as np
from datetime import datetime, timedelta

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# For KD-Tree (fast nearest neighbor)
def build_kdtree(shops):
    coords = np.array([[s.lat, s.lon] for s in shops])
    return KDTree(coords), shops

def find_nearest_shops(user_lat, user_lon, shops, k=20):
    if not shops:
        return []
    tree, shop_list = build_kdtree(shops)
    distances, indices = tree.query([user_lat, user_lon], k=min(k, len(shop_list)))
    if isinstance(distances, float): distances = [distances]; indices = [indices]
    results = []
    for d, idx in zip(distances, indices):
        shop = shop_list[idx]
        results.append((shop, d))
    return results