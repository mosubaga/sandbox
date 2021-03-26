require 'net/http'
require 'uri'
require 'json'

uri = URI('https://api.covidtracking.com/v1/states/current.json')
response = Net::HTTP.get_response(uri)

parsed = JSON.parse(response.body) # returns a hash

# Create Hashes
cases  = Hash.new()
deaths = Hash.new()

parsed.each do |data|
  sState    = data['state']
  iPositive = data['positive']
  iDeaths   = data['death']
  cases[sState] = iPositive
  deaths[sState] = iDeaths
end

cases = cases.sort_by {|k, v| -v}

i = 1
cases.each do |key, value|
  puts "#{i},#{key},#{value},#{deaths[key]}\n"
  i+=1
end



