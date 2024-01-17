import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:5000", // Postavljanje osnovne URL adrese
});

// Interceptor koji automatski dodaje osnovnu adresu
instance.interceptors.request.use(function (config) {
  // Dodavanje osnovne adrese svakom zahtevu
  config.url = `${config.baseURL}${config.url}`;
  return config;
}, function (error) {
  return Promise.reject(error);
});

export default instance;