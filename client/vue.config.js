

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer:{
    proxy:{
      '/api':{
        // TODO: 解决地址硬编码的问题，把它放到本地文件中，现在仍有无法导入文件的问题
        target:"http://localhost:5000",
        changeOrigin: true,
        ws: true,
        pathRewrite:{
          '^/api': ''
        }
      }
    }
  }
})
