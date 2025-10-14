import re
import subprocess
import time
from prometheus_client import start_http_server, Gauge

# Создание метрик
unbound_metrics = {
    "total_queries": Gauge("unbound_total_queries", "Общее количество запросов, обработанных Unbound"),
    "cache_hits": Gauge("unbound_cache_hits", "Количество запросов, обслуженных из кеша"),
    "cache_misses": Gauge("unbound_cache_misses", "Количество запросов, не обслуженных из кеша"),
    "queries_ip_ratelimited": Gauge("unbound_queries_ip_ratelimited", "Количество запросов, ограниченных по IP"),
    "prefetch": Gauge("unbound_prefetch", "Количество запросов на предварительную выборку"),
    "expired": Gauge("unbound_expired", "Количество запросов с истекшим сроком действия"),
    "recursive_replies": Gauge("unbound_recursive_replies", "Количество рекурсивных ответов"),
    # Метрики для типов запросов
    "query_type_A": Gauge("unbound_query_type_A", "Количество запросов типа A"),
    "query_type_PTR": Gauge("unbound_query_type_PTR", "Количество запросов типа PTR"),
    "query_type_TXT": Gauge("unbound_query_type_TXT", "Количество запросов типа TXT"),
    "query_type_AAAA": Gauge("unbound_query_type_AAAA", "Количество запросов типа AAAA"),
    "query_type_SVCB": Gauge("unbound_query_type_SVCB", "Количество запросов типа SVCB"),
    "query_type_HTTPS": Gauge("unbound_query_type_HTTPS", "Количество запросов типа HTTPS"),
    "query_type_ANY": Gauge("unbound_query_type_ANY", "Количество запросов типа ANY"),
    # Лимитирование запросов
    "queries_tcp": Gauge("unbound_queries_tcp", "Количество запросов, обслуженных по TCP"),
    "queries_tls": Gauge("unbound_queries_tls", "Количество запросов, обслуженных по TLS"),
    "queries_dnscrypt": Gauge("unbound_queries_dnscrypt", "Количество запросов через DNSCrypt"),
    # Статистика по кодам ответов
    "rcode_noerror": Gauge("unbound_rcode_noerror", "Ответы без ошибок"),
    "rcode_servfail": Gauge("unbound_rcode_servfail", "Ошибки сервера"),
    "rcode_nxdomain": Gauge("unbound_rcode_nxdomain", "Ответы, где домен не существует"),
    "rcode_refused": Gauge("unbound_rcode_refused", "Отказано в обслуживании"),
    "rcode_formerr": Gauge("unbound_rcode_formerr", "Ошибки формата"),
    # Метрики кэша
    "msg_cache_count": Gauge("unbound_msg_cache_count", "Количество записей в кэше сообщений"),
    "rrset_cache_count": Gauge("unbound_rrset_cache_count", "Количество записей в кэше ресурсов (RRSet)"),
    "infra_cache_count": Gauge("unbound_infra_cache_count", "Количество записей инфраструктурного кэша"),
    "key_cache_count": Gauge("unbound_key_cache_count", "Количество записей в кэше ключей DNSSEC"),
    # Использование памяти
    "mem_cache_rrset": Gauge("unbound_mem_cache_rrset", "Память, занятая кэшем RRSet"),
    "mem_cache_message": Gauge("unbound_mem_cache_message", "Память, занятая кэшем сообщений"),
    "mem_mod_iterator": Gauge("unbound_mem_mod_iterator", "Память, используемая итератором"),
    "mem_mod_validator": Gauge("unbound_mem_mod_validator", "Память, занятая валидатором DNSSEC"),
    "mem_streamwait": Gauge("unbound_mem_streamwait", "Память для ожидающих запросов"),
    # Статистика по DNSSEC
    "num_answer_secure": Gauge("unbound_num_answer_secure", "Количество ответов, подписанных DNSSEC"),
    "num_answer_bogus": Gauge("unbound_num_answer_bogus", "Ответы с недействительными DNSSEC-подписями"),
    "num_rrset_bogus": Gauge("unbound_num_rrset_bogus", "Количество некорректных RRSet с DNSSEC"),
    # Статистика потоков
    "thread_queries": Gauge("unbound_thread_queries", "Запросы, обработанные потоками"),
    "thread_cachehits": Gauge("unbound_thread_cachehits", "Количество кэш-хитов потоков"),
    "thread_recursivereplies": Gauge("unbound_thread_recursivereplies", "Количество рекурсивных ответов потоков"),
    # Дополнительно
    "unwanted_queries": Gauge("unbound_unwanted_queries", "Количество нежелательных запросов"),
    "unwanted_replies": Gauge("unbound_unwanted_replies", "Количество нежелательных ответов"),
    "zero_ttl": Gauge("unbound_zero_ttl", "Ответы с нулевым TTL"),
    "query_subnet": Gauge("unbound_query_subnet", "Количество запросов с использованием EDNS Client Subnet")
}

# Регулярное выражение для извлечения данных из логов
log_pattern = r"(\d{10})\] unbound\[\d+:\d+\] info: (\d+\.\d+\.\d+\.\d+) (\S+) (\S+) IN(?: (\S+) (\S+) (\S+))?"

# Функция для парсинга логов
def parse_logs(logs):
    parsed_data = []
    for log in logs:
        match = re.search(log_pattern, log)
        if match:
            timestamp = match.group(1)
            ip_address = match.group(2)
            domain_name = match.group(3)
            query_type = match.group(4)
            error = match.group(5) if match.group(5) else 'NOERROR'
            response_time = match.group(6) if match.group(6) else '0.000000'
            other_data = match.group(7) if match.group(7) else None
            parsed_data.append({
                "timestamp": timestamp,
                "ip_address": ip_address,
                "domain_name": domain_name,
                "query_type": query_type,
                "error": error,
                "response_time": response_time,
                "other_data": other_data
            })
    return parsed_data

# Функция для получения данных из файла лога
def read_log_file(file_path):
    with open(file_path, "r") as file:
        return file.readlines()

# Функция для получения статистики из unbound-control
def fetch_unbound_stats():
    try:
        result = subprocess.run(
            "unbound-control stats", 
            capture_output=True, text=True, shell=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды unbound-control: {e}")
        return None

# Функция для парсинга статистики
def parse_stats(stats_output):
    if not stats_output:
        return {}
    
    stats = {}
    for line in stats_output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            try:
                stats[key] = float(value.strip())
            except ValueError:
                pass
    return stats

# Функция для обновления метрик Prometheus
def update_metrics():
    stats_output = fetch_unbound_stats()
    if stats_output:
        stats = parse_stats(stats_output)
        
        # Обновляем метрики для общего количества запросов, кэш-хитов, кэш-промахов и т.д.
        unbound_metrics["total_queries"].set(stats.get("total.num.queries", 0))
        unbound_metrics["cache_hits"].set(stats.get("total.num.cachehits", 0))
        unbound_metrics["cache_misses"].set(stats.get("total.num.cachemiss", 0))
        unbound_metrics["queries_ip_ratelimited"].set(stats.get("total.num.queries.ip_ratelimited", 0))
        unbound_metrics["prefetch"].set(stats.get("total.num.prefetch", 0))
        unbound_metrics["expired"].set(stats.get("total.num.expired", 0))
        unbound_metrics["recursive_replies"].set(stats.get("total.num.recursive_replies", 0))
        
        # Метрики для типов запросов
        unbound_metrics["query_type_A"].set(stats.get("total.num.queries.A", 0))
        unbound_metrics["query_type_PTR"].set(stats.get("total.num.queries.PTR", 0))
        unbound_metrics["query_type_TXT"].set(stats.get("total.num.queries.TXT", 0))
        unbound_metrics["query_type_AAAA"].set(stats.get("total.num.queries.AAAA", 0))
        unbound_metrics["query_type_SVCB"].set(stats.get("total.num.queries.SVCB", 0))
        unbound_metrics["query_type_HTTPS"].set(stats.get("total.num.queries.HTTPS", 0))
        unbound_metrics["query_type_ANY"].set(stats.get("total.num.queries.ANY", 0))
        
        # Лимитирование запросов
        unbound_metrics["queries_tcp"].set(stats.get("total.num.queries.tcp", 0))
        unbound_metrics["queries_tls"].set(stats.get("total.num.queries.tls", 0))
        unbound_metrics["queries_dnscrypt"].set(stats.get("total.num.queries.dnscrypt", 0))
        
        # Статистика по кодам ответов
        unbound_metrics["rcode_noerror"].set(stats.get("total.num.rcodes.NOERROR", 0))
        unbound_metrics["rcode_servfail"].set(stats.get("total.num.rcodes.SERVFAIL", 0))
        unbound_metrics["rcode_nxdomain"].set(stats.get("total.num.rcodes.NXDOMAIN", 0))
        unbound_metrics["rcode_refused"].set(stats.get("total.num.rcodes.REFUSED", 0))
        unbound_metrics["rcode_formerr"].set(stats.get("total.num.rcodes.FORMERR", 0))
        
        # Метрики кэша
        unbound_metrics["msg_cache_count"].set(stats.get("cache.num.msgcache", 0))
        unbound_metrics["rrset_cache_count"].set(stats.get("cache.num.rrsetcache", 0))
        unbound_metrics["infra_cache_count"].set(stats.get("cache.num.infracache", 0))
        unbound_metrics["key_cache_count"].set(stats.get("cache.num.keycache", 0))
        
        # Использование памяти
        unbound_metrics["mem_cache_rrset"].set(stats.get("memory.cache.rrset", 0))
        unbound_metrics["mem_cache_message"].set(stats.get("memory.cache.msg", 0))
        unbound_metrics["mem_mod_iterator"].set(stats.get("memory.module.iterator", 0))
        unbound_metrics["mem_mod_validator"].set(stats.get("memory.module.validator", 0))
        unbound_metrics["mem_streamwait"].set(stats.get("memory.module.streamwait", 0))
        
        # Статистика по DNSSEC
        unbound_metrics["num_answer_secure"].set(stats.get("security.num.secure", 0))
        unbound_metrics["num_answer_bogus"].set(stats.get("security.num.bogus", 0))
        unbound_metrics["num_rrset_bogus"].set(stats.get("security.num.rrsetbogus", 0))
        
        # Статистика потоков
        unbound_metrics["thread_queries"].set(stats.get("threads.num.queries", 0))
        unbound_metrics["thread_cachehits"].set(stats.get("threads.num.cachehits", 0))
        unbound_metrics["thread_recursivereplies"].set(stats.get("threads.num.recursivereplies", 0))
        
        # Дополнительно
        unbound_metrics["unwanted_queries"].set(stats.get("total.num.unwanted.queries", 0))
        unbound_metrics["unwanted_replies"].set(stats.get("total.num.unwanted.replies", 0))
        unbound_metrics["zero_ttl"].set(stats.get("total.num.zero.ttl", 0))
        unbound_metrics["query_subnet"].set(stats.get("total.num.query.subnet", 0))

# Главная функция
def main():
    # # Чтение логов из файла
    # log_data = read_log_file("/var/log/unbound/unbound.log")
    # parsed_logs = parse_logs(log_data)
    
    # for entry in parsed_logs:
    #     print(entry)  # Вывод распарсенных данных лога

    # # Запускаем сервер для Prometheus на порту 9100
    # start_http_server(9100)
    # print("Сервер Prometheus запущен на порту 9100.")

    # # Обновление метрик каждую минуту
    # while True:
    #     update_metrics()
    #     time.sleep(60)

    # Чтение логов из файла
    log_data = read_log_file("/var/log/unbound/unbound.log")
    parsed_logs = parse_logs(log_data)
    
    # Выводим данные лога
    print("Содержимое логов:")
    for entry in parsed_logs:
        print(entry)  # Вывод распарсенных данных лога

    # Запускаем сервер для Prometheus на порту 9100
    start_http_server(9100)
    print("Сервер Prometheus запущен на порту 9100.")

    # Обновление метрик каждую минуту
    while True:
        update_metrics()
        print("\nОбновленные метрики:")
        for metric_name, metric in unbound_metrics.items():
            print(f"{metric_name}: {metric._value}")
        time.sleep(60)

if __name__ == "__main__":
    main()
