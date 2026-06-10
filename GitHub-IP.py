import socket

# 原始 GitHub 域名列表
domains = [
    "github.com",
    "gist.github.com",
    "api.github.com",
    "assets-cdn.github.com",
    "raw.githubusercontent.com",
    "gist.githubusercontent.com",
    "cloud.githubusercontent.com",
    "camo.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "avatars4.githubusercontent.com",
    "avatars5.githubusercontent.com",
    "avatars6.githubusercontent.com",
    "avatars7.githubusercontent.com",
    "avatars8.githubusercontent.com",
    "user-images.githubusercontent.com",
    "github.githubassets.com"
]

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"[!] 无法解析 {domain}: {e}")
        return None

def generate_hosts(domains):
    new_hosts = []
    for domain in domains:
        ip = resolve_domain(domain)
        if ip:
            new_hosts.append(f"{ip}\t{domain}")
    return new_hosts

def save_hosts(file_path, hosts_lines):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# GitHub Start\n")
        for line in hosts_lines:
            f.write(line + "\n")
        f.write("# GitHub End\n")
    print(f"[+] 新 hosts 文件已生成: {file_path}")

if __name__ == "__main__":
    hosts_lines = generate_hosts(domains)
    save_hosts("github_hosts.txt", hosts_lines)
