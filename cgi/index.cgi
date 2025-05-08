#!/usr/bin/ruby

require 'cgi'
require 'erb'

$page = ERB.new(<<PAGE)
<!DOCTYPE html>
<head>
<meta http-equiv="Content-Type"
      content="text/html;
      charset=utf-8">
<meta name="viewport"
      content="width=device-width,
      initial-scale=1.0,
      user-scalable=yes" />
<title>Index</title>
<link href="/assets/warai4.ico"
      rel="icon"
      type="image/x-icon"/>
<style>
ul      { list-style-type: none; 
          padding-left:    0; }
.button { width:           100%; }
</style>
<link href="/assets/css/simple.min.css"
      rel="stylesheet"
      type="text/css"/>
</head>
<body>

<h1>Tools</h1>


<ul class="cards">
<% @scripts.each do |a| %>
  <li class="card">
    <a class="button" href="/<%= a %>">
      <%= a.gsub(/\.cgi$/, '').gsub("_", " ") %>
    </a>
  </li>
<% end %>
</ul>
</body>
</html>
PAGE

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  @scripts = Dir.children(Dir.pwd).sort.select { |i| /.*cgi$/.match? i }
  # @scripts.delete(caller_locations.first.path.split('/')[1])
  @scripts.delete("index.cgi")
  @scripts.delete("api.cgi")
  $page.result(binding)
end

__END__

$links = [
  { 'href'=> "/assets/Snap-latest/snap.html",
    'name'=> 'Snap!' },
  { 'href'=> "/assets/CharacterMap/index.html",
    'name'=> 'CharacterMap' },
  { 'href'=> "/assets/cyberchef/CyberChef_v9.46.0.html",
    'name'=> 'CyberChef' },
  { 'href'=> "/assets/kuroshimu-main/index.html",
    'name'=> 'Kuroshimu' },
  { 'href'=> "/assets/twine-web/index.html",
    'name'=> 'Twine' },
  { 'href'=> "https://taminhlam.github.io/notes/",
    'name'=> 'My Library' },
  { 'href'=> "#",
    'onclick' => 'javascript:window.location.port=8080',
    'name'=> 'VLC' },
  { 'href'=> "#",
    'onclick' => 'javascript:window.location.port=1780',
    'name'=> 'Snapcast' }
]

<% $links.each do |a| %>
  <% if a['onclick'] %>
  <li class="card">
    <a class="button" href="<%= a['href'] %>" onclick="<%= a['onclick'] %>"><%= a['name'] %></a>
  </li>
  <% else %>
  <li class="card">
    <a href="<%= a['href'] %>"><%= a['name'] %></a>
  </li>
  <% end %>
<% end %>
