'use strict'
const { VueLoaderPlugin } = require('vue-loader');
const path = require('path');

module.exports = {
  mode: 'development',
  watch:true,
  entry: [
    './js/index.js'
  ],
  output:{
    filename:'bundle.js',
    path:path.resolve(__dirname, './js/')
  },
  module: {
    rules: [
      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        use: [
          'file-loader',
          {
            loader: 'image-webpack-loader',
            options: {
              bypassOnDebug: true, // webpack@1.x
              disable: true, // webpack@2.x and newer
            },
          },
        ],
      },
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          {
            loader: 'css-loader',
            options: {
              // enable CSS Modules
              modules: false,
              // customize generated class names
              localIdentName: '[local]_[hash:base64:8]'
            }
          }
        ]
      },
      
    ]
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}