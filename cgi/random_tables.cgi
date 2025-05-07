#!/usr/bin/ruby
require 'cgi'
require 'erb'

$template   = ERB.new(<<TEMPLATE)
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      lang="en-US"
      xml:lang="en-US"/>
<head>
<link href="/assets/warai4.ico"
      rel="icon"
      type="image/x-icon"/>
<meta http-equiv="content-type"
      content="text/html; charset=UTF-8"/>
<meta charset="utf-8"/>
<meta name="viewport"
      content="width=device-width, initial-scale=1.0, user-scalable=yes"/>
<meta name="author"
      content="Ta Minh Lam"/>
<meta name="robots"
      content="noindex"/>
<meta name="googlebot"
      content="noindex"/>
<link rel="stylesheet"
      href="assets/css/simple.min.css"
      type="text/css"/>
<title>Random Tables</title>
<script src="/assets/js/htmx.min.js"></script>
<style>
ul     { list-style-type: none;
         padding-left:    0; }
button { width:           100%;
         text-align:      left; }
</style>
</head>
<body>

<h1>Random Tables</h1>

<table id="answer"></table>

<% @files.each_key do |k| %>
<% next if @files[k].all? { |f| File.directory? f[0] } %>
<details>
<summary><%= k %></summary>
<ul>
  <% @files[k].each do |f| %>
  <li>
    <button hx-get="api.cgi"
            hx-vals='{"random": "1", "path": "<%= f[0] %>"}'
            hx-target="#answer">
    <%= f[2] %>
    </button>
  </li>
  <% end %>
</ul>
</details>
<% end %>

</body>
</html>
TEMPLATE

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do

  @files = {}
  Dir["../data/**/*"]
     .select { |c| /.+\.tsv$/.match? c }
     .map    { |path|
                #e.g. "foo/bar/baz.mp4"
                dir  = File.split(File.dirname(path)).last #=> "bar"
                ext  = File.extname(path)                  #=> ".mp4"
                name = File.basename(path, ext)            #=> "baz"

                @files[dir] = [] unless @files.has_key? dir
                @files[dir].push [path, dir, name]
              }  
  $template.result(binding)
end
