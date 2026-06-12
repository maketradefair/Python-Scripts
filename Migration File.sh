curl -H "X-Requested-With: Curl Sample" -u "tatac3sa:Sw0rdf1sh@090"  "https://qualysguard.qg3.apps.qualys.com/api/2.0/fo/asset/ip/?action=list&tracking_method=IP" > ip_tracked

curl -H "X-Requested-With: Curl Sample" -u "sevenAsq:Sw0rdf1sh@123"  "https://qualysguard.qg1.apps.qualysksa.com/api/2.0/fo/asset/ip/?action=list&tracking_method=IP" > dns_tracked

curl -H "X-Requested-With: Curl Sample" -u "Username:Password" "https://qualysguard.qg1.apps.qualys.ae/api/2.0/fo/asset/group/?action=list" > asset_groups.xml

curl -H "X-Requested-With: Curl Sample" -u "arahb_em:API@m!grati0n" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/qid/search_list/dynamic/?action=list" > Dynamic-Search-Lists.xml

                                                                                                                                                                                                                                        

OPTION PROFILE
curl -u "tatac3sa:Sw0rdf1sh@090" -H "X-Requested-With:curl" "https://qualysguard.qg3.apps.qualys.com/api/2.0/fo/subscription/option_profile/?action=export" > Export-OP.xml
curl -u "tatac8sa6:Sw0rdf1sh@090" -H "X-Requested-With:curl" -H "content-type: application/xml" -X POST --data-binary @Export-OP.xml "https://qualysguard.qg1.apps.qualys.in/api/2.0/fo/subscription/option_profile/?action=import"



XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxxxxx

curl -H "X-Requested-With: Curl Sample" -u  "arahb_em:arahb_em" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/asset/group/?action=list&output_format=csv" > asset_groups.xml


curl -u "mzn_em:arahb_em" -H "X-Requested-With:curl" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/schedule/scan/?action=list" > Scheduled_Vuln_Scans.xml

curl -H "X-Requested-With: Curl Sample" -u "mzn_em:arahb_em"  "https://qualysguard.scan.stc.com.sa/api/2.0/fo/asset/ip/?action=list&tracking_method=IP" > dns_tracked

curl -H "X-Requested-With: Curl Sample" -u "tatac3sa:Sw0rdf1sh@090" "https://qualysguard.qg3.apps.qualys.com/api/2.0/fo/qid/search_list/dynamic/?action=list" > Dynamic-Search-Lists.xml

curl -H "X-Requested-With: Curl Sample" -u "arahb_em:arahb_em" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/qid/search_list/static/?action=list" > Static-Search-Lists.xml

OPTION PROFILE
curl -u "mzn_em:arahb_em" -H "X-Requested-With:curl" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/subscription/option_profile/?action=export" > Export-OP.xml
curl -u "mznAem1:arahb_em" -H "X-Requested-With:curl" -H "content-type: application/xml" -X POST --data-binary @Export-OP.xml "https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/subscription/option_profile/?action=import"



curl -u "mzn_em:arahb_em" -H "X-Requested-With:curl" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/schedule/scan/?action=list" > Scheduled_Vuln_Scans.xml

Report
curl -u "mzn_em:arahb_em" -H "X-Requested-With:curl" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/subscription/report/template/scan/?action=export" > Report.xml
curl -u "aanzAst1:uAUT9qW+" -H "X-Requested-With:curl" -H "content-type: application/xml" -X POST --data-binary @Report.xml "https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/report/template/scan/?action=import"


Policies
curl -H "X-Requested-With: Curl Sample" -u "mzn_em:arahb_em" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/compliance/policy/?action=export" > pc-policies.xml
curl -H "X-Requested-With: Curl Sample" -u "sevenAsq:Sw0rdf1sh@123" "https://qualysguard.qg1.apps.qualysksa.com/api/2.0/fo/asset/group/?action=list" > Asset_Groups_Edited.xml





curl -H "X-Requested-With: Curl Sample" -u "arahb_em:API@m!grati0n" "https://qualysguard.scan.stc.com.sa/api/2.0/fo/asset/ip/?action=list&tracking_method=IP" > ip_tracked


curl -H "X-Requested-With: Curl Sample" -u "arsevenAsq:Sw0rdf1sh@123" "https://qualysguard.qg1.apps.qualysksa.com/api/2.0/fo/asset/group/?action=list" > asset_groups.xml

https://qualysguard.scan.stc.com.sa/fo/scan/scanSearchLists.php


curl -u "aanzAst1:uAUT9qW+" -H "X-Requested-With:curl" -H "content-type: application/xml" -X POST --data-binary @Export-OP.xml "https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/subscription/option_profile/?action=import"



curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Authorization: mznAem1:arahb_em" \
  -d @policies.xml \
  "https://qualysapi.qg1.apps.qualysksa.com/api/2.0/fo/subscription/policies/?action=import"
