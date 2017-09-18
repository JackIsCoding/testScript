*** Settings ***
Documentation     Res info data.

*** Variables ***
${thunder_url}               http://thunder.qvcd.net/C2CE5944920EE94248D705A4251D77DBFA4BA54E/【Qvcd电影www.qvcd.net】开心魔法.DVD国语中字.rmvb

${ftp_url}                   ftp://dygod3:dygod3@y069.dydytt.net:3272/海贼王/[阳光电影-www.ygdy8.com][one piece][677].rmvb

${http_url}                  http://down.33k.cc:41256/www.xunbo.cc/[迅雷下载Www.99b.Cc]名侦探柯南[第588话].rmvb

${thunder_http_url}          thunder://QUFodHRwOi8vZG93bi4zM2suY2M6NDExNTEvd3d3Lnh1bmJvLmNjL1vRuMDXz8LU2Fd3dy45OWIuQ2NdwfrW6bjEW7XaNja7sF0ucm12Ylpa

${thunder_magnet url}        thunder://QUFtYWduZXQ6P3h0PXVybjpidGloOkUxMDYxODQ5RTJBRDk5RkFGNjI4RkFERTFGOUM4RDFBQzBDNkU0RkJaWg==

${thunder_torrent_url}       thunder://QUFodHRwOi8vdDEzYTAxNXZtNy5zYW5kYWkubmV0L3hsbXVsdGlEaXJmaWxlLnRvcnJlbnRaWg==

${multi_url1}               http://test_multi/test1.rmvb
${multi_gcid1}              3211437DE059C491E762308903C1385959715E30
${multi_cid1}               3211437DE059C491E762308903C1385959715E30
${multi_filesize1}          113912612
${multi_gcid_part_size1}    262144
${multi_gcidlevel1}         90
${multi_filesuffix1}        rmvb


${multi_url2}               http://test_multi/test2.rmvb
${multi_gcid2}              FC3D34B673B0D5DD629EB4642475E5AEC76C00BA
${multi_cid2}               3211437DE059C491E762308903C1385959715E30
${multi_filesize2}          108060874
${multi_gcid_part_size2}    262144
${multi_gcidlevel2}         90
${multi_filesuffix2}        rmvb


${kankan_url}            http://pubnet.sandai.net:8080/20/c7cbb1a4ea986831ff7ca0a6922a9cc3427f7f98/fda828573c73cb5025fb51e80ba58c612c2114e1/1cba0685/200000/0/f62f5/0/0/1cba0685/0/index=0-12034/indexmd5=e653af462899a8ba72bc1eb5a4f9983f/90b8b9e231250636f1b4b8fa07b05775/47728e70c12307984ff35b4ab9af1973/fda828573c73cb5025fb51e80ba58c612c2114e1.flv.xv?type=vod&movieid=184337&subid=1093783&ext=.xv

${publish_url}      http://gdl.lixian.vip.xunlei.com/download?fid=5bTGntNVeixBNXJLO4XFNj1rst/AGBAAAAAAALapN3kdmCuPM/GPnTBbCC5JVHJ6&mid=666&threshold=150&tid=0CDBEF0232878C1D515C9142D31E6A89&srcid=4&verno=1&g=B6A937791D982B8F33F18F9D305B082E4954727A&scn=c8&i=B6A937791D982B8F33F18F9D305B082E4954727A&t=1&ui=109273277&ti=832266684861696&s=1054912&m=0&n=01085F972B616C6C5F075D852C68706C611854966E367833320044BB387462645F0259963B5F646E5F005085006169682E0449815F00000000&ff=0&co=5D4FC1B856091AFBA4CF6C29B9C5A5E7&cm=1&pk=lixian&ak=1:1:6:4&e=2000000000&ms=10485760&ck=98B2000655D698FAF0ED0B1C8C8D2779&at=B0B0871FA4588D729673CB1DC7E75D8D

${thunder_ed2k}  thunder://QUFlZDJrOi8vfGZpbGV8ob5MT0y159OwzOzMw3d3dy5sb2xkeXR0LmNvbaG/0s/Iyy4yMDE1LkhEVFPH5c7606LT79bQ06LLq9fWW0J0ubcgbG9sZHl0dC5jb21dKGxvbGR5dHQuY29tKS5tcDR8NjM5MDg4NjI3fDAwREQ0M0I2OUZENUQ0ODczREU0OTFBRkE2MjA0OUQ2fGg9TFRXVlRGVDdQUU8zQ1FXUVdCVjdZQkJZUU9QSjREMzZ8aHR0cDovL2ZhZmRhZmEucmFyfC9aWg==

${magnet_url}   magnet:?xt=urn:btih:E1061849E2AD99FAF628FADE1F9C8D1AC0C6E4FB
${bt_url}         bt://E1061849E2AD99FAF628FADE1F9C8D1AC0C6E4FB
${ed2k_url}      ed2k://|file|【LOL电影天堂www.loldytt.com】蚁人.2015.HDTS清晰英语中英双字[Bt狗 loldytt.com](loldytt.com).mp4|639088627|00DD43B69FD5D4873DE491AFA62049D6|h=LTWVTFT7PQO3CQWQWBV7YBBYQOPJ4D36|http://fafdafa.rar|/

${thunder_urlencode}      thunder://QUFodHRwJTNBJTJGJTJGZjIubWFya2V0Lm1pLWltZy5jb20vZG93bmxvYWQvQXBwU3RvcmUvMDRmYjFhNTM5MjljYjQxZjIwMjhiOTMwNWM2ZDZmNTZhYTBiNGNiZmQvJUU1JUIwJThGJUU3JUIxJUIzJUU2JTk5JUJBJUU4JTgzJUJEJUU1JUFFJUI2JUU1JUJBJUFEXzMuMC42XzYwMTc2Lm1kc1pa

${ed2k_bt}        ed2k://|file|【lol电影天堂www.loldytt.com】奇幻森林.The Jungle Book.2016.TC720P.X264.AAC.Mandarin.torrent|63095|0269DC4F381711900FF3893F1821BC7F|h=K7HWQ4EGL7L3AEDZ5TTISL7P33KSVCBH|/

${upgrade_bt}      http://dl.2xxv.mm/?h=30F38E191583A9B518FD30042D2E1B6464FE9961&i=99&v=1

${magnet32_url}    Magnet:?xt=Urn:btih:FTNKLA7DNVWNASNY3M7UZRS4U7M54RFX
${session_url}     http://218.77.3.29/cdn.baidupcs.com/file/7b571b8a4a786d9d4a191e7be82a3f1e?xcode=f080c63ed91e8fad3ea1baae38b1d03d3cce9f1bc6d88472&fid=1614005835-250528-2851940094&time=1400056872&sign=FDTAXER-DCb740ccc5511e5e8fedcff06b081203-TWdlcfpjuLSIOrkAKrYDHGKQooU%3D&to=cb&fm=NBTt&sta_dx=6&sta_cs=22&sta_ft=pdf&sta_ct=6&newver=1&expires=1400057472&rt=sh&r=767581845&logid=2184372551&sh=1&vuk=282335&fn=NoSQL%E7%B2%BE%E7%B2%B9.pdf&wshc_tag=0&wsiphost=ipdbm
