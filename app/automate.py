import requests
import time

base_url = "http://flaskapp:5001"


def call_produce():
    """Trigger the produce API to start producing Kafka messages."""
    print("Calling produce API...")
    response = requests.get(f"{base_url}/produce")
    print("Produce API Response:", response.json())


def call_consume():
    print("Calling consume API...")
    """Continuously call consume API until it indicates 'explicit stop'."""
    while True:
        response = requests.get(f"{base_url}/consume")
        if response.status_code == 200:
            data = response.json()
            print("Consume API Response:", data)
            if data.get("message") == "explicit stop":
                print("Received explicit stop from consume API.")
                break
        else:
            print("Error with consume API:", response.json())
            break


def call_attack():
    print("Calling attack API...")
    """Trigger the attack API after all data has been consumed."""
    response = requests.get(f"{base_url}/attack")
    print("Attack API Response:", response.json())

def generate_report():
    print('Generating report....')
    """Create a bar chart and save it"""
    response = requests.get(f"{base_url}/report")
    print("Attack API Response:", response.json())


def main():
    print("Starting API Automation...")
    call_produce()
    call_consume()
    call_attack()

    print("API Automation Completed.")


if __name__ == "__main__":
    main()
