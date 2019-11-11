<template>
  <span :class="spanClass" @click="handleClick">
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

const CLICK_EVENT = "click";
const DELETE_EVENT = "delete";

export default Vue.extend({
  props: {
    feature: String
  },
  setup({ feature }, { emit, listeners }) {
    const deletable = computed(() => {
      // if parent is listening to delete, this should be deletable
      return !!listeners[DELETE_EVENT];
    });

    const spanClass = computed(() => {
      const val = (feature as string)[0];

      return {
        tag: true,
        feature: true,
        "is-large": true,
        "is-success": val === "+",
        "is-danger": val === "-",
        button: !deletable.value
      };
    });

    function handleDelete() {
      emit(DELETE_EVENT, feature);
    }

    function handleClick() {
      emit(CLICK_EVENT, feature);
    }

    return {
      spanClass,
      handleDelete,
      handleClick,
      deletable
    };
  }
});
</script>
