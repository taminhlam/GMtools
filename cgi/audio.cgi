#!/usr/bin/ruby
require 'cgi'
require "erb"

$page = ERB.new(<<PAGE)
<!DOCTYPE html>
<head>
<meta http-equiv="Content-Type"
      content="text/html; charset=utf-8">
<meta name="viewport"
        content="width=device-width, initial-scale=1.0, user-scalable=yes"/>
<title>Audio</title>
<link href="/assets/warai4.ico"
      rel="icon"
      type="image/x-icon"/>
<link href="/assets/css/simple.min.css"
      rel="stylesheet"
      type="text/css"/>
<style>
img,
audio,
video   { margin:     auto;
          width:      auto;
          height:     auto;
          width:      100%;
          max-height: 90vh;
          transition: opacity 300ms ease-in; }
td.loop { background: #ffb300; }
.num    { color:      gray; }
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("table").addEventListener("click", function(e) {
    var classes = e.target.classList;
    if (classes.contains("loop")) {
      e.target.parentElement.classList.toggle('loop')
      prev = e.target.parentElement.previousSibling.lastElementChild;
      console.log(prev);
      if (prev.loop == false) {
        prev.loop = true}
      else {
        prev.loop = false
      };
    }
  });
})
</script>
</head>
<body>

<h1>Audio</h1>
<% @files.each_key do |k| %>
<% next if @files[k].all? { |f| File.directory? f[0] } %>
<details>
<summary><%= k %></summary>
  <table>
    <tbody>
    <% @files[k].each.with_index do |f, i| %>
    <% next if File.directory? f[0] %>
      <tr>
        <td class="num"><%= i %></td>
        <td>
        <span><%= f[2].gsub("_", " ") %></span>
      <% if f[1] == "img" %>
        <img src="<%= f[0] %>" loading="lazy"/>
        <td></td>
      <% elsif f[1] == "video" %>
        <video src="/media/<%= f[0] %>" controls></video>
        <td><a class="button loop" href="#loop<%= i %>">loop
      <% elsif f[1] == "audio" %>
        <audio src="/media/<%= f[0] %>" controls preload="none"></audio>
        <td><a class="button loop" href="#loop<%= i %>">loop
      <% end %>
        </td>
      </tr>
    <% end %>
    </tbody>
  </table>
</details>
<% end %>

</body>
</html>
PAGE

$types = {
  "img"   => [".gif", ".jpg", ".jpeg", ".png", ".webp"],
  "audio" => [".mp3", ".ogg", ".wav", ".m4a"],
  "video" => [".mp4"]
}

def gettype(extension) 
  $types.each { |t|
    return t[0] if t[1].include? extension.downcase
  }
end

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  @files = {}
  Dir["../media/**/*"]
              .select { |c| /.+\..{3,}$/.match? c }
              .map    { |path|
                #e.g. "foo/bar/baz.mp4"
                dir  = File.split(File.dirname(path)).last #=> "bar"
                ext  = File.extname(path)                  #=> ".mp4"
                name = File.basename(path, ext)            #=> "baz"

                @files[dir] = [] unless @files.has_key? dir
                @files[dir].push [path,  gettype(ext), name]
              }

  $page.result(binding)
end
