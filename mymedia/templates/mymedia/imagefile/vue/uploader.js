{% load staticfiles %}
var Uploader = Vue.extend({
    props: ['modalState'], template: '#imagefile-uploader-template',
    data(){
        return{
          oiginal: {},
          instance: {},
          image: {},
          access_options: [
            { text: 'Public', value: 'public' },
            { text: 'Protected', value: 'protected' }
          ]
        }
    },
    mounted(){
    },
    computed: {
       endpoint(){
           if(this.instance.id){
             return "{% url 'mymedia_api:imagefile-detail' pk='___' %}".replace('___', this.instance.id); }
           else {return "{% url 'mymedia_api:imagefile-list' %}"; }
       },
       tags_json(){
         try{
            return JSON.stringify(
                  this.instance.tags.split(',').map((i)=>i.trim()) );
          }catch(e) {
            return '[""]'
          }
       },
       uploadData(){
         var vm = this;
         var formData = new FormData();
         ['access', 'data', 'tags', 'filename', 'title'].forEach((i) => {
            val = vm.instance[i];
            if (vm.instance.id){ //Update
              if(vm.original[i] != val){
                  formData.append( i,  (i == 'tags') ? vm.tags_json : val);
              }
            }else { // New
              formData.append(i,  (i == 'tags') ? vm.tags_json : val);
            }
          });
          console.log(formData);
         return formData;
       },
       currentImage(){
          if(this.image.thumbnail)
            return this.image.thumbnail;
          if(this.instance.id)
            return this.instance.data;
       }
    },
    methods: {
      setId(prefix, id){
          return prefix + "-" +id;
      },
      onHidden(){
        this.resetForm();
      },
      setOriginal(original){
          this.original = original;
          this.instance = Object.assign({}, original);
      },
      resetForm(){
          // TODO: clear form
          this.instance = {};
          this.image = {};
      },
      uploadFile(evt) {
        evt.preventDefault(); // Prevent modal from closing
        if (!this.instance.data) {
            console.log("no data");
        } else {
            this.uploadInstance();
        }
      },
      createImage(file) {
         var image = new Image();
         var vm = this;
         var reader = new FileReader();
         reader.onload = function(e) {
            var img = {thumbnail: e.target.result, uploadFile: file, name: file.name};
            vm.image = img;
         };
         reader.readAsDataURL(file);
      },
      onFileChanged(e){
          var vm = this;
          var files = e.target.files || e.dataTransfer.files;
          vm.createImage(files[0]);
          let params = new URLSearchParams();
          params.append('csrfmiddlewaretoken', vm.$root.csrftoken);
          params.append('filename',  files[0].name);
          return axios.post("{% url 'mymedia_api:filenames' %}", params)
            .then((res)=>{
                vm.instance.filename = res.data.filename;
                vm.instance.title= res.data.title;
                vm.$forceUpdate();    // rebind to UI
            });
      },
      uploadInstance(){
          var vm = this;
          var config = {headers: {'content-type': 'multipart/form-data'}};
          var data = vm.uploadData;
          axios.defaults.xsrfCookieName = 'csrftoken';
          axios.defaults.xsrfHeaderName = 'X-CSRFToken';
          var method = vm.instance.id ? 'patch' : 'post';
          console.log("uploadInstance:...", method, data)
          axios[method](vm.endpoint, data, config)
            .then(function(res) {vm.$refs.dialog.hide(); })
            .catch(function(error){console.log(error.response); });
      }
    }
});
