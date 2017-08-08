import csv
import urllib2
import urllib
import json
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="WIFI Passwords Crack")
    parser.add_argument("-f", required=True, type=str,dest='file', help='Target WigleWifi CSV file')
    args = parser.parse_args()
    filename = args.file
    
    csvfile = file(filename, 'rb')
    reader = csv.reader(csvfile)

    rows = [row for row in reader]
    rows = rows[2:]

    ssids = ''
    bssids = ''

    count = 0
    for row in rows:
        if row[10] == 'WIFI':
            ssids = ssids + row[1] + ','
            bssids = bssids + row[0].replace(':', '') + ','
            count = count + 1
            

    csvfile.close()

    postdata = 'ssids=' + ssids[:len(ssids)-1] + '&bssids=' + bssids[:len(bssids)-1]
    print '[+] The number of WIFIs: ' + str(count)
    print '[+] Now start cracking, please wait...'
    
    
    url = 'http://' + 'www.wifi4.cn' + '/api/v2/?random=0.5093924434059545'
    request = urllib2.Request(url)

    try:
        request.add_header('Origin', 'http://www.wifi4.cn')
        request.add_header('X-Requested-With', 'XMLHttpRequest')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        request.add_header('Referer', 'http://www.wifi4.cn/querys/')
        request.add_header('Cookie', 'PHPSESSID=1;')
    
        request.add_data(postdata)
        response = urllib2.urlopen(request)
        if response.code == 200 :
            resdata = response.read()
            j = json.loads(resdata)
            count = 0
            for x in j['querys']:
                pwd = j['querys'][x]["pwd"]
                if pwd != '':
                    print "====================================================="
                    print 'ssid:' + j['querys'][x]['ssid']
                    print 'bssid: ' + j['querys'][x]['bssid']
                    print 'password: ' + pwd
                    count = count + 1

            print ''
            print '[+] ' + str(count) + ' passwords cracked!'
        else:
            print '[-] Crack fail!'
            
    except Exception as e:
        print "[-] Exception: " + str(e)
