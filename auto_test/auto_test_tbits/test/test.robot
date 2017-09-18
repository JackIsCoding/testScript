*** settings ***
Documentation  Try test suit.
Library        ../library/DatabaseOperation.py
Library        ../library/RedisOperation.py
Suite Setup     Connect To Database
Suite Teardown  Disconnect From Database
Test Timeout      10 seconds

*** Test Cases ***
#Test 1
#	execute_sql_string      show databases
#	get_full_table          bcid_info                    59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607
#	get_full_table          server_res                   59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607
#	get_full_table          gcid_info                    96C32F6962A450C3F213C9FEFA03666AEC30854D
#
#Test 4
#	select_gcid_info        96C32F6962A450C3F213C9FEFA03666AEC30854D         6201259
#	select_bcid_info        59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607
#	select_res_info         http://redirected_1.url.com/test.flv
#	select_server_res       59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607         http://redirected_1.url.com/test.flv
#
Test 5
	Connect To Redis
	get_dc_bcid_info           E75B0BFE0B70F63ACA859E102C0B4188683C7ADB 
	get_dc_res_info            http://cdn.amazeui.org/src/2.0/dist/AmazeUI-2.1.0-beta1.zip
	get_cn_bcid_info           E75B0BFE0B70F63ACA859E102C0B4188683C7ADB
	get_cn_res_info_url        http://cdn.amazeui.org/src/2.0/dist/AmazeUI-2.1.0-beta1.zip 
	get_cn_res_info_cid        708ADEF83259B6CE2D79B6EF6D8AE4EA026F7DDE
	get_cn_server_res          E75B0BFE0B70F63ACA859E102C0B4188683C7ADB
#	del_dc_bcid_info           59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607
#	del_dc_res_info            http://redirected_1.url.com/test.flv
	del_cn_bcid_info           59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607
	del_cn_res_info_url        http://redirected_1.url.com/test.flv
	del_cn_res_info_cid        96C32F6962A450C3F213C9FEFA03666AEC30854D
	del_cn_server_res          59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607 

Test 6
	delete_all_res          59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607          96C32F6962A450C3F213C9FEFA03666AEC30854D             6201259          http://redirected_1.url.com/test.flv
	delete_all_res          59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607          96C32F6962A450C3F213C9FEFA03666AEC30854D             6201259          http://original_1.url.com/test.flv 
	delete_all_res          4E5089001F4C3E85E611413D148695A2D4555D4D          DAA36ED006AA89E2BF9FFD4E26D41A2411DEBC7F           7700114684         http://dota2.dl.wanmei.com/dota2/client/DOTA2Setup20141125.zip
	delete_all_redis        http://redirected_1.url.com/test.flv            59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607          96C32F6962A450C3F213C9FEFA03666AEC30854D
	delete_all_redis        http://xmp.down.sandai.net/kankan/XMPSetup_8.8.888888-7.9.9.9.exe       59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607          96C32F6962A450C3F213C9FEFA03666AEC30854D
	delete_all_res          59A49B62E1AFAFB01C6879B8CDE53A0ACBBCD607          96C32F6962A450C3F213C9FEFA03666AEC30854D             6201259          http://xmp.down.sandai.net/kankan/XMPSetup_8.8.888888-7.9.9.9.exe

Test 7
#	select_res_info         http://cdn.amazeui.org/src/2.0/dist/AmazeUI-2.1.0-beta1.zip
#	select_gcid_info        708ADEF83259B6CE2D79B6EF6D8AE4EA026F7DDE        932912
	delete_bcid_info        E75B0BFE0B70F63ACA859E102C0B4188683C7ADB
#	select_server_res       E75B0BFE0B70F63ACA859E102C0B4188683C7ADB        http://cdn.amazeui.org/src/2.0/dist/AmazeUI-2.1.0-beta1.zip
	delete_all_res          E75B0BFE0B70F63ACA859E102C0B4188683C7ADB        708ADEF83259B6CE2D79B6EF6D8AE4EA026F7DDE        932912           http://cdn.amazeui.org/src/2.0/dist/AmazeUI-2.1.0-beta1.zip
	delete_all_res          E75B0BFE0B70F63ACA859E102C0B4188683C7ADB        708ADEF83259B6CE2D79B6EF6D8AE4EA026F7DDE        932912           http://original_1.url.com/test.flv
	delete_all_res          E75B0BFE0B70F63ACA859E102C0B4188683C7ADB        708ADEF83259B6CE2D79B6EF6D8AE4EA026F7DDE        932912           http://xmp.down.sandai.net/kankan/XMPSetup_8.8.888888-7.9.9.9.exe
	delete_all_server_res   E75B0BFE0B70F63ACA859E102C0B4188683C7ADB
#	delete_all_res         846ACA4CC5A6490766CFC9E718080490CE7F20D5         C2CE5944920EE94248D705A4251D77DBFA4BA54E        547222305        http://test_result.not.exist/query_url/res_info.rar
	select_res_info        http://test_result.not.exist/query_url/res_info.rar
