<template>
  <div class="svg-container">
    <svg ref="graph" :width="width" :height="height">
      <g :transform="'translate(' + width + ',' + height + ')'">
        <g ref="linksGroup"></g>
        <g ref="nodesGroup"></g>
      </g>
    </svg>
  </div>
</template>
<script>
import * as d3 from 'd3'
import axios from 'axios'
import * as d3_sampled from 'd3-force-sampled'

export default {
  setup() {},
  props: [
    'initial_crawl_link',
    'refresh_rate',
    'total_number_of_nodes',
    'number_of_nodes_per_branch',
    'getFirst'
  ],
  data() {
    return {
      crawl_link: '',
      loading: false,
      width: window.innerWidth / 2,
      height: window.innerHeight,
      selectedNode: { id: 'no node selected yet' },
      previously_visited_nodes: [],
      nodes: [],
      links: [],
      simulation: null,
      pathToRoot: [{ id: '' }],
      graph: {
        nodes: [],
        links: []
      }
    }
  },
  methods: {
    getPathToRoot() {
      return this.pathToRoot
    },
    getNodes() {
      return this.graph.nodes
    },
    getLinks() {
      return this.graph.links
    },
    getSelectedNode() {
      return this.selectedNode
    },
    async startGraph() {
      this.initializeGraph()
      this.previously_visited_nodes = []
      const sub_links = await this.getLinksAndNodes()
      var next_links = sub_links
      this.previously_visited_nodes.push(this.crawl_link)
      this.loading = false
      this.createForceGraph()
      while (this.graph.nodes.length <= this.total_number_of_nodes && this.loading === false) {
        const next_links_arr = []
        for (let link of next_links) {
          if (this.loading === true) {
            break
          }
          if (this.previously_visited_nodes.includes(link)) {
            continue
          }
          this.crawl_link = link
          const sub_links = await this.getNextLink()
          for (const sub_link of sub_links) {
            next_links_arr.push(sub_link)
          }
          this.previously_visited_nodes.push(link)
          if (this.graph.nodes.length > this.total_number_of_nodes) {
            break
          }
        }
        next_links = next_links_arr
        await this.sleep(this.refresh_rate)
      }
    },
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms))
    },
    async getNextLink() {
      const sub_links = await this.getLinksAndNodes()
      this.updateGraph()
      return sub_links
    },
    initializeGraph() {
      this.crawl_link = this.initial_crawl_link
      this.nodes = [this.crawl_link.slice()]
      this.graph.nodes = [{ id: this.crawl_link.slice() }]
      this.graph.links = []
    },
    async getLinksAndNodes() {
      try {
        const post_json = {
          link: this.crawl_link,
          crawled_links: [] // used to skip certain links
        }
        if (this.getFirst) {
          post_json.first_n_sublinks = Number(this.number_of_nodes_per_branch)
        } else {
          post_json.last_n_sublinks = Number(this.number_of_nodes_per_branch)
        }
        const response = await axios.post('http://localhost:3000/post_link', post_json)
        const links = this.graph.links
        const nodes = this.graph.nodes
        const sub_links = []
        // Welcome to spaghetti
        for (const node of response.data.nodes) {
          if (this.nodes.includes(node.id)) {
            var found_link = false
            for (let link of links) {
              if (link.source === this.crawl_link && link.target === node.id) {
                found_link = true
              }
            }
            if (!found_link) {
              links.push({ source: this.crawl_link, target: node.id })
            }
            continue
          }
          links.push({ source: this.crawl_link, target: node.id })
          nodes.push(node)
          sub_links.push(node.id)
          this.nodes.push(node.id)
        }
        this.graph.links = links
        this.graph.nodes = nodes
        return sub_links
      } catch (error) {
        this.error = error.response ? error.response.data : error.message
        console.error('There was an error!', error)
      }
    },
    createForceGraph() {
      const svg = d3.select(this.$refs.graph)
      const width = this.width
      const height = this.height
      const graph = this.graph

      // Define a force simulation
      this.simulation = d3
        .forceSimulation(graph.nodes)
        // .velocityDecay(0.2)
        .force(
          'link',
          d3.forceLink(graph.links).id((d) => d.id)
          // .distance(100)
        )
        .force('charge', d3_sampled.forceManyBodySampled())
        .force('center', d3.forceCenter(width / 2, height / 2))

      // Create a container for the graph that will be zoomed and panned
      const zoomGroup = svg.append('g').attr('class', 'zoom-group')

      // Create links
      const link = zoomGroup
        .append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(graph.links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#999')
        .style('stroke-opacity', 0.6)

      // Create nodes
      const node = zoomGroup
        .append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(graph.nodes)
        .enter()
        .append('g')
        .on('click', (event, d) => this.highlightNode(d))

      node.append('circle').attr('r', 5).attr('fill', 'steelblue')

      // Zoom behavior
      const zoom = d3.zoom().on('zoom', (event) => {
        zoomGroup.attr('transform', event.transform)
      })

      // Apply zoom to the SVG
      svg.call(zoom)

      // Update positions on each tick
      this.simulation.on('tick', () => {
        link
          .attr('x1', (d) => d.source.x)
          .attr('y1', (d) => d.source.y)
          .attr('x2', (d) => d.target.x)
          .attr('y2', (d) => d.target.y)

        node.attr('transform', (d) => `translate(${d.x}, ${d.y})`)
      })

      // this.node = node
      this.link = link
    },
    updateGraph() {
      const svg = d3.select(this.$refs.graph)

      // Update links
      const link = svg
        .select('.links')
        .selectAll('line')
        .data(this.graph.links, (d) => `${d.source.id}-${d.target.id}`)

      // Remove old links
      link.exit().remove()

      // Add new links
      link
        .enter()
        .append('line')
        .attr('class', 'link')
        .style('stroke', '#999')
        .style('stroke-opacity', 0.6)
        .merge(link)

      // Update nodes
      const node = svg
        .select('.nodes')
        .selectAll('g')
        .data(this.graph.nodes, (d) => d.id)

      // Remove old nodes
      node.exit().remove()

      // Add new nodes
      const newNode = node
        .enter()
        .append('g')
        .on('click', (event, d) => this.highlightNode(d))

      newNode.append('circle').attr('r', 5).attr('fill', 'steelblue')

      // Merge old and new nodes
      newNode.merge(node)

      // Restart the simulation with updated data
      this.simulation.nodes(this.graph.nodes)
      this.simulation.force('link').links(this.graph.links)
      this.simulation.alpha(1).restart()

      // Update positions on each tick
      this.simulation.on('tick', () => {
        svg
          .selectAll('.link')
          .attr('x1', (d) => d.source.x)
          .attr('y1', (d) => d.source.y)
          .attr('x2', (d) => d.target.x)
          .attr('y2', (d) => d.target.y)

        svg.selectAll('.nodes g').attr('transform', (d) => `translate(${d.x}, ${d.y})`)
      })

      this.node = newNode
      this.link = link
    },
    highlightNode(selectedNode) {
      this.selectedNode = selectedNode

      const svg = d3.select(this.$refs.graph)

      // Reset styles
      const allNodes = svg.selectAll('.nodes g').attr('fill', 'steelblue').style('opacity', 1)
      const allLinks = svg
        .selectAll('.links line')
        .style('stroke', '#999')
        .style('stroke-opacity', 0.6)

      // Highlight selected node
      allNodes
        .filter((d) => d.id === selectedNode.id)
        .select('circle')
        .attr('fill', 'orange')

      // Find neighbors of the selected node
      const neighbors = new Set()
      this.graph.links.forEach((link) => {
        if (link.source.id === selectedNode.id) {
          neighbors.add(link.target.id)
        }
        if (link.target.id === selectedNode.id) {
          neighbors.add(link.source.id)
        }
      })

      // Highlight neighbors
      allNodes
        .filter((d) => neighbors.has(d.id))
        .select('circle')
        .attr('fill', 'lightblue')

      allNodes
        .filter((d) => !neighbors.has(d.id) && d.id !== selectedNode.id)
        .select('circle')
        .attr('fill', 'steelblue')

      // Optionally change link color between the node and its neighbors
      allLinks
        .filter((d) => d.source.id === selectedNode.id || d.target.id === selectedNode.id)
        .style('stroke', 'orange')
        .style('stroke-opacity', 1)

      for (let node of this.getCalculatedPathToRoot(selectedNode)) {
        this.highlightSpecificNode(node)
      }
    },
    highlightSpecificNode(selectedNode) {
      const svg = d3.select(this.$refs.graph)
      const allNodes = svg.selectAll('.nodes g').attr('fill', 'steelblue').style('opacity', 1)
      allNodes
        .filter((d) => selectedNode.id === d.id)
        .select('circle')
        .attr('fill', 'pink')
    },
    getCalculatedPathToRoot(selectedNode) {
      const return_val = []
      var currentNode = selectedNode.id
      while (currentNode !== this.initial_crawl_link) {
        for (let link of this.graph.links) {
          if (link.target.id === currentNode) {
            return_val.push({ id: link.source.id })
            currentNode = link.source.id
            break
          }
        }
      }
      this.pathToRoot = return_val
      return return_val
    },
    async resetGraph() {
      this.loading = true
      // Reset data
      await this.sleep(this.refresh_rate + 1000) // stupid but waits for all nodes to be loaded before deletion
      this.graph.nodes = []
      this.graph.links = []
      this.nodes = []
      this.links = []
      this.selectedNode = { id: 'no node selected yet' }
      this.previously_visited_nodes = []

      // Reset SVG
      const svg = d3.select(this.$refs.graph)
      svg.selectAll('*').remove()
      this.$forceUpdate()
    }
  }
}
</script>
<style scoped>
.svg-container {
  width: 50vw;
  height: 100vh;
  overflow: auto;
  border: 1px solid #ccc;
  position: absolute;
  right: 10px;
  top: 0;
}

svg {
  width: 50vw;
  height: 100vh;
}
</style>
