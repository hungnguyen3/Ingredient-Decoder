-- connect to wifi
wifi.sta.config("name","password")
wifi.sta.connect()
tmr.delay(1000000)

-- trying get request
sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("GET /ws\r\nConnection: keep-alive\r\nAccept: /\r\n\r\n")

-- trying single quotation marks
sk=net.createConnection(net.TCP, 0)
sk:on('receive', function(sck, c) print(c) end )
sk:connect(3000,'52.138.39.36')
sk:send('GET /ws\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n')

-- trying post request
data_table = {
    to_search = "Apple",
}

data = "" 
for param,value in pairs(data_table) do     
    data = data .. param.."="..value.."&" 
end
print(data)
sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("POST /search_byname\r\nHost: 52.138.39.36\r\nConnection: keep-alive\r\nAccept: /\r\n\r\nContent-Type: application/x-www-form-urlencoded\r\n"..
        "Content-Length: "..string.len(data).."\r\n"..
        "\r\n"..
        data)

-- post request format
uri = "/login"
host = "52.138.39.36"
sk:send("POST "..uri.." HTTP/1.1\r\n"..
    "Host: "..host.."\r\n"..
    "Connection: keep-alive\r\n"..
    "Accept: /\r\n\r\n"..
    "Content-Type: application/x-www-form-urlencoded\r\n"..
    "\r\n"..)

---------------------------------------
    request = "POST "..uri.." HTTP/1.1\r\n"..
    "Host: "..host.."\r\n"..
    "Connection: close\r\n"..
    "Content-Type: application/x-www-form-urlencoded\r\n"..
    "Content-Length: "..string.len(data).."\r\n"..
    "\r\n"..
    data