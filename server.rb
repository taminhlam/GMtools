#!/usr/bin/ruby

require 'cgi'
require 'webrick'
require 'dworker'

# begin
  # require 'zeroconf'
  # $host = "test-hostname"
  # ZeroConf.service "_http._tcp.local.", 8080, host
# rescue
  $host = "0.0.0.0"
# end

### Config ############################################################

def start_webrick(config = {})
  @port    = 8080
  @address = $host
  # @address = "0.0.0.0"
  config.update(:Port => @port)
  config.update(:BindAddress => @address)
  server = WEBrick::HTTPServer.new(config)
  yield server if block_given?
  # # http://www.ruby-doc.org/core-2.1.1/Kernel.html#method-i-trap
  ['INT', 'TERM'].each {|signal|
    trap(signal) {server.shutdown}
  }
  puts "Starting Webrick at \"http://#{@address}:#{@port}\""
  server.start
end

# WEBrick::HTTPServlet::FileHandler.add_handler("erb", WEBrick::HTTPServlet::ERBHandler)

### Rinda ##############################################################

# begin
  # $ts = DWorker.new.ts
  # puts "#{$ts}"
# rescue
  # $ts = nil
  # puts "No Tuplespace …"
# end

### Start #############################################################

start_webrick { |server|
  cgi_dir = File.expand_path("cgi")
  server.mount('/', WEBrick::HTTPServlet::FileHandler, cgi_dir)
  server.mount('/assets', WEBrick::HTTPServlet::FileHandler, 'assets/')
  server.mount('/media', WEBrick::HTTPServlet::FileHandler, 'media/')
}
