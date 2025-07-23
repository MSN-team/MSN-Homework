<template>
  <router-view/>
</template>
<script>
import { useRoute, useRouter } from 'vue-router'
export default {
  setup() {
    const route = useRoute()
    const router = useRouter()

    // 如果当前路径不是 /login，则跳转
    if (route.path !== '/login') {
      router.push('/login')
    }

    return {}
  }
}
</script>
<style>
  html,body,#app{
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
  }
</style>
