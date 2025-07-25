
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
   getSetclass(params) {
    return axios.post(base.baseUrl + base.setclass, params)
   },
   getQueryclass(params) {
    return axios.post(base.baseUrl + base.queryclass, params)
   },
   getJoinclass(params) {
    return axios.post(base.baseUrl + base.joinclass, params)
   },
   getAddcomment(params) {
    return axios.post(base.baseUrl + base.addcomment, params)
   },
   getshowcomment(params) {
    return axios.post(base.baseUrl + base.showcomment, params)
   },
   //change
  getquestion() {
  return axios.get(base.popquizUrl + base.quiz)
  },

  //
  uploadPDF(formData) {
    return axios.post(base.popquizUrl+base.uploadpdf, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },

  // 上传 TXT 文件
  uploadText(formData) {
    return axios.post(base.popquizUrl+base.uploadtext, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
}

export default api

