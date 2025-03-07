import os
import time
import redis
from flask import Flask
from flask_socketio import SocketIO
from comms.Mapper import Mapper
import sys
sys.stdout.flush()

# Set environment variables inside Python script
os.environ["REDIS_DB_HOST"] = "10.203.12.106"
os.environ["REDIS_DB_PORT"] = "6379"
os.environ["REDIS_DB_PWD"] = "e87052bfcc0b65b2d0603ad4baa8d8ced7aa929b6698a568d2ce53dfd2dc04bcs"

# Initialize Flask & SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Redis Connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_DB_HOST"),
    port=int(os.getenv("REDIS_DB_PORT")),
    password=os.getenv("REDIS_DB_PWD"),
    decode_responses=True
)

# Initialize Mapper instances for P1, P2, P3
mpr_p1 = Mapper("P1")
mpr_p2 = Mapper("P2")
mpr_p3 = Mapper("P3")

def fetch_data_p1():
    """Fetch data from P1 and emit it via WebSocket."""
    # while True:
    value1, status, exception = mpr_p1.AllGather(modelLocal=None)
    if value1:
        print("P1 Data:", value1)
        redis_client.set("latest_sensor_data_p1", str(value1))
        socketio.emit("update_p1", value1)  # Emit to clients
        
        # time.sleep(1)

def fetch_data_p2():
    """Fetch data from P2 and emit it via WebSocket."""
    # while True:
    value2, status, exception = mpr_p2.AllGather(modelLocal=None)
    if value2:
        print("P2 Data:", value2)
        redis_client.set("latest_sensor_data_p2", str(value2))
        socketio.emit("update_p2", value2)  # Emit to clients
        
        # time.sleep(1)

def fetch_data_p3():
    """Fetch data from P3 and emit it via WebSocket."""
    # while True:
    value3, status, exception = mpr_p3.AllGather(modelLocal=None)
    if value3:
        print("P3 Data:", value3)
        redis_client.set("latest_sensor_data_p3", str(value3))
        socketio.emit("update_p3", value3)  # Emit to clients
        
        # time.sleep(1)
@socketio.on("refresh_data")
def handle_refresh():
    """Handles refresh requests from frontend."""
    print("Refreshing data...")
    fetch_data_p1()
    fetch_data_p2()
    fetch_data_p3()


@socketio.on("connect")
def on_connect():
    """Handle client connection and send the last known data."""
    print("Client connected")
    
    # Retrieve and send latest data from Redis
    latest_p1 = redis_client.get("latest_sensor_data_p1")
    if latest_p1:
        socketio.emit("update_p1", eval(latest_p1))

    latest_p2 = redis_client.get("latest_sensor_data_p2")
    if latest_p2:
        socketio.emit("update_p2", eval(latest_p2))

    latest_p3 = redis_client.get("latest_sensor_data_p3")
    if latest_p3:
        socketio.emit("update_p3", eval(latest_p3))

    # Start background tasks for each pipeline
    socketio.start_background_task(fetch_data_p1)
    socketio.start_background_task(fetch_data_p2)
    socketio.start_background_task(fetch_data_p3)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
