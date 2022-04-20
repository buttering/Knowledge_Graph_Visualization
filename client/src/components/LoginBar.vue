<template>
  <div
      class="login"
      v-if="model==='login'"
      v-loading="loading"
      element-loading-text="登录中..."
  >

    <div id="username">
      <el-icon :size="35"><UserFilled/></el-icon>
      <el-input
          v-model="username"
          placeholder="输入用户名"
          size="large"
          clearable
      />
    </div>

    <div id="password">
      <el-icon :size="35"><Sunrise/></el-icon>
      <el-input
        v-model="password"
        placeholder="输入密码"
        size="large"
        show-password/>
    </div>

    <div class="button">
      <el-button type="primary" @click="login">登录</el-button>
      <el-button type="success" @click="to_register">注册</el-button>
    </div>
  </div>

  <div
      class="login"
      v-if="model==='register'"
      v-loading="loading"
      element-loading-text="注册中..."
  >
    <div id="username1">
      <el-icon :size="35"><UserFilled/></el-icon>
      <el-input
          v-model="username"
          placeholder="输入用户名"
          size="large"
          clearable
      />
    </div>

    <div id="password1">
      <el-icon :size="35"><Sunrise/></el-icon>
      <el-input
        v-model="password"
        placeholder="输入密码"
        size="large"
        show-password
      />
    </div>

    <div id="email">
      <el-icon :size="35"><Message/></el-icon>
      <el-input
        v-model="email"
        placeholder="输入邮箱"
        size="large"
        clearable
      />
    </div>
    <div id="type">
      <el-icon :size="35"><Location/></el-icon>
      <el-select
          v-model="type"
          placeholder="选择角色"
          size="large"
      >
        <el-option
            v-for="item in user_types"
            :key="item"
            :label="item"
            :value="item"
        />
      </el-select>
    </div>
    <div id="code" v-if="need_code">
      <el-icon :size="35"><Key/></el-icon>
      <el-input
        v-model="code"
        placeholder="输入邀请码"
        size="large"
      />
    </div>
    <div class="button">
      <el-button type="primary" @click="to_login">返回登录</el-button>
      <el-button type="success" @click="register">注册</el-button>
    </div>
  </div>

</template>

<script>
import {UserFilled, Sunrise, Message, Location, Key } from '@element-plus/icons-vue'
import axios from "axios";
import config from "../../config";

export default {
  name: "LoginBar",
  data(){
    return {
      username: '',
      password: '',
      email: '',
      type: '游客',
      code: '',
      model: 'login',
      failure_msg: '',
      loading: false,
      user_types: ['游客', '专家', '管理员']
    }
  },
  computed: {
    need_code(){
      return this.type !== '游客';
    }
  },
  methods: {
    login(){
      this.loading = true
      let that = this
      let data = {
        "username": this.username,
        "password": this.password
      }
      axios({
        method: 'post',
        url: config.session_url,
        data: data
      }).then(function (response){
        that.loading = false
        if (response.status === 200 && response.data.code === 200)
          that.$emit('login', response.data.token, that.username)
        else if (response.data.code === 401) {
          that.failure_msg = response.data.msg
          that.$message.warning('登录失败')
        }
      }).catch(error=>{
        that.loading = false
        that.attribute_bar_loading = false
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
      })
    },
    register(){
      if (this.username === ''){
        this.$message.warning('请填写用户名')
        return;
      } else if (this.password === ''){
        this.$message.warning('请填写密码')
        return;
      } else if (this.email === ''){
        this.$message.warning('请填写邮箱')
        return;
      } else if (this.type !== '游客' && this.code === ''){
        this.$message.warning('请填写邀请码')
        return;
      } else {
        this.loading = true
        let that = this
        let type
        if (this.type === '游客')
          type = 'common'
        else if (this.type === '专家')
          type = 'specialist'
        else
          type = 'administrator'
        let data = {
          username: this.username,
          password: this.password,
          email: this.email,
          type: type,
          code: this.code
        }
        axios({
          method: 'post',
          data: data,
          url: config.user_url
        }).then(function (response){
          if (response.status === 200 && response.data.code === 200){
            that.model = 'login'
            that.$message.success('注册成功')
          } else if (response.data.code === 401)
            that.$message.warning('用户名已被占用')
          else if (response.data.code === 402)
            that.$message.warning('邮箱已被注册')
          else if (response.data.code === 403)
            that.$message.warning('无效的密码格式！')
          else if (response.data.code === 404)
            that.$message.warning('无效的验证码')
          that.loading = false
        }).catch(error=>{
          that.loading = false
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
        })
      }
    },
    to_register(){
      this.model = 'register'
    },
    to_login(){
      this.model = 'login'
    }
  },
  components: {
    UserFilled,
    Sunrise,
    Message,
    Location,
    Key
  }
}
</script>

<style scoped>
.login{
  position: fixed;
  margin: 20% 30%;
  width: 40%;
  border-radius: 5%;
  font-size: 30px;
  font-weight: 700;
  font-family: Source Han Sans CN,serif;
  line-height: 0;
  background-color: #B9E8F8;
}
#username, #password, #username1, #password1, #email, #type, #code{
  margin: 10% 10%;
  display: flex;
}
/deep/ .el-select{
  width: 100%;
}
/deep/ .el-icon{
  margin-right: 10px;
}
.button{
  display: flex;
  /*position: fixed;*/
  bottom: 5%;
  margin: 10%;
}
.login button{
  width: 50%;
}

</style>