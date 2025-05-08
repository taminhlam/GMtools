#!/usr/bin/ruby
require 'cgi'
require 'erb'

begin
  require_relative '../scripts/getip.rb'
  $url = GETIP::V4.new.pri
rescue
  $url = "0.0.0.0"
end

page = ERB.new(File.read("websocket.html"))

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  page.result(binding)
end
