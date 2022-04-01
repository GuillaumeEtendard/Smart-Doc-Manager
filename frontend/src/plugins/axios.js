import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'X-USER-ID': 1 }
});

export default instance;
