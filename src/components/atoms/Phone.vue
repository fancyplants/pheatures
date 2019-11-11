<template>
  <span @click="handleClick" class="tag is-primary phone button">{{ phone }}</span>
</template>

<style lang="scss" scoped>
.phone {
  font-size: 22px;
  margin: 5px;
}
</style>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    phone: String
  },
  setup({ phone }, { emit }) {
    function handleClick() {
      emit("click", phone);
    }

    return {
      handleClick
    };
  }
});
</script>
