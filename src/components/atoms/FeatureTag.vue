<template>
  <span :class="spanClass">
    {{ feature }}
    <button :class="deletable ? 'delete' : 'invisible'" @click="handleDelete"></button>
  </span>
</template>

<style lang="scss" scoped>
.feature {
  margin: 4px;
}

.invisible {
  display: none;
}
</style>

<script lang="ts">
import Vue, { PropType } from "vue";
import { computed } from "@vue/composition-api";

export default Vue.extend({
  props: {
    feature: String,
    deletable: Boolean
  },
  setup({ feature, deletable }, { emit }) {
    const spanClass = computed(() => {
      const val = (feature as string)[0];

      return {
        tag: true,
        feature: true,
        "is-large": true,
        "is-success": val === "+",
        "is-danger": val === "-"
      };
    });

    function handleDelete() {
      emit("delete", feature);
    }

    return {
      spanClass,
      handleDelete
    };
  }
});
</script>
