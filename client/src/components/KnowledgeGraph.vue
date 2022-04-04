<template>
  <div id="chart" style="width: 100%;height: 100%"></div>

  <SearchBar
      :node_name_list="node_name_list"
      :edge_name_list="edge_name_list"
  ></SearchBar>
  <edit-bar
      :clicked="clicked"
      :clicked_ele_id="click_ele_id"
      :clicked_ele_type="click_ele_type"
      :clicked_ele_attribute="click_ele_attribute"
  ></edit-bar>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import EditBar from "@/components/EditBar";

import * as echarts from 'echarts/core'
import {GraphChart} from 'echarts/charts'
import {TitleComponent, GridComponent} from 'echarts/components'
import {CanvasRenderer} from 'echarts/renderers'

export default {
  name: "KnowledgeGraph",
  data(){
    return {
      title: "Knowledge",
      // click_ele_id: 251,
      click_ele_id: -1,
      click_ele_type: "",
      click_ele_attribute: {},
      clicked: true
    }
  },
  props:{
    node_name_list: Array,
    edge_name_list: Array,
    nodes: Array,
    edges: Array
  },
  methods:{
    init_charts(){
        echarts.use([
            GraphChart,
            TitleComponent,
            CanvasRenderer,
            GridComponent,
        ])
      let that = this
      if (!this.myChart){
        this.myChart = echarts.init(document.getElementById('chart'), 'dark')
      }
      let nodes = [
        {
          name: "韦小宝",
          id: "1",
        },
        {
          name: "方怡",
          id: "2",
        },
        {
          name: "双儿",
          id: "3",
        },
        {
          name: "茅十八",
          id: "4",
        },
        {
          name: "吴六奇",
          id: "5",
        },
      ];
      let option = {
        animationDurationUpdate: 1500,  // 启动动画时长
        animationEasingUpdate: 'quinticInOut',  // 动画速率曲线
        series: [
          {
            type: 'graph',
            layout: 'force',  // 力引导布局
            // legendHoverLink: true,  // 开启图例hover时的联动高亮
            // hoverAnimation: true,
            // edgeLabel: {  // 关系文字样式
            //   position: 'middle',
            //   formatter: '{c}',
            //   show: true
            // },
            // edgeSymbol: ['arrow', ''],  // 箭头样式
            // force: {
            //   edgeLength: 120,  // 节点距离
            //   repulsion: 500  // 斥力因子
            // },
            // roam: true,  // 开启鼠标缩放和平移漫游
            // draggable: true,  // 节点可拖拽
            // itemStyle: {
            //   itemStyle: {
            //     normal: {
            //       color: '#00FAE1',
            //       cursor: 'pointer',
            //       //color:Math.floor(Math.random()*16777215).toString(16),
            //       // color: ['#fc853e','#28cad8','#9564bf','#bd407e','#28cad8','#fc853e','#e5a214'],
            //       label: {
            //         //formatter: "{c}",为什么这个写上就不打开了？
            //         show: true,
            //         position: [-10, -15],
            //         textStyle: { //标签的字体样式
            //           color: '#fff', //字体颜色
            //           fontStyle: 'normal',//文字字体的风格 'normal'标准 'italic'斜体 'oblique' 倾斜
            //           fontWeight: 'bolder',//'normal'标准'bold'粗的'bolder'更粗的'lighter'更细的或100 | 200 | 300 | 400...
            //           fontFamily: 'sans-serif', //文字的字体系列
            //           fontSize: 12, //字体大小
            //         }
            //       },
            //       nodeStyle: {
            //         brushType: "both",
            //         borderColor: "rgba(255,215,0,0.4)",
            //         borderWidth: 1,
            //       },
            //     },
            //     //鼠标放上去有阴影效果
            //     emphasis: {
            //       shadowColor: '#00FAE1',
            //       shadowOffsetX: 0,
            //       shadowOffsetY: 0,
            //       shadowBlur: 40,
            //     },
            //   }
            // },
            // lineStyle:{
            //   width: 2
            // },
            // label:{
            //   color: '#00FAE1',
            //   fontSize: 18
            // },
            // symbolSize: 14,  // 节点大小
            // links: [
            //   {
            //     source: 'n1',
            //     target: 'n2'
            //   }, {
            //     source: 'n2',
            //     target: 'n3'
            //   }
            // ],
            nodes: nodes,
            // cursor: 'cursor'  // 鼠标悬浮时在图形元素上时鼠标的样式是什么
          }
        ]
      };
      this.myChart.setOption(option)
      window.onresize = function (){
        that.myChart.resize()
      }
      // window.onresize = function (){
      //   function getStyle(el, name){
      //     if (window.getComputedStyle){
      //       return window.getComputedStyle(el, null)
      //     }else{
      //       return el.cuttentStyle
      //     }
      //   }
      //   var wi = getStyle()
      // }
    },
  },
  watch: {
    // 该回调会在任何被侦听的对象的 property 改变时被调用，不论其被嵌套多深
    query_result: {
      handler(val, old){
        // TODO:更新图标
        console.log('query_result has changed:', val, old)
      }
    }
  },
  mounted() {
    this.init_charts()
    // TODO:查询所有元素
    this.query_result = {'aaa': 111}
  },
  components: {
    SearchBar,
    EditBar
  }
}
</script>

<style scoped>

</style>