# Client-Proxy-Server
---

## Assignment - CS5060: ACN

---
* *This Repo Contain files*
  * Server File.
  * Proxy File.
  * Client File.
  * ExtendedProxy.
      * extendedProxy
      * daily.py
      * weekly.py
      * monthy.py
      * plot.py

```
1 | client.py             |
2 | server.py             | 
3 | proxy.py              | 
4 | extendedProxy.py      | 
5 | daily.py              | 
6 | weekly.py             | 
7 | monthy.py             | 
8 | plot.py               | 

```


 **I Have Folder Structure for Storage as follows**
---
* In server
```bash
index.html
image1.jgp
image2.jpg
```


# **How To Run Code?**


 * To run the server
```bash
python3 server.py
```



# **To run the client**
```bash
python3 client.py
```

Input in client
```bash
[server_ip]/[server_domain_name]
[server_port]
[proxy_ip]/[]
[proxy_port]/[]
[path]
```

If proxy ip and port number not given means direct communication to server is done.



# **To run the proxy**
```bash
python3 proxy.py
```



# **To run the Extended Proxy**
```bash
python3 ExtendedProxy.py (It will store statistics in web_usage_data.csv file)
python3 plot.py
python3 daily.py
python3 monthy.py
python3 weekly.py
```
* It will plot the corresponding graphs for the given data
---


# **Using Browser to fetch HTTP request**
   *Two way*
   * **FIRST:  Configuring your Browser to use proxy**
   * You can also directly configure your web browser to use your proxy. This depends on your browser.
    In Internet Explorer, you can set the proxy in 
    Tools > Internet Options > Connections tab > LAN Settings.

* In Netscape (and derived browsers such as Mozilla), you can set the proxy in 
    Tools >Options > Advanced tab > Network tab > Connection Settings.
* In both cases you need to give the address of the proxy and the port number that you gave when you ran the proxy server. You should be able to run the proxy and the browser on the same computer without any problem. With this approach, webpage using the proxy server, you simply provide the URL of the page you want.
    For e.g. http://www.google.com.

* **SECOND: By explicitly forcing the browser to request the server through proxy** proxy_ip:Proxy_port/server_ip:server_port/path in browser
    For e.g. 127.0.0.1:12000/127.0.0.1:6789/index.html.

