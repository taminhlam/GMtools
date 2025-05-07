#!/usr/bin/ruby
require 'cgi'
require 'erb'
require 'csv'

$test  = ERB.new(<<TEMPLATE)
<tbody>
<% $lines.each do |line| %>
  <tr>
    <% line.each do |l| %>
    <td><%= l %></td>
    <% end %>
  </tr>
<% end %>
</tbody>
TEMPLATE
$lines = []

def ask(path)
  raw     = File.read(path).force_encoding("UTF-8")
  data    = CSV.parse(raw, :col_sep => "\t")
  headers = data.shift if data[0].first == "h"
  cols    = data.map { |d| d.length }.max
  sample  = data.sample(cols).map.with_index { |d, i| [d[i]] }
  if not headers.nil?
    sample = sample.map.with_index { |s, i| [headers[i]] + s }  
  end
  sample
end

$cgi = CGI.new
$cgi.out( type: 'text/html',
          status: 200,
          charset: 'UTF-8') do
  query = CGI.parse(ENV["QUERY_STRING"])
  if not query['path'].nil?
    path   = query['path'][0]
    $lines = ask(path)
  else
    begin
      $lines = CGI.parse(ENV["QUERY_STRING"]).to_a
    rescue
      $line = ["All broken ..."]
    end
  end
  $test.result(binding)
end
