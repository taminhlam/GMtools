require 'webrick/websocket'
require 'json'
require 'bcdice'
require 'bcdice/game_system' # 全ゲームシステムをロードする

server = WEBrick::Websocket::HTTPServer.new(Port: 8000, DocumentRoot: File.dirname(__FILE__))

def roll(querystring)
  if querystring.nil? or querystring.empty?
    return  nil
  else
    puts "interpreted as: #{querystring}"
    roll  = querystring.chomp

    game_system = BCDice.game_system_class("DiceBot")
    result      = game_system.eval(roll)
    puts "result.text: #{result.text}"
    data        = { 'roll' => roll,
                    'rands' => result.rands,
                    'secret' => result.secret?,
                    'success' => result.success?,
                    'failure' => result.failure?,
                    'critical' => result.critical?, 
                    'fumble' => result.fumble?,
                    'text' => result.text
                                    .dump
                                    # .gsub("成功", "success")
                                    # .gsub("＞", "&#xFF1E;")
                                    # .gsub("<", "&lt;")
                                    # .encode('utf-8')
                                    # .gsub("[", "&#91;")
                                    # .gsub("]", "&#93;")
                                    # .gsub("+", "&#43;")
                  }

    return JSON.dump(data)
  end
end

class MyServlet < WEBrick::Websocket::Servlet
  @@socks = []

  def select_protocol(available)
    # method optional,
    # if missing, it will always select first protocol.
    # Will only be called if client actually requests a protocol
    available.include?('myprotocol') ? 'myprotocol' : nil
  end

  def socket_open(sock)
    @@socks.push sock
    sock.puts ['Welcome'].to_json # send a text frame
  end

  def socket_close(sock)
    @@socks.delete sock
    puts 'Poof. Socket gone.'
  end

  def socket_text(sock, text)
    puts "Client sent: #{text}"
    result = roll(text)
    @@socks.each { |s|
      s.puts result.to_s
    }
  end
end

server.mount('/websocket', MyServlet)

server.start
