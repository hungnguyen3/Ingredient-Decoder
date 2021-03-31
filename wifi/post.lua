SSID = "TP-LINK_888"
SSID_PASSWORD = "12345687"
wifi.setmode(wifi.STATION)
wifi.sta.config(SSID,SSID_PASSWORD)
wifi.sta.autoconnect(1)
tmr.delay(1000000)
HOST = "52.138.39.36"
URI = "/search_byname"
function build_post_request(host, uri, data_table)
    data = ""
    for param,value in pairs(data_table) do
         data = data .. param.."="..value.."&"
    end
    request = "POST "..uri.." HTTP/1.1\r\n"..
    "Host: "..host.."\r\n"..
    "Connection: close\r\n"..
    "Content-Type: application/x-www-form-urlencoded\r\n"..
    "Content-Length: "..string.len(data).."\r\n"..
    "\r\n"..
    data
    print(request)
    return request
end

function send_sms()
    data = {
     to_search = "Apple"
    }
    socket = net.createConnection(net.TCP,0)
    socket:on("receive",display)
    socket:connect(3000,HOST)

    socket:on("connection",function(sck)
         post_request = build_post_request(HOST,URI,data)
         sck:send(post_request)
    end)
end
send_sms()