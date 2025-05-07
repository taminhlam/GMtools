require "bcdice"
require "bcdice/game_system" # 全ゲームシステムをロードする

cthulhu7th = BCDice.game_system_class("Cthulhu7th")
result = cthulhu7th.eval("2d12") #=> #<BCDice::Result>
# result.methods.each { |v|
result.rands.each { |v|
  puts "#{v}"
}

# puts result.text      #=> "(1D100<=25) ボーナス・ペナルティダイス[0] ＞ 1 ＞ 1 ＞ クリティカル"
# puts result.success?  #=> true
# puts result.critical? #=> true
