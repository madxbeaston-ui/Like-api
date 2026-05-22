import requests
import json
import time

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"
API_URL = "https://xtytdtyj-jwt.up.railway.app/token"

# Har 4 hour baad update
UPDATE_INTERVAL = 4 * 60 * 60


def read_uidpass():
    with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_token(uid, password):
    url = f"{API_URL}?uid={uid}&password={password}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        token = data.get("token")

        if token:
            print(f"[✓] Token generated for UID: {uid}")
            return token
        else:
            print(f"[X] No token received for UID: {uid}")
            return None

    except Exception as e:
        print(f"[X] Error fetching token for UID {uid}: {e}")
        return None


def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, ensure_ascii=False, indent=4)


def generate_all_tokens():
    print("\n[+] Updating tokens.json ...")

    uidpass_list = read_uidpass()
    new_tokens = []

    for item in uidpass_list:
        uid = item.get("uid")
        password = item.get("password")

        if not uid or not password:
            continue

        token = fetch_token(uid, password)

        if token:
            new_tokens.append({
                "token": token
            })

    if new_tokens:
        update_token_file(new_tokens)
        print(f"[✓] tokens.json updated with {len(new_tokens)} tokens")
    else:
        print("[X] No valid tokens generated")


def main():
    while True:
        try:
            generate_all_tokens()

        except Exception as e:
            print(f"[X] Main loop error: {e}")

        print(f"\n[+] Sleeping for 4 hours...\n")
        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    main()
