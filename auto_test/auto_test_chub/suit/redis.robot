*** Settings ***
Documentation    CHUB  Query  test suit.
...
...               Test query. 
Library           ../library/Query.py
Library           ../library/RedisOperation.py
Resource          ../resources/res_info_data.robot
Resource          ../resources/resources.robot
Suite Setup       Connect_to_redis

*** Test Cases ***
Query http url
	[Documentation]    query http url.
	Case_init          ${resources_path}/query.query          ${resources_path}/query.resp
	Set_query_url      ${http_url}
	Set_expect         0    0     1
	Send_query
	Get_cache_res_info     ${http_url}
