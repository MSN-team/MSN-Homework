
/**
 * 存放所有网络请求地址
 */
const base = {
  baseUrl:"http://localhost:5000",     // 公共地址
  login:"/user/login/",           // 登录地址 
  register:"/user/users/",     // 注册地址
  setclass:"/user/setclass/",
  queryclass:"/user/queryclass/",
  joinclass:"/user/joinclass/",
  addcomment:"/user/addcomment/",
  showcomment:"/user/getcomment/",
  popquizUrl:"http://127.0.0.1:8000",     // 公共地址
  quiz:"/questions",                 // 查询题目
  uploadpdf:"/upload-pdf",
  uploadtext:"/upload-text",
}

export  default base