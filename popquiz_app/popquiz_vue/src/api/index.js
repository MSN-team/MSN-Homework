import axios from "../utils/request.js"
import base from "./base.js"


const api = {
  /**
   * 登录
   */
  getLogin(params) {
    return axios.post(base.baseUrl + base.login, params)
   },
   getRegister(params) {
    return axios.post(base.baseUrl + base.register, params)
   },
}


export default api
