import config from "./config";

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer:{
    proxy:{
      '/api':{
        target:config.default_url,
        changeOrigin: true,
        ws: true,
        pathRewrite:{
          '^/api': ''
        }
      }
    }
  }
})
