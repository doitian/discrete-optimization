#!/usr/bin/env ruby
require 'matrix'
require 'forwardable'

class Store
  attr_reader :solution

  attr_reader :edges

  attr_reader :node_count
  attr_reader :edge_count

  def initialize(node_count, edge_count)
    @node_count = node_count
    @edge_count = edge_count

    @solution = Array.new(@node_count, -1)
    @edges = Hash.new { |h, k| h[k] = [] }
    @store = Array.new(@node_count) { Array.new(@node_count) }
  end

  def add_edge(from, to)
    # Only need to check the already colored nodes, a.k.a, nodes id < self
    if from < to
      @edges[to] << from
    else
      @edges[from] << to
    end
  end

  def refresh_node(node_id)
    flags = @store[node_id]
    flags.fill(true)

    @edges[node_id].each do |id|
      flags[@solution[id]] = false
    end
    @solution[node_id] = -1
  end

  def next_node_candidate(node_id)
    flags = @store[node_id]
    return if @edges[node_id].size + 1 > flags.size

    current_solution = @solution[node_id]
    if current_solution >= 0
      last_false = flags.rindex(false)
      # It is already a new color, do not need to try another new color
      return if last_false.nil? || current_solution > last_false

      offset = current_solution + 1
      slice = flags[offset..-1]
      position = slice.index(true) if slice
      position + offset if position
    else
      flags.index(true)
    end
  end

  def color_node(node_id, color)
    @solution[node_id] = color
  end

  def restrict_color_count(limit)
    @store.each do |flags|
      flags.replace flags[0...limit]
    end
  end
end

class Solver
  extend Forwardable
  def_delegators :@store, :node_count, :edge_count

  attr_reader :color_count

  attr_reader :solution

  def initialize(store)
    @store = store
    @solution = (0...store.node_count).to_a
    @color_count = store.node_count
  end

  def search
    return if node_count <= 1

    starting_node = 0
    @store.refresh_node(starting_node)
    max_search_count = 3
    while max_search_count > 0 && starting_node >= 0 && (solution = search_once(starting_node))
      max_search_count -= 1
      @solution = solution.dup
      @color_count = @solution.max + 1

      break if @color_count <= 1 || (edge_count > 0 && @color_count == 2)

      @store.restrict_color_count(@color_count - 1)
      starting_node = @solution.index(@color_count - 1) - 1
    end
  end

  private

  def search_once(starting_node)
    current_node = starting_node

    max_iter = 100000
    while (starting_node == 0 || max_iter > 0) && current_node >= 0 && current_node < node_count
      max_iter -= 1
      color = @store.next_node_candidate(current_node)

      if color
        @store.color_node(current_node, color)
        current_node += 1
        if current_node < node_count
          @store.refresh_node(current_node)
        end
      else
        current_node -= 1
      end
    end

    if current_node == node_count
      return @store.solution
    end
  end
end

node_count, edge_count = STDIN.gets.split.collect(&:to_i)

store = Store.new(node_count, edge_count)

STDIN.each_line do |line|
  from, to = line.split.collect(&:to_i)
  store.add_edge from, to
end

solver = Solver.new(store)
solver.search

solution = solver.solution
color_count = solver.color_count

if ARGV.first == '--plot'
  COLORS = %W{aliceblue	antiquewhite	   aqua   	aquamarine	azure
beige	bisque	black	blanchedalmond	   blue   
blueviolet	brown	burlywood	cadetblue	chartreuse
chocolate	coral	cornflowerblue	cornsilk	crimson
   cyan   	darkblue	darkcyan	darkgoldenrod	darkgray
darkgreen	darkgrey	darkkhaki	darkmagenta	darkolivegreen
darkorange	darkorchid	darkred	darksalmon	darkseagreen
darkslateblue	darkslategray	darkslategrey	darkturquoise	darkviolet
deeppink	deepskyblue	dimgray	dimgrey	dodgerblue
firebrick	floralwhite	forestgreen	fuchsia	gainsboro
ghostwhite	   gold   	goldenrod	   gray   	   grey   
green	greenyellow	honeydew	hotpink	indianred
indigo	ivory	khaki	lavender	lavenderblush
lawngreen	lemonchiffon	lightblue	lightcoral	lightcyan
lightgoldenrodyellow	lightgray	lightgreen	lightgrey	lightpink
lightsalmon	lightseagreen	lightskyblue	lightslategray	lightslategrey
lightsteelblue	lightyellow	   lime   	limegreen	linen
magenta	maroon	mediumaquamarine	mediumblue	mediumorchid
mediumpurple	mediumseagreen	mediumslateblue	mediumspringgreen	mediumturquoise
mediumvioletred	midnightblue	mintcream	mistyrose	moccasin
navajowhite	   navy   	oldlace	olive	olivedrab
orange	orangered	orchid	palegoldenrod	palegreen
paleturquoise	palevioletred	papayawhip	peachpuff	   peru   
   pink   	   plum   	powderblue	purple	   red   
rosybrown	royalblue	saddlebrown	salmon	sandybrown
seagreen	seashell	sienna	silver	skyblue
slateblue	slategray	slategrey	   snow   	springgreen
steelblue	   tan   	   teal   	thistle	tomato
turquoise	violet	wheat	white	whitesmoke
yellow	yellowgreen}

  puts "graph coloring {"

  puts "node [colorscheme=svg,style=filled];"
  solution.each_with_index do |color, i|
    puts "#{i} [color=#{COLORS[color]}];"
  end

  store.edges.each_pair do |from, tos|
    tos.each do |to|
      puts "#{from} -- #{to};"
    end
  end

  puts "}"
else
  puts "#{color_count} 0"
  puts solution.join(' ')
end

