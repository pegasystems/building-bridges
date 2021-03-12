const proxy = require('http-proxy-middleware');

const API_ENDPOINT = 'http://localhost:8888';

module.exports = function(app) {
  app.use(proxy('/api', {
    target: API_ENDPOINT,
    changeOrigin: true
  }));
};
