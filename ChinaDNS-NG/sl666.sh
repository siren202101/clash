# 获取 chnroute 集合中的 IP 地址数量
chnroute_ip_count=$(nft list set inet global chnroute | grep -Eo '(\d+\.\d+\.\d+\.\d+)' | wc -l)
echo "chnroute 集合中包含 $chnroute_ip_count 个 IPv4 地址。"

# 获取 chnroute6 集合中的 IP 地址数量
chnroute6_ip_count=$(nft list set inet global chnroute6 | grep -Eo '([0-9a-fA-F:]+)' | wc -l)
echo "chnroute6 集合中包含 $chnroute6_ip_count 个 IPv6 地址。"
