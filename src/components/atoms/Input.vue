<template>
  <div>
    <input v-model="text" class="input" @input="onChange">
      <span class="tag"></span>
    </input>
    <h1>Text: {{ text }}</h1>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ref, watch } from "@vue/composition-api";

export default Vue.extend({
  setup(_, { emit }) {
    const text = ref("");

    function onChange() {
      emit("input", text.value);
    }

    return {
      text,
      onChange
    };
  }
});
</script>
