import redis
import pickle
import zlib
import pandas as pd

# Connect to Redis
redis_host = "10.203.12.106"
redis_port = 6379
redis_password = "e87052bfcc0b65b2d0603ad4baa8d8ced7aa929b6698a568d2ce53dfd2dc04bcs"

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=False)

# Get all keys with "P1_key-value:"
keys = r.keys("P1_key-value:*")

if not keys:
    print("❌ No keys found in Redis.")
else:
    print(f"🔑 Retrieved {len(keys)} keys from Redis.")

    all_data = []

    for key in keys:
        try:
            # Retrieve compressed data
            compressed_data = r.get(key)
            
            if compressed_data is None:
                print(f"⚠️ Warning: Key {key} has no data, skipping...")
                continue

            # Decompress and deserialize
            data = pickle.loads(zlib.decompress(compressed_data))
            
            # Extract relevant fields
            all_data.append({
                "timestamp": key.decode().split(":")[-1],  # Extract timestamp from key
                "date": data.get("date", "N/A"),
                "time": data.get("time", "N/A"),
                "P1_PCV01D": data.get("State", {}).get("P1_PCV01D", None),
                "P1_PCV02D": data.get("State", {}).get("P1_PCV02D", None),
                "P1_PIT01": data.get("Measure", {}).get("P1_PIT01", None)
            })
        
        except Exception as e:
            print(f"❌ Error retrieving key {key}: {e}")

    if all_data:
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # Save to CSV
        df.to_csv("retrieved_data.csv", index=False)
        print("✅ Data successfully saved to retrieved_data.csv")

    else:
        print("❌ No valid data found.")
