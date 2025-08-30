#!/bin/bash

# 获取 CPU 支持的特性，并转换为小写以避免大小写匹配问题
cpu_flags=$(cat /proc/cpuinfo | grep -m 1 'flags' | cut -d: -f2 | tr '[:upper:]' '[:lower:]')

# 定义各版本的特性集合
v1_flags="cmov cx8 fpu fxsr mmx osfxsr sce sse sse2"
v2_flags="cmpxchg16b lafh-sahf popcnt sse3 sse4_1 sse4_2 ssse3"
v3_flags="avx avx2 bmi1 bmi2 f16c fma lzcnt movbe osxsave"
v4_flags="avx512f avx512bw avx512cd avx512dq avx512vl"

# 用于保存检测到的特性
detected_v1=""
detected_v2=""
detected_v3=""
detected_v4=""

# 检查并列出支持的特性
for flag in $v1_flags; do
    if [[ $cpu_flags == *$flag* ]]; then
        detected_v1="$detected_v1 $flag"
    fi
done

for flag in $v2_flags; do
    if [[ $cpu_flags == *$flag* ]]; then
        detected_v2="$detected_v2 $flag"
    fi
done

for flag in $v3_flags; do
    if [[ $cpu_flags == *$flag* ]]; then
        detected_v3="$detected_v3 $flag"
    fi
done

for flag in $v4_flags; do
    if [[ $cpu_flags == *$flag* ]]; then
        detected_v4="$detected_v4 $flag"
    fi
done

# 输出检测结果
if [[ -n "$detected_v1" ]]; then
    echo "v1: $detected_v1"
else
    echo "v1: No v1 features detected"
fi

if [[ -n "$detected_v2" ]]; then
    echo "v2: $detected_v2"
else
    echo "v2: No v2 features detected"
fi

if [[ -n "$detected_v3" ]]; then
    echo "v3: $detected_v3"
else
    echo "v3: No v3 features detected"
fi

if [[ -n "$detected_v4" ]]; then
    echo "v4: $detected_v4"
else
    echo "v4: No v4 features detected"
fi
