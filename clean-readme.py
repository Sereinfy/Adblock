import subprocess
import datetime
import pytz
import os
import requests
 # 获取上游白名单
url = "https://raw.githubusercontent.com/217heidai/adblockfilters/refs/heads/main/rules/white.txt"  # 要下载的文本文件的 URL
folder_name = "rules"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

response = requests.get(url)

if response.status_code == 200:
    file_path = os.path.join(folder_name, "white.txt")
    with open(file_path, "wb") as f:
        f.write(response.content)
    print(f"文件下载成功，保存在 {file_path}。")
else:
    print(f"下载失败，状态码：{response.status_code}")

# 提取规则计数
num_dns = subprocess.getoutput("sed -n 's/^! Blocked domains: //p' ./rules/adblockdns.txt")
num_adblock = subprocess.getoutput("sed -n 's/^! Blocked Filters: //p' ./rules/adblockfilters.txt")

# 获取当前时间并转换为北京时间
time = datetime.datetime.now(pytz.timezone('UTC'))
beijing_time = time.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

# 用提取的规则计数和当前时间更新README.md
subprocess.run(f"sed -i 's/^更新时间:.*/更新时间: {beijing_time} （北京时间） /g' README.md", shell=True)
subprocess.run(f"sed -i 's/^插件拦截规则数量.*/插件拦截规则数量: {num_adblock} /g' README.md", shell=True)
subprocess.run(f"sed -i 's/^DNS拦截规则数量.*/DNS拦截规则数量: {num_dns} /g' README.md", shell=True)

print("已成功更新README.md中的规则计数和时间")
