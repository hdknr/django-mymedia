{% load staticfiles %}
var Uploader = Vue.extend({
    props: ['modalState'], template: '#imagefile-uploader-template',
    data(){
        return{
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
           return "{% url 'mymedia_api:imagefile-list' %}";
       },
       tags_json(){
            return JSON.stringify(
                this.instance.tags.split(',').map((i)=>i.trim()) );
       },
       uploadData(){
         var formData = new FormData();
         for(var attr in this.instance){
           var val = this.instance[attr];
           if(val){
              formData.append(attr, (attr=='tags') ? this.tags_json : val);
           }
         }
         return formData;
       }
    },
    methods: {
      setId(prefix, id){
          return prefix + "-" +id;
      },
      onShow(){
          this.resetForm();
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
            console.log("uploadFile", this.instance);
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
          var data = this.uploadData;
          axios.defaults.xsrfCookieName = 'csrftoken';
          axios.defaults.xsrfHeaderName = 'X-CSRFToken';
          var method = vm.instance.id ? 'patch' : 'post';
          axios[method](vm.endpoint, data, config)
            .then(function(res) {vm.$refs.dialog.hide(); })
            .catch(function(error){console.log(error.response); });
      }
    }
});
