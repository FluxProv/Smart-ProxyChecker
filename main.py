import threading
import socket
import time
import colorama
from colorama import Fore, Style
import socks
import urllib.request
import json

colorama.init()

MAX_THREADS = 100

def check_proxy(proxy, test_url='http://www.google.com'):
    try:
        protocol, host, port = parse_proxy(proxy)
        if protocol == "http":
            proxy_handler = urllib.request.ProxyHandler({'http': f'{protocol}://{host}:{port}'})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
            with urllib.request.urlopen(test_url, timeout=5):
                return True
        elif protocol in ["socks4", "socks5"]:
            sock = socks.socksocket(socks.AF_INET, socks.SOCK_STREAM)
            sock.set_proxy(socks.SOCKS4 if protocol == "socks4" else socks.SOCKS5, host, int(port))
            sock.settimeout(5)
            sock.connect((host, int(port)))
            return True
    except Exception:
        return False

def parse_proxy(proxy):
    if '://' in proxy:
        protocol, address = proxy.split('://')
        host, port = address.split(':')
    else:
        protocol = "http"
        host, port = proxy.split(':')
    return protocol, host, port

def check_proxies_from_file(filename, test_url):
    working_proxies = []
    threads = []
    semaphore = threading.Semaphore(MAX_THREADS)
    with open(filename, 'r') as f:
        proxies = f.readlines()
    for proxy in proxies:
        semaphore.acquire()
        thread = threading.Thread(target=lambda p: check_proxy_in_thread(p, test_url, working_proxies, semaphore), args=(proxy,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return working_proxies

def check_proxy_in_thread(proxy, test_url, working_proxies, semaphore):
    if check_proxy(proxy, test_url):
        working_proxies.append(proxy)
    semaphore.release()

def print_working_proxies(working_proxies):
    if working_proxies:
        log_results(working_proxies)
        print(Fore.GREEN + f"Работающие прокси ({len(working_proxies)}): " + Style.RESET_ALL)
        for proxy in working_proxies:
            print(Fore.GREEN + f"  {proxy.strip()}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "К сожалению, ни один прокси не работает." + Style.RESET_ALL)

def log_results(working_proxies):
    with open('proxy_log.txt', 'a') as f:
        f.write(f"\nПроверка от {time.strftime('%Y-%m-%d %H:%M:%S')}:\n")
        for proxy in working_proxies:
            f.write(f"{proxy.strip()}\n")

def filter_proxies_by_country(proxies, country_code):
    filtered_proxies = []
    for proxy in proxies:
        if get_proxy_country(proxy) == country_code:
            filtered_proxies.append(proxy)
    return filtered_proxies

def get_proxy_country(proxy):
    try:
        url = f"http://ip-api.com/json/{proxy.split(':')[0]}"
        response = urllib.request.urlopen(url)
        data = json.load(response)
        return data['countryCode']
    except Exception:
        return None

def anonymize_proxy(proxy):
    try:
        protocol, host, port = parse_proxy(proxy)
        anonymized_proxy = f"{protocol}://anonymous:{port}@{host}"
        return anonymized_proxy
    except Exception:
        return None

def save_proxies(proxies, filename):
    with open(filename, 'w') as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")

def rotate_proxies(proxies, target_function, *args, **kwargs):
    for proxy in proxies:
        try:
            if check_proxy(proxy):
                target_function(proxy, *args, **kwargs)
        except Exception as e:
            print(Fore.RED + f"Ошибка с прокси {proxy}: {e}" + Style.RESET_ALL)

def main():
    print(Fore.GREEN + """
███████╗██╗░░░░░██╗░░░██╗██╗░░██╗
██╔════╝██║░░░░░██║░░░██║╚██╗██╔╝
█████╗░░██║░░░░░██║░░░██║░╚███╔╝░
██╔══╝░░██║░░░░░██║░░░██║░██╔██╗░
██║░░░░░███████╗╚██████╔╝██╔╝╚██╗
╚═╝░░░░░╚══════╝░╚═════╝░╚═╝░░╚═╝
""" + Style.RESET_ALL)
    
    while True:
        proxy_file = input(Fore.YELLOW + "Введите имя файла с прокси: " + Style.RESET_ALL)
        test_url = input(Fore.YELLOW + "Введите URL для проверки (нажмите Enter для использования Google): " + Style.RESET_ALL) or 'http://www.google.com'
        
        start_time = time.time()
        working_proxies = check_proxies_from_file(proxy_file, test_url)
        end_time = time.time()
        
        print(Fore.CYAN + f"Проверка завершена за {end_time - start_time:.2f} секунд." + Style.RESET_ALL)
        print_working_proxies(working_proxies)

        save_choice = input(Fore.YELLOW + "Сохранить работающие прокси в файл? (д/н): " + Style.RESET_ALL)
        if save_choice.lower() == 'д':
            save_file = input(Fore.YELLOW + "Введите имя файла для сохранения: " + Style.RESET_ALL)
            save_proxies(working_proxies, save_file)

        filter_choice = input(Fore.YELLOW + "Отфильтровать прокси по стране? (д/н): " + Style.RESET_ALL)
        if filter_choice.lower() == 'д':
            country_code = input(Fore.YELLOW + "Введите код страны (например, RU, US): " + Style.RESET_ALL)
            filtered_proxies = filter_proxies_by_country(working_proxies, country_code)
            print_working_proxies(filtered_proxies)

        anonymize_choice = input(Fore.YELLOW + "Анонимизировать прокси? (д/н): " + Style.RESET_ALL)
        if anonymize_choice.lower() == 'д':
            anonymized_proxies = [anonymize_proxy(proxy) for proxy in working_proxies if anonymize_proxy(proxy)]
            print(Fore.GREEN + "Анонимизированные прокси:" + Style.RESET_ALL)
            print_working_proxies(anonymized_proxies)

        choice = input(Fore.YELLOW + "Хотите проверить прокси ещё раз? (д/н): " + Style.RESET_ALL)
        if choice.lower() != 'д':
            break

if __name__ == '__main__':
    main()
