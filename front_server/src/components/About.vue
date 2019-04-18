<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'About',
  data () {
    return {
      msg: 'hello world!'
    }
  },
  /* ajax请求获得数据 */
  methods: {
    getMessage () {
      const path = 'http://localhost:3000/about'
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
