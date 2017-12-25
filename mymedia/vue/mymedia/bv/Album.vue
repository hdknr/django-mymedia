<template>
  <b-container fluid>
    <b-row >
      <b-col cols="2"> </b-col>
      <b-col cols="8"> </b-col>
      <b-col cols="2" class="text-right">
        <mymedia-toggle v-model="show_meta"> </mymedia-toggle>
      </b-col>
    </b-row>

    <b-row>
      <b-col :cols="main_cols"  style="transition: .4s;">

          <b-row id="slide-container">

            <b-col cols="2"
                :class="{'border-danger': value.current==media, 'border': value.current==media}"
                v-for="(media, position) in all_mediafiles"
                :key="media.id"
                @dragstart="on_dragstart(position, $event)"
                @dragenter="on_dragenter(position, $event)"
                @dragend="on_drop($event)"
                draggable="true">

                <span class="far fa-trash-alt"
                  data-toggle="tooltip" data-placement="top"
                  title="{% trans 'Remove MediaFile' %}"
                  @click="removeFile(position)"></span>

                <b-img width="120px"
                  class="rounded media-move-handle"
                  @click="selectFile(position)"
                  style="padding-top: 5px" :src="media.data" >
                </b-img>

                <span> {{ position }}.{{ media.title }}
                </span>
            </b-col>

            <b-col cols="2">
              <b-button  variant="outline-primary" @click="$refs.gallery.$refs.dialog.show();"
                style="width:100%; height:100%; margin:5px;">Add...</b-button>
              <mymedia-gallery ref="gallery" @on-select="onImageSelected"></mymedia-gallery>
            </b-col>

          </b-row>
      </b-col>

      <b-col :cols="meta_cols" class="pl-2" v-if="show_meta"  style="transition: .4s;">
          <mymedia-mediafile
            @on-mediafile-updated="replaceCurrentMediaFile"
            v-model="value.current" v-if="value.current"></mymedia-mediafile>
      </b-col>

    </b-row>
  </b-container>
</template>

<script>
import Gallery from './Gallery.vue'
import Toggle from './Toggle.vue'
import MediaFile from './MediaFile.vue'

export default {
  props: ['value', 'instanceId', 'modalState'],
  components: {
    'mymedia-gallery': Gallery,
    'mymedia-toggle': Toggle,
    'mymedia-mediafile': MediaFile},
  data: function(){
    return {
      show_meta: false,
      drag: null, dragenter: null
    };
  },
  computed:{

    all_mediafiles(){
      try{
        return this.value.mediafiles;
      }catch(e){ return [];}
    },
    main_cols(){return this.show_meta ? 8: 12;},
    meta_cols(){return this.show_meta ? 4: 0;},
  },
  created(){
    try{
      if(this.value && this.value.mediafiles)
        this.value.current = this.value.mediafiles[0];
    }catch(e){}
  },
  methods: {
     update(){
       this.$root.send('album-list', this.value);
     },
     on_dragstart(position,e) {this.drag = position;},
     on_dragenter(position, e){this.dragenter = position; },
     on_drop(e) {
        this.value.mediafiles.splice(
          this.dragenter, 0,
          this.value.mediafiles.splice(this.drag, 1)[0]);
        this.$emit('input', this.value); },

     selectFile(index){
        Vue.set(this.value, 'current', this.value.mediafiles[index]);
        this.$forceUpdate();      // to make highlight the selected one
      },

     removeFile(index){
       this.value.mediafiles.splice(index, 1);
       if(this.value.mediafiles.length < 1)
          Vue.set(this.value, 'current', null);
       this.$emit('input', this.value);
     },

     addFiles(mediafiles){
      Array.prototype.push.apply(
        this.value.mediafiles, mediafiles);
      this.$emit('input', this.value);
      this.$forceUpdate();      // to make highlight the selected one
      },

      onImageSelected(mediafile, selected){
        if(selected == true){
          this.value.mediafiles.push(mediafile);
          this.$emit('input', this.value);
          this.$forceUpdate();      // to make highlight the selected one
        }
      },

     replaceCurrentMediaFile(item){
       var i = this.value.mediafiles.findIndex(el => el.id === item.id);
       Vue.set(this.value, 'current', item);
       this.value.mediafiles[i] = item;
       this.$forceUpdate();
     }
  }
}
</script>
