<template>
  <div style="widows: 100%; height: 100%">
    <div class="form-container">
      <!-- Input for string -->
      <label for="inputString">Wikipedia String: </label>
      <input type="text" id="inputString" v-model="initial_crawl_link" />
      <!-- Slider 1 -->
      <label for="slider1">Refresh Rate (0-1500): {{ refresh_rate }}</label>
      <input type="range" id="slider1" v-model="refresh_rate" min="10" max="1500" />
      <!-- Slider 2 -->
      <label for="slider2"
        >Number Of Nodes Per Branch (5-500): {{ number_of_nodes_per_branch }}</label
      >
      <input type="range" id="slider2" v-model="number_of_nodes_per_branch" min="5" max="500" />
      <!-- Slider 3 -->
      <label for="slider2"
        >Total Number Of Nodes (500-2000 but it lags the larger it gets):
        {{ total_number_of_nodes }}</label
      >
      <input type="range" id="slider3" v-model="total_number_of_nodes" min="500" max="10000" />
      <!-- Checkbox -->
      <label for="checkbox"
        >Get First {{ number_of_nodes_per_branch }} (left unchecked will get last
        {{ number_of_nodes_per_branch }})</label
      >
      <input type="checkbox" id="checkbox" v-model="getFirst" />
      <div class="form-group">
        <h3>Form Data:</h3>
        <p>Root Wiki Url: {{ initial_crawl_link }}</p>
        <p>Refresh Rate: {{ refresh_rate }}</p>
        <p>Number Of Nodes Per Branch: {{ number_of_nodes_per_branch }}</p>
        <p>Total Number Of Nodes: {{ total_number_of_nodes }}</p>
        <p>
          Type:
          {{
            getFirst === true
              ? 'get first ' + number_of_nodes_per_branch + ' links'
              : 'get last ' + number_of_nodes_per_branch + ' links'
          }}
        </p>
      </div>
      <button v-if="!button_pressed" @click="callStartGraph">Grow Tree!</button>
      <button v-if="button_pressed" @click="reloadPage">Reset Tree!</button>
      <p>
        selected =
        <a
          v-if="getSelectedNode().id == 'no node selected yet' ? false : true"
          :href="getSelectedNode().id"
          >{{ getSelectedNode().id }}</a
        >
      </p>
      <div>
        <p>All Nodes</p>
        <label for="inputString">Search For: </label>
        <input type="text" id="inputString" v-model="searched_text_input" />
        <a v-for="node in getNodes" :key="node.id" @click="selectNode(node)">
          {{ node.id }} <br />
        </a>
      </div>
    </div>
    <GraphComponent
      ref="graphRef"
      :initial_crawl_link="initial_crawl_link"
      :refresh_rate="refresh_rate"
      :getFirst="getFirst"
      :total_number_of_nodes="total_number_of_nodes"
      :number_of_nodes_per_branch="number_of_nodes_per_branch"
    />
  </div>
</template>

<script>
import GraphComponent from '@/components/GraphComponent.vue'
import { ref, onMounted } from 'vue'

export default {
  name: 'ForceGraph',
  setup() {},
  data() {
    return {
      width: 500,
      height: 500,
      initial_crawl_link: 'https://en.wikipedia.org/wiki/Albert_Einstein',
      refresh_rate: 100,
      searched_text_input: '',
      number_of_nodes_per_branch: 10,
      total_number_of_nodes: 500,
      dataGraph: null,
      selectedNode: { id: 'no node selected yet' },
      getFirst: true,
      button_pressed: false,
      graph: {
        nodes: [{ id: '' }],
        links: []
      }
    }
  },
  computed: {
    getNodes() {
      if (this.dataGraph) {
        const all_nodes = this.dataGraph.getNodes()
        return all_nodes.filter((node) =>
          node.id.toLowerCase().includes(this.searched_text_input.toLowerCase())
        )
      } else {
        console.log('getNodes: graphRef is null')
      }
      return [{ id: '' }]
    }
  },
  methods: {
    getSelectedNode() {
      if (this.dataGraph) {
        return this.dataGraph.getSelectedNode()
      }
      return { id: '' }
    },
    callStartGraph() {
      const graphRef = this.$refs.graphRef
      if (graphRef) {
        this.button_pressed = true
        this.dataGraph = graphRef
        graphRef.startGraph().then(() => {
          console.log('done')
          graphRef.updateGraph()
        })
      } else {
        console.log('callStartGraph: graphRef is null')
      }
    },
    selectNode(node) {
      if (this.dataGraph) {
        this.dataGraph.highlightNode(node)
      } else {
        console.log('selectNodes: graphRef is null')
      }
      return null
    },
    resetGraph() {
      if (this.dataGraph) {
        this.dataGraph.resetGraph()
        this.dataGraph.updateGraph()
      } else {
        console.log('resetGraph: graphRef is null')
      }
    }
  },
  components: {
    GraphComponent
  }
}
</script>

<style scoped>
.form-container {
  position: absolute;
  display: flex;
  flex-direction: column;
  max-width: 40vw;
  left: 20px;
  top: 50px;
  overflow: scroll;
}

.form-group {
  margin-bottom: 20px; /* Adds space between inputs */
  left: 0;
}

label {
  margin-bottom: 5px;
}

input[type='text'],
input[type='range'],
input[type='checkbox'] {
  display: block;
  max-width: 40vw;
}

input[type='checkbox'] {
  width: auto;
}
</style>
