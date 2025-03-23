import requests
import time
from google.cloud import pubsub_v1

PROJECT_ID = "vcc-assignment3"
TOPIC_NAME = "auto-scale-trigger"

def get_cpu_usage():
    """Fetch CPU usage from Prometheus using PromQL."""
    try:
        query = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
        response = requests.get(f"http://localhost:9090/api/v1/query?query={query}")

        if response.status_code != 200:
            print(f"❌ Prometheus API Error: {response.status_code}")
            return None

        data = response.json()
        if "data" in data and "result" in data["data"] and data["data"]["result"]:
            cpu_usage = float(data["data"]["result"][0]["value"][1])
            return cpu_usage
        else:
            print("⚠ No CPU usage data found in Prometheus API response.")
            return None

    except Exception as e:
        print(f"❌ Error fetching CPU usage: {e}")
        return None

def publish_message():
    """Publish a message to Google Cloud Pub/Sub to trigger scaling."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    publisher.publish(topic_path, b"Trigger Scaling")
    print("🔄 Scaling Trigger Sent to GCP")

while True:
    cpu_usage = get_cpu_usage()
    if cpu_usage is not None:
        print(f"✅ CPU Usage: {cpu_usage:.2f}%")
        if cpu_usage > 75:
            publish_message()
    else:
        print("⚠ Skipping scaling check due to missing CPU data.")
    
    time.sleep(10)
