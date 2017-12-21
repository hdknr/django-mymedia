<template>
  <b-row v-if="value" no-gutters="true">

    <b-col cols="12">
      <b-row>
        <b-col cols="10">
        </b-col>
        <b-col cols="2" class="text-right">
          <mymedia-toggle v-model="show_meta"> </mymedia-toggle>
        </b-col>
      </b-row>

      <b-row>
        <b-col :cols="main_cols" style="transition: .4s;">
          <div class="mx-1">

            <b-img fluid class="rounded" style="padding-top: 5px"
              @click="$refs.gallery.$refs.dialog.show()" :src="value.data" v-if="value.data">
            </b-img>
            <b-button v-else @click="$refs.gallery.$refs.dialog.show()">Select Image</b-button>

            <mymedia-gallery ref="gallery" @on-select="onImageSelected"></mymedia-gallery>
          </div>
        </b-col>

        <b-col :cols="meta_cols" v-if="show_meta" style="transition: .4s; ">
          <mymedia-mediafile v-model="value"></mymedia-mediafile>
        </b-col>
      </b-row>

    </b-col>
  </b-row>
</template>

<script>
import Text from 'mymedia/bv/Text.vue'
import Gallery from 'mymedia/bv/Gallery.vue'
import MediaFile from 'mymedia/bv/MediaFile.vue'
import Toggle from 'mymedia/bv/Toggle.vue'

export default {
  props: ['value', ],
  components:{
    'mymedia-text': Text,
    'mymedia-gallery': Gallery,
    'mymedia-mediafile': MediaFile,
    'mymedia-toggle': Toggle,
  },
  data: function(){
    return {show_meta: false};
  },
  computed:{
      main_cols(){ return this.show_meta ?  8: 12; },
      meta_cols(){ return this.show_meta ?  4: 0; },
  },
  methods: {
    onImageSelected(image, selected){
      if(selected == true){
          this.$emit('input', image);
          this.$refs.gallery.$refs.dialog.hide();
      }
    }
  }
};
</script>
