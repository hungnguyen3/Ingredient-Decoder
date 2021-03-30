-- connect to wifi
wifi.sta.config("name","password")
wifi.sta.connect()
tmr.delay(1000000)

-- trying get/post requests
sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("GET /ws\r\nConnection: keep-alive\r\nAccept: /\r\n\r\n")

sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("POST /login\r\n Connection: keep-alive\r\nAccept: /\r\n\r\n")

uri = "/login"
host = "52.138.39.36"
sk:send("POST "..uri.." HTTP/1.1\r\n"..
    "Host: "..host.."\r\n"..
    "Connection: keep-alive\r\n"..
    "Accept: /\r\n\r\n"..
    "Content-Type: application/x-www-form-urlencoded\r\n"..
    "\r\n"..)