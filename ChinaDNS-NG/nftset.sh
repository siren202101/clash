#!/bin/sh

echo "===== 初始化 nftables 规则 ====="

# 确保 nftables 运行
# opkg update
# opkg install nftables

# service nftables enable
# service nftables start

# 检测 inet global 规则表是否存在，存在则先删除
nft list table inet global >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "删除已有的 inet global 规则表..."
    nft delete table inet global
fi

# 重新创建 inet global 规则表
echo "创建新的 inet global 规则表..."
nft add table inet global

# 定义要创建的 IPv4 和 IPv6 集合
IPV4_SETS="global_black global_white global_vps global_gfw chnroute"
IPV6_SETS="global_black6 global_white6 global_vps6 global_gfw6 chnroute6"

# 处理 IPv4 集合
for set in $IPV4_SETS; do
    echo "创建 IPv4 集合: $set"
    nft add set inet global "$set" '{ type ipv4_addr; flags interval; timeout 1h; }'
done

# 处理 IPv6 集合
for set in $IPV6_SETS; do
    echo "创建 IPv6 集合: $set"
    nft add set inet global "$set" '{ type ipv6_addr; flags interval; timeout 1h; }'
done

# 加载 chnroute.nftset 规则（删除已有集合后重新加载）
if [ -f "/root/chinadns_ng/chnroute.nftset" ]; then
    echo "检查 chnroute 集合是否存在并删除..."
    # 删除已有的 chnroute 集合
    nft delete set inet global chnroute 2>/dev/null
    echo "加载 chnroute.nftset 规则..."
    nft -f /root/chinadns_ng/chnroute.nftset
else
    echo "警告: chnroute.nftset 文件未找到，跳过加载。"
fi

# 加载 chnroute6.nftset 规则（删除已有集合后重新加载）
if [ -f "/root/chinadns_ng/chnroute6.nftset" ]; then
    echo "检查 chnroute6 集合是否存在并删除..."
    # 删除已有的 chnroute6 集合
    nft delete set inet global chnroute6 2>/dev/null
    echo "加载 chnroute6.nftset 规则..."
    nft -f /root/chinadns_ng/chnroute6.nftset
else
    echo "警告: chnroute6.nftset 文件未找到，跳过加载。"
fi

# 等待 15 秒钟
sleep 15

# 执行 chinadns-ng
echo "启动 chinadns-ng..."
/usr/bin/chinadns-ng -C /root/chinadns_ng/chinadns_ng.conf

echo "===== nftables 规则初始化完成，chinadns-ng 启动完成！====="
