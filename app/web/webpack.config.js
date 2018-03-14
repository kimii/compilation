const path = require('path');

module.exports = {
  entry: './src/library.js',
  output: {
    filename: 'mylib.js',
    path: path.resolve(__dirname, 'public/javascripts/'),
    library: 'mylib'
  },
  externals: {
    jquery: 'jQuery',
    vis: 'vis',
    d3: 'd3'
  },
  mode: 'development'
};
