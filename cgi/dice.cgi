#!/usr/bin/ruby
require 'cgi'
require 'erb'

begin
  require_relative '../scripts/getip.rb'
  $url = GETIP::V4.new.pri
rescue
  $url = "0.0.0.0"
end

# page = ERB.new(File.read("websocket.html"))
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
<script src="/assets/js/dice.js"></script>
<style>
@font-face {
    font-family: 'Dicier';
    src:    url('../assets/fonts/dicier/Dicier-Round-Light.woff') format('woff'),
            url('../assets/fonts/dicier/Dicier-Round-Light.otf') format('truetype'),
    font-weight: normal;
    font-style: normal;
    /* font-feature-settings: "ss17"; */
}
article { font-family: 'Dicier';
          font-size: 2em;
          text-align: center; }
label, input, .button { width: 100%; }
</style>
<title>BCDice</title>
</head>
<body>
<form method="dialog">
  <label>Command</label>
  <input type="text" name="cmd">
  <input type="button" class="button" value="Roll">
</form>

<article id="response"></article>
<table>
<thead></thead>
<tbody id="res"></tbody>
</table>

<details>
<summary>help</summary>
<table>
  <thead>
    <tr>
      <th>コマンド名</th>
      <th>例</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/add_dice.html">加算ダイス</a>
      </td>
      <td>
        <code>2D6+1&gt;=7</code>, <code>5D6KH3</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/barabara_dice.html">バラバラダイス</a>
      </td>
      <td>
        <code>5B6</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/reroll_dice.html">個数振り足しダイス</a>
      </td>
      <td>
        <code>2R6[&gt;3]&gt;=5</code>, <code>2R6&gt;=5@&gt;3</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/upper_dice.html">上方無限ロール</a>
      </td>
      <td>
        <code>2U6[4]&gt;=10</code>, <code>2U6&gt;=10@4</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/tally_dice.html">集計ダイス</a>
      </td>
      <td>
        <code>8TY6</code>, <code>7TZ10</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/d66_dice.html">D66</a>
      </td>
      <td>
        <code>D66</code>, <code>D66A</code>, <code>D66D</code>, <code>D66N</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/calc.html">計算コマンド</a>
      </td>
      <td>
        <code>c1+2*3/4</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/choice.html">チョイスコマンド</a>
      </td>
      <td>
        <code>choice[A,B,Z]</code>, <code>choice(A,B,Z)</code>, <code>choice A B Z</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/repeat.html">繰り返しコマンド</a>
      </td>
      <td>
        <code>x5 2D6</code>, <code>rep5 2D6</code>, <code>repeat5 2D6</code>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://docs.bcdice.org/command/version.html">Versionコマンド</a>
      </td>
      <td>
        <code>BCDiceVersion</code>
      </td>
    </tr>
  </tbody>
  </table>
  <p>url: <%= $url %></p>
</details>
</body>
</html>
TEMPLATE

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  page.result(binding)
end
