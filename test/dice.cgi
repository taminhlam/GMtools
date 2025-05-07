#!/usr/bin/ruby
require 'cgi'
require 'erb'
require 'bcdice'
require 'bcdice/game_system' # 全ゲームシステムをロードする

page = ERB.new(<<TEMPLATE)
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      lang="en-US"
      xml:lang="en-US">
<head>
<meta charset="utf-8">
<meta http-equiv="content-type"
      content="text/html; charset=UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0, user-scalable=yes">
<meta name="author"
      content="Ta Minh Lam">
<meta name="robots"
      content="noindex">
<meta name="googlebot"
      content="noindex">
<link rel="icon"
      href="../assets/warai4.ico"
      type="image/svg+xml">
<link rel="stylesheet"
      href="../assets/css/simple.min.css"
      type="text/css"/>
<title>Dice</title>
<style>
@font-face {
    font-family: 'Dicier';
    src:    url('../assets/fonts/dicier/Dicier-Round-Light.woff') format('woff'),
            url('../assets/fonts/dicier/Dicier-Round-Light.otf') format('truetype'),
    font-weight: normal;
    font-style: normal;
}
</style>
</head>
<body>
<form hx-post="/submit-form" hx-target="#response">
  <p>
  <label>Command</label>
  <input type="text" name="cmd" style="width: 100%;">
  </p>
  <input type="submit" value="Submit">
</form>

<article id="response">
<%= query %>:
<p style="font-family: 'Dicier'; font-size: 2em; text-align: center;">
<%= result %>
</p>
</article>
</body>
</html>
TEMPLATE

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  engine = BCDice.game_system_class("Cthulhu7th")
  begin
    query  = ENV["QUERY_STRING"].split("=")
                                .last
                                .gsub("1d100", "2d10") unless ENV["QUERY_STRING"].nil?
    result = engine.eval(query).rands.map { |pair|
      pair.join("_ON_D")
    }.join(", ")
  rescue
    result = "cmd incorrect"
  end
  page.result(binding)
end


__END__
  if $cgi.params.map { |v| v.first }.include? 'id' or /^id=/.match? ENV["QUERY_STRING"]
    @id = ENV["QUERY_STRING"].split("=").last
    if not ENV["CONTENT_TYPE"].nil?
      @data = $cgi['fileToUpload'].read
      @name = $cgi['fileToUpload'].original_filename
      # FileUtils.mkdir_p(@path)
      File.open("../assets/uploads/#{@id}/#{@name}", 'w') { |f|
        f.write(@data)
      }
    end
    #$test.result(binding)
    #@files = Dir.children("../assets/Gallery/")
 	# @files = Dir["../assets/uploads/#{$cgi.params['id'][0]}/*"]
 	@files = Dir["../assets/uploads/#{@id}/*"]
            .select { |c| /.+\..{3,}$/.match? c }
            .map    { |f| [f, gettype(f)] }
    $inside.result(binding)
  else
    $test.result(binding)
  end

  <button>Send</button>
  <button type="reset">Reset</button>
  <button disabled="disabled">Disabled</button>
