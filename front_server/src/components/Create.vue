<template>
  <div class="hello">
    <h1>{{ msg["url"] }}</h1>
  </div>
</template>

<script>

import axios from 'axios'
export default {
  name: 'Create',
  data () {
    return {
      msg: '欢迎来到菜鸟教程！'
    }
  },
  /* ajax请求获得数据 */
  methods: {
    getMessage () {
      const path = 'http://localhost:3000/container/create'
      axios.get(path)
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created () {
    this.getMessage()
  }
}
</script>

<style scoped>

</style>
