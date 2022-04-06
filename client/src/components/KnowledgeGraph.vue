<template>
  <div id="chart" style="width: 100%;height: 100%"></div>

  <SearchBar
      :node_name_list="node_name_list"
      :edge_name_list="edge_name_list"
      @inquire="inquire_data"
  ></SearchBar>
  <edit-bar
      :clicked= true
      :clicked_ele_id="click_ele_id"
      :clicked_ele_type="click_ele_type"
      :clicked_ele_label="clicked_ele_label"
      :clicked_ele_attribute="click_ele_attribute"
  ></edit-bar>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import EditBar from "@/components/EditBar";

import * as echarts from 'echarts/core'
import {GraphChart} from 'echarts/charts'
import {
  TitleComponent,
  GridComponent,
  LegendComponent,
  ToolboxComponent,
  VisualMapComponent,
  DataZoomComponent,
  TimelineComponent,
  CalendarComponent
} from 'echarts/components'
import {CanvasRenderer} from 'echarts/renderers'
import axios from "axios";
import config from "../../config";

export default {
  name: "KnowledgeGraph",
  data(){
    return {
      click_ele_id: 12,
      click_ele_type: "节点",  // '节点' or '关系'
      clicked_ele_label: 'Person',
      click_ele_attribute: {name: 'Wang Jiawei', age: 18, height: 180},
      clicked: true,

      // 以下两个变量需要传递给SearchBar
      node_name_list: [],
      edge_name_list: [],

      nodes: [],
      edges: [],

      cypher_sentiment: "",

      main_attribute:{}  // 展示在节点上的属性,每种标签的节点可定制一个属性名
    }
  },
  props:{

  },
  methods:{
    // 所有查询都通过这个方法进行
    inquire_data(cypher_sentiment = null, return_type = null){
      const that = this;
      // 查询所有节点和关系，直接访问url即可
      if (cypher_sentiment === null){
        axios.get(config.graph_url).then(function (response){
          // 回调函数中this指向会改变，所以先用that保存Vue对象指针that.node_name_list = response.data.msg.node_name_list
          that.node_name_list = response.data.msg.node_name_list
          that.edge_name_list = response.data.msg.edge_name_list
          that.nodes = response.data.msg.nodes
          that.edges = response.data.msg.edges
          console.log('Get data:', response.data.msg)
        }).catch(error=>{
          if (error.response) {
            // 请求已发出，且服务器的响应状态码超出了 2xx 范围
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            // 请求已发出，但没有接收到任何响应
            // 在浏览器中，error.request 是 XMLHttpRequest 实例
            // 在 node.js 中，error.request 是 http.ClientRequest 实例
            console.log(error.request);
          } else {
              // 引发请求错误的错误信息
              console.log('Error', error.message);
          }
          console.log(error.config);
        });
      // 进行Cypher查询
      }else {
        axios({
          method: 'post',
          url: config.graph_url,
          data:{
            "Cypher-Sentiment": cypher_sentiment,
            "Return-Type": return_type
          }
        }).then(function (response){
          that.nodes = response.data.msg.nodes
          that.edges = response.data.msg.edges
          console.log('Get data:', response.data.msg)
        }).catch(error=>{
          if (error.response) {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          } else if (error.request) {
            console.log(error.request);
          } else {
              console.log('Error', error.message);
          }
          console.log(error.config);
        });
      }
    },

    format_node(){
      let formatted_node = []
      // vue组件的property不能使用for-in进行数组的变量，因为数组在vue中是由一个代理对象进行包裹的
      for (let i = 0; i < this.nodes.length; i ++){
        let node = this.nodes[i]
        let new_node = {
          id : String(node['<id>']),
          category: this.node_name_list.indexOf(node.label),  // 节点类型所在类目的index
          name: node.attribute[ this.main_attribute[node.label] ]  // 显示在节点上的属性值,选择哪个属性进行展示由this.main_attribute决定
        }
        formatted_node.push(new_node)
      }
      console.log('formatted_node:', formatted_node)
      return formatted_node
    },
    format_edge(){
      let formatted_edge = []
      for (let i = 0; i < this.edges.length; i ++){
        let new_edge = {
          source: String(this.edges[i].source),
          target: String(this.edges[i].target),
          type: this.edges[i].type
        }
        formatted_edge.push(new_edge)
      }
      console.log('formatted_edge:', formatted_edge)
      return formatted_edge
    },
    // 对节点显示哪个属性进行设置
    set_main_attribute(label=null, attribute_name=null){
      if (label === null) {  // 自动设置
        for (let i = 0; i < this.nodes.length; i++) {
          let node_label = this.nodes[i].label
          if ( Object.keys(this.main_attribute).indexOf(node_label) < 0 ) {
            //  获取第一个属性名
            let node_first_attribute = ""
            let keys = Object.keys(this.nodes[i].attribute)
            if ( keys.indexOf('name') >= 0 ) {  // 预设几个高优先级属性
              node_first_attribute = 'name'
            } else if ( keys.indexOf('title') >= 0 ) {
              node_first_attribute = 'title'
            } else if (this.nodes[i].attribute) {
              node_first_attribute = Object.keys(this.nodes[i].attribute)[0]
            }
            this.main_attribute[node_label] = node_first_attribute
          }
        }
      }else{
        this.main_attribute[label] = attribute_name
      }
    },

    init_charts(){
      // let category = ['A', 'B', 'C']
      echarts.use([
        GraphChart,
        TitleComponent,
        CanvasRenderer,
        GridComponent,
        LegendComponent,
        ToolboxComponent,
        VisualMapComponent,
        DataZoomComponent,
        TimelineComponent,
        CalendarComponent
      ])
      let that = this
      if (!this.myChart){
        this.myChart = echarts.init(document.getElementById('chart'), 'dark')
      }
      let option = {
        animationDurationUpdate: 1500,  // 启动动画时长
        animationEasingUpdate: 'quinticInOut',  // 动画速率曲线
        series: [
          {
            name: 'graph',
            type: 'graph',
            layout: 'force',  // 力引导布局
            // legendHoverLink: true,  // 开启图例hover时的联动高亮
            // hoverAnimation: true,
            edgeSymbol: ['circle', 'arrow'],  // 箭头样式
            // force: {
            //   edgeLength: 120,  // 节点距离
            //   repulsion: 500  // 斥力因子
            // },
            roam: true,  // 开启鼠标缩放和平移漫游
            draggable: true,  // 节点可拖拽
            lineStyle:{  // 边的样式
              width: 2,
              curveness: 0.1
            },
            label:{  // 展示图形标签
              color: '#FFFFFF',
              position: 'inside',
              show: true,
              fontSize: 12,
              fontStyle: 'normal',
              fontWeight: 'bold',
              fontFamily: 'serif',
              // backgroundColor: 'rgba(0, 21, 11, 0.3)',  // 文字块背景颜色
              // borderRadius: 10,  // 文字块圆角，
              // padding: 4  // 文字块内边距
            },
            emphasis: {  // 高亮状态配置
              scale: true,  // 节点放大
              focus: 'adjacency',  // 聚焦邻接点
              label: {
                position: 'top'
              },
              lineStyle: {
                width: 10,

              },
              edgeLabel: {
                show: true,
                formatter: (params) => { return params.data.type }
              }
            },
            categories: [],
            symbolSize: 18,  // 节点大小
            nodes: [{}],
            edges: [{}],
            // cursor: 'cursor'  // 鼠标悬浮时在图形元素上时鼠标的样式是什么
          }
        ]
      };
      this.myChart.setOption(option)
      window.onresize = function (){
        that.myChart.resize()
      }
    },

    string_hash_to_number(string){
      let number = ''
      for (let char of string){
        number += String(char.charCodeAt())
      }
      return Number(number)
    }
  },

  watch: {
    // 该回调会在任何被侦听的对象的 property 改变时被调用，不论其被嵌套多深
    nodes: {
      // 更新echarts数据
      handler(){
        // TODO:更新图标
        this.set_main_attribute()
        let option = this.myChart.getOption()
        option.series[0].nodes = this.format_node(this.nodes)
        option.series[0].edges = this.format_edge(this.edges)
        option.series[0].categories = Object.values(this.node_name_list)
        console.log('option:', option)
        this.myChart.setOption(option)
      }
    },

  },
  mounted() {
    this.inquire_data()
    this.init_charts()
    // TODO:查询所有元素

  },
  components: {
    SearchBar,
    EditBar,
  }
}
</script>

<style scoped>

</style>