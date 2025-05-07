#!/usr/bin/ruby
require 'socket'

# addlist = Socket.ip_address_list
# addlist.each { |a|
# if (a.ipv4? and a.getnameinfo[0] != "localhost")
  # @locip = a.inspect_sockaddr
# end

# based on:
# https://stackoverflow.com/questions/5029427/ruby-get-local-ip-nix

module GETIP

  class V4
    def initialize
      @pub = Socket.ip_address_list.detect{ |intf|
        intf.ipv4? and
        !intf.ipv4_loopback? and
        !intf.ipv4_multicast? and
        !intf.ipv4_private? }

      @pri = Socket.ip_address_list.detect{ |intf| intf.ipv4_private? }
    end

    def pub
      @pub.inspect_sockaddr unless @pub.nil?
    end

    def pri
      @pri.inspect_sockaddr
    end
  end

end
