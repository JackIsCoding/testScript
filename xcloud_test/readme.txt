1.gbt是通用压测工具
2.go run http_client.go  "http://10.10.67.110:801/xcloud/hostquery?version=1&client_version=1.1.0&channel=test&seq=1001&host=aaa.com"  1
gslb发包工具，支持发送多个包
3../http_server_keepalive  :port time
桩程序，用于模拟后端接收请求并回包
4.xcloud_shub.py请求，模拟网关接入shub发包，具体用法参见mshub
