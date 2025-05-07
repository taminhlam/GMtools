require "bcdice"
require "bcdice/game_system" # 全ゲームシステムをロードする

cthulhu7th = BCDice.game_system_class("Cthulhu7th")
result = cthulhu7th.eval("3d12") #=> #<BCDice::Result>
# result.methods.each { |v|
# puts result&.text #cf `repl.rb:151`

if result
  puts "type: #{result.class}"
  r = result
  r = {        'rands'          => r.rands, 
               'detailed_rands' => r.detailed_rands.inspect, 
               'secret'         => r.secret?, 
               'success'        => r.success?, 
               'failure'        => r.failure?, 
               'critical'       => r.critical?, 
               'fumble'         => r.fumble?,
               'text'           => r.text
      }
   puts "#{JSON.dump(r)}"
  # rands = result.rands
  # result.rands.each { |v|
    # puts "#{v}"
  # }
end

__END__
# puts result.text      #=> "(1D100<=25) ボーナス・ペナルティダイス[0] ＞ 1 ＞ 1 ＞ クリティカル"
# puts result.success?  #=> true
# puts result.critical? #=> true

+-------------------+--------------------------------------------+
| コマンド名 	        | 例                                         |
+-------------------+--------------------------------------------+
| 加算ダイス 	        | 2D6+1>=7, 5D6KH3                           |
| バラバラダイス      | 5B6                                        |
| 個数振り足しダイス   | 2R6[>3]>=5, 2R6>=5@>3                      |
| 上方無限ロール      | 2U6[4]>=10, 2U6>=10@4                      |
| 集計ダイス 	        | 8TY6, 7TZ10                                |
| D66               | D66, D66A, D66D, D66N                         |
| 計算コマンド        | c1+2*3/4                                   |
| チョイスコマンド    | choice[A,B,Z], choice(A,B,Z), choice A B Z |
| 繰り返しコマンド    | x5 2D6, rep5 2D6, repeat5 2D6              |
| Versionコマンド    | BCDiceVersion                              |
+-------------------+--------------------------------------------+
