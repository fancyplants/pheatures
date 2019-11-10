<template>
  <div>
    <Input @input="handleText" />
    <p>{{ search }}</p>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import Input from "@/components/atoms/Input.vue";
import { ref } from '@vue/composition-api';

export default Vue.extend({
  components: {
    Input
  },
  setup() {
    const search = ref("");
    function handleText(text: string) {
      search.value = text;
    }

    return {
      search,
      handleText
    }
  }

});
</script>