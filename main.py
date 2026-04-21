from serpapi import GoogleSearch
from urllib.parse import urlparse
import sys
import os
import ctypes

def get_domains_from_serpapi(query, location="Hanoi, Vietnam", hl="vi", gl="vn", google_domain="google.com.vn", api_key="d7b14c71aee0bade7ac6c0358c845315c94d27ab53539ea7d39ee1a2d8cf2468"):
    params = {
        "q": query,
        "location": location,
        "hl": hl,
        "gl": gl,
        "google_domain": google_domain,
        "api_key": api_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    domains = []
    if "organic_results" in results:
        for item in results["organic_results"]:
            if "link" in item:
                link = item["link"]
                domain = urlparse(link).netloc.strip()
                domains.append(domain)
    return domains

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def quang():
    if not is_admin():
        print("Script is asking for admin permit......")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

quang()

while True:
    try:
        query = input("Input search (CTRL + C to exit): ")
        search_results = list(set(get_domains_from_serpapi(query)))
        print("Results search:")
        for i in range(0, len(search_results), 3):
            print(*search_results[i:i+3], sep='           ')  

        pathToHostsFile = r"C:\Windows\System32\Drivers\etc\hosts"

        with open(pathToHostsFile, 'r', encoding='utf-8') as file:
            existing_lines = file.readlines()
        existing_entries = [line.strip() for line in existing_lines]

        with open(pathToHostsFile, 'a', encoding='utf-8') as file:
            for domain in search_results:
                entry = f"127.0.0.1       {domain}"
                if entry not in existing_entries:
                    file.write(entry + "\n")

        print(f"\nTHE DATA HAS BEEN LOGGED {pathToHostsFile}.")
        print(f"ALL THE WEBSITE HAS BEEN BLOCKED!!!")
        input("Press Enter to continue...\n----------------------------------------")
        # os.system('cls' if os.name == 'nt' else 'clear')
    except PermissionError:
        print("ERROR: No administrator permission!")
    except KeyboardInterrupt:
        print("\nExit requested by user.")
        sys.exit()
    except Exception as e:
        print(f"ERROR: Unknown error - {e}")
