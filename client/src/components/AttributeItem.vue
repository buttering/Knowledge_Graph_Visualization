<template>
  <div>{{attr_key}}, {{attr_value}}</div>
</template>

<script>
export default {
  name: "AttributeItem",
  props:{
    attr_key: String,
    attr_value: String
  }
}
</script>

<style scoped>

</style>