


wifi.sta.config("TP-LINK_888","12345687")
wifi.sta.connect()
tmr.delay(1000000)   -- wait 1,000,000 us = 1 second
print(wifi.sta.status())
print(wifi.sta.getip())


sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("GET /ws\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n")
--............................................................................................................................

--send the message code part(final)

wifi.sta.config('TP-LINK_888','12345687')
wifi.sta.connect()
tmr.delay(1000000)   -- wait 1,000,000 us = 1 second
print(wifi.sta.status())
print(wifi.sta.getip())

sk=net.createConnection(net.TCP, 0)
sk:on('receive', function(sck, c) print(c) end )
sk:connect(3000,'52.138.39.36')
sk:send('GET /sms\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n')
--....................................................................................................................



sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
sk:send("POST /plist\r\n{username = customer1,password = 123}\r\n\r\n")
sk:send("POST /plist\r\n{username = "customer1", password = "123"}\r\nConnection: keep-alive\r\nAccept: /\r\n\r\n")
--wrong but no error....................................................................................................3:30

sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")
data_table = {
    username = "customer1",
    password = "123"
}
data = ""
for param,value in pairs(data_table) do
    data = data .. param.."="..value.."&"
end
print(data)
sk:send("POST ".."/login".." HTTP/1.1\r\n"..
"Host: ".."52.138.39.36".."\r\n"..
"Connection: close\r\n"..
"Content-Type: application/x-www-form-urlencoded\r\n"..
"Content-Length: "..string.len(data).."\r\n"..
"\r\n"..
data)








sk:send("GET /ws\r\n ")



sk:send("GET /"..HTTP_SERVER_SCRIPTNAME.."?id="..node.chipid()
                                             .."&t="..data1
                                             .."&h="..data2.." HTTP/1.1\r\n"
            .."Host: "..HTTP_SERVER_HOSTNAME.."\r\n"
            .."Connection: keep-alive\r\n"
            .."Accept: */*\r\n\r\n")








https://httpbin.org/post

http:52.138.39.36:3000/login
{   username:"customer1",
    password:"123"}







wifi.sta.config("TP-LINK_888","12345687")
wifi.sta.connect()
tmr.delay(1000000)   -- wait 1,000,000 us = 1 second
print(wifi.sta.status())
print(wifi.sta.getip())

sk=net.createConnection(net.TCP, 0)
sk:on("receive", function(sck, c) print(c) end )
sk:connect(3000,"52.138.39.36")

sk:send("POST "/login" HTTP/1.1\r\n"..
"Host: "..host.."\r\n"..
"Connection: close\r\n"..
"Content-Type: application/x-www-form-urlencoded\r\n"..
"Content-Length: "..string.len(data).."\r\n"..
"\r\n"..
data)
    