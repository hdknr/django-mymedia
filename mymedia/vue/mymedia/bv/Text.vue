<template>
  <div>
    <div
      @click="orginal=value; editing=true"
      v-show="!editing">
      <span v-if="value">{{ value }}</span>
      <span v-else>Click to Edit</span>
    </div>

    <b-form flud v-show="editing">

      <b-form-textarea
        @blur.native="updateText($event)"
        :value="value" placeholder="Enter something" v-if="multiline==true">
     </b-form-textarea>

      <b-input-group v-else>
        <b-form-input type="text" :required="true"
          @blur.native="updateText($event)"
          :value="value"></b-form-input>
         <b-input-group-addon @click="editing=false">
           <strong class="text-danger far fa-times-circle"></strong>
         </b-input-group-addon>
     </b-input-group>

   </b-form>
  </div>
</template>

<script>

export default {

  props: ['value', 'multiline'],
  data(){
      return{
          editing: false,
          original: ''
      }
  },
  methods: {
    updateText(ev){
      if(ev.target.value && ev.target.value != this.original){
        this.editing = false;
        this.$emit('input', ev.target.value);
      }
      else{
          this.value = this.orginal;
      }
    }
  }
}
</script>
