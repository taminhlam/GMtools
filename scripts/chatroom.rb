#!/usr/bin/ruby
require 'json'
require 'bcdice'
require 'bcdice/game_system' # 全ゲームシステムをロードする

querystring = ENV['QUERY_STRING']

if querystring.nil?
  result  = {}
else
  roll  = querystring.split("=")
                     .last
                     #.gsub("1d100", "2d10")

  engine = BCDice.game_system_class("Cthulhu7th")

  result = engine.eval(roll).rands.map { |pair|
    pair.join("_ON_D")
  }.join(", ")

  result = result.to_json
end

p "#{result}"


__END__

# puts result.text      #=> "(1D100<=25) ボーナス・ペナルティダイス[0] ＞ 1 ＞ 1 ＞ クリティカル"
# puts result.success?  #=> true
# puts result.critical? #=> true

