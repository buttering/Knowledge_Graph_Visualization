<template>
  <el-scrollbar id="add-bar">
    <el-radio-group id="type-button" v-model="
    new_type">
      <el-radio-button label="节点"/>
      <el-radio-button label="关系"/>
    </el-radio-group>

    <div id="type-label">
      <el-icon :size="30" ><key /></el-icon>
      <el-select
          v-model="new_label_type"
          :placeholder="label_or_type"
          filterable
          clearable
          allow-create
          default-first-option
      >
        <el-option
            v-for="(item, index) in select_list"
            :key="index"
            :label="item"
            :value="item"
        />
      </el-select>
    </div>

    <div class="line_01"></div>

    <div v-if="show_node_select" id="graphic">
      <el-tooltip
        effect="dark"
        content="选择起点"
        placement="top"
      >
        <button
          class="node-icon"
          id="source"
          @click="select_node('source')"
        >{{source_node_id}}</button>
      </el-tooltip>
      <div id="arrow">&nbsp;===>&nbsp;</div>
      <el-tooltip
        effect="dark"
        content="选择终点"
        placement="top"
      >
        <button
            class="node-icon"
            id="target"
            @click="select_node('target')"
        >{{target_node_id}}</button>
      </el-tooltip>
    </div>

    <div id="attribute">
      <AddAttributeItem
        v-for="(value, key) in new_attribute"
        :key="key"
        :attr_key="key"
        :attr_value="value"
        @delete_attribute="edit_ele_attribute"
      />
      <NewAttributeItem
        @add_attribute="edit_ele_attribute"
      />
    </div>

    <div id="cancel-submit">
      <el-button id="exit" @click="exit_add_mode">取消</el-button>
      <el-button id="submit" @click="on_submit">提交</el-button>
    </div>
  </el-scrollbar>
</template>

<script>
import {Key} from '@element-plus/icons-vue'
import AddAttributeItem from "@/components/AddAttributeItem";
import NewAttributeItem from "@/components/NewAttributeItem";
export default {

  name: "AddBar",
  data(){
    return {
      source_node_id: -1,
      target_node_id: -1,
      select_type: '',  // 选择的是关系的起点("source")还是终点("target")

      new_type: '关系',  // '节点' or '关系'
      new_label_type: '',
      new_attribute: {}
    }
  },
  props: {
    clicked_node_id: Number,  // 初试被点击的节点默认为起始点
    select_node_id: Number,
    node_name_list: Array,
    edge_name_list: Array
  },
  computed:{
    show_node_select(){
      return this.new_type === '关系'
    },
    label_or_type(){
      if (this.new_type === '节点')
        return '节点标签'
      else
        return '关系类型'
    },
    select_list(){
      if (this.new_type === '节点')
        return this.node_name_list
      else
        return this.edge_name_list

    }
  },
  methods: {
    exit_add_mode(){
      this.$emit("change_mode", 'view')
    },
    select_node(type){
      this.select_type = type
      this.$emit('change_mode', 'select')
    },
    edit_ele_attribute(key, value=null){
      if (value === null)
        delete this.new_attribute[key]
      else
        this.new_attribute[key] = value
    },
    on_submit(){
      if (this.new_type === '节点'){
        if (this.new_label_type === ''){
          this.$message.warning("请输入节点标签！")
          return
        }
        this.$emit("add_element", this.new_type, this.new_label_type, this.new_attribute )
      } else if (this.new_type === '关系') {
        if (this.source_node_id < 0 || this.target_node_id < 0) {
          this.$message.warning("请选择起始节点！")
          return
        }
        if (this.new_label_type === ''){
          this.$message.warning("请输入关系类型！")
          return;
        }
        this.$emit("add_element", this.new_type, this.new_label_type, this.new_attribute, this.source_node_id, this.target_node_id)
      }
    }
  },
  watch: {
    select_node_id: {
      handler(){
        if (this.select_type === 'source')
          this.source_node_id = this.select_node_id
        else if (this.select_type === 'target')
          this.target_node_id = this.select_node_id
      }
    },
    new_type: {
      handler(){
        this.new_label_type = ''
      }
    }
  },
  mounted() {
    this.source_node_id = this.clicked_node_id
  },
  components: {
    AddAttributeItem,
    NewAttributeItem,
    Key
  }
}
</script>

<style scoped>
#add-bar{
  position: fixed;
  right: 5%;
  top: 50%;
  transform:translate(0px,-50%);
  height: 70%;
  width: 300px;
  border-radius: 5px;
  background: rgba(243, 248, 251, 0.6);
}
#type-button{
  width: 90%;
  padding: 5%;
}

/deep/ .el-radio-button{
  flex: 1;
}
/deep/ .el-radio-button__inner{
  width: 100%;
}

#type-label{
  display: flex;
  width: 90%;
  height: 31px;
  padding: 5%;
}
/deep/ .el-icon{
  padding-right: 10px;
  vertical-align: middle;
  height: 100%;
}

/deep/ .el-select{
  width: 100%;
}

#graphic{
  display: flex;
  width: 80%;
  padding-left: 10%;
  padding-right: 10%;
  justify-content: space-between;
}
.node-icon{
  width: 70px;
  height: 70px;
  border: 0;
  border-radius: 50%;
  font-size: 30px;
  font-weight: 700;
  font-family: Source Han Sans CN,serif;
  line-height: 0;
  transition-duration: 0.2s;
  cursor: pointer;

}
#graphic button:hover{
  background: #FFFFFF;
}
#source{
  background: #64CCFC;
}
#target{
  background: #1CACF4;
}
#arrow{
  height: 70px;
  line-height: 70px;
  font-size: 30px;
  font-weight: 700;
}

#cancel-submit{
  position: fixed;
  width: 90%;
  bottom: 0;
  display: flex;
  padding: 5%;
}
/deep/ .el-button{
  flex: 1;
  border: 0;
}

#attribute{
  width: 90%;
  padding: 5%;
}

.line_01{
  margin: 5%;
  border: 1px solid black;
  height: 0;
}
</style>