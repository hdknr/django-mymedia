<template>
  <div>

    <b-button size="sm"
        @click="popTag(tag)" :key="tag.id"
        variant="secondary" v-for="tag in value"
        style="border-radius: 15px;margin: 3px">{{ tag }}</b-button>

    <b-button size="sm" variant="outline-secondary"
      style="border-radius: 15px;margin: 3px"
      @click="newtag=''; editing=true"
      v-show="!editing">
      <i class="fa fa-plus-square" aria-hidden="true"></i> &nbsp;Add Tag...
    </b-button>

    <b-form flud v-show="editing">
      <b-input-group >
        <b-form-input type="text"
          size="sm"
          placeholder="New Tag"
          :required="true"
          value=""
          @blur.native="addTag($event)"></b-form-input>

       <b-input-group-addon @click="editing=false">
         <strong class="text-danger fa fa-times"></strong>
       </b-input-group-addon>

     </b-input-group>
   </b-form>
  </div>
</template>

<script>
export default {
    props: ['value'],
    data(){
      return{
        editing: false,
      }
    },
    methods: {
      popTag(name){
        if(!this.value) this.value = [];
        this.value.splice( this.value.indexOf(name) , 1);
        this.$emit('input', this.value);
      },
      addTag(ev){
        if(!this.value) this.value = [];
        this.value.push(ev.target.value);
        this.editing=false;
        ev.target.value = '';
        this.$emit('input', this.value);
      }
    }
};
</script>
