<template>
  <div>
    <form @submit="handleSubmit">
      <input class="input" v-model="search" />
    </form>
    <FeatureTag
      v-for="feature in activeFeatures"
      v-bind:key="feature"
      :feature="feature"
      @delete="removeActive"
    />
    <hr />

    <Phone @click="handlePhoneClick" v-for="phone in found" v-bind:key="phone" :phone="phone" />

    <div :class="modalClass">
      <div class="modal-background"></div>
      <div class="modal-content box">
        <h2 class="title notification is-info">{{ currentPhone }}</h2>
        <!-- Any other Bulma elements you want -->
        <FeatureTag
          v-for="feature in modalInfo"
          v-bind:key="feature"
          :feature="feature"
          @click="addActive"
        />
      </div>
      <button @click="handleModalClose" class="modal-close is-large" aria-label="close"></button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ref, watch, computed } from "@vue/composition-api";

import FeatureTag from "@/components/atoms/FeatureTag.vue";
import Phone from "@/components/atoms/Phone.vue";
import { Phones, getFeatures } from "@/utils.ts";

export default Vue.extend({
  components: {
    FeatureTag,
    Phone
  },
  props: {
    phones: Object as PropType<Phones>
  },
  setup(props) {
    const { phones }: { phones: Phones } = props as any;

    const search = ref("");
    const found = ref([] as string[]);
    const activeFeatures = ref([] as string[])
    const modalInfo = ref([] as string[]);
    const currentPhone = ref("");
    const modalClass = computed(() => ({
      modal: true,
      "is-active": modalInfo.value.length > 0
    }));

    watch(activeFeatures, () => {
      found.value = phones.getPhones(activeFeatures.value);
    });

    function removeActive(feature: string) {
      activeFeatures.value = activeFeatures.value.filter(f => f !== feature);
    }

    function addActive(feature: string) {
      // close modal
      modalInfo.value = [];
      if (!activeFeatures.value.includes(feature)) {
        activeFeatures.value.push(feature);
      }
    }

    function handleSubmit(e: Event) {
      e.preventDefault();
      if (search.value.length < 1) {
        return;
      }

      const features = phones.allFeatures;

      switch (search.value[0]) {
        case "+":
        case "-":
        case "0":
          const feat = search.value.substring(1);
          if (features.has(feat)) {
            addActive(search.value);
          }
          break;
      }

      search.value = "";
    }

    function handlePhoneClick(phone: string) {
      const features = phones.getFeatureset(phone);
      const data = Object.keys(features).map(feature => {
        const value = features[feature];

        return value + feature;
      });

      modalInfo.value = data;
      currentPhone.value = phone;
    }

    function handleModalClose() {
      modalInfo.value = [];
      currentPhone.value = "";
    }

    return {
      search,
      found,
      activeFeatures,
      removeActive,
      handleSubmit,
      handlePhoneClick,
      modalClass,
      modalInfo,
      handleModalClose,
      currentPhone,
      addActive
    };
  }
});
</script>
